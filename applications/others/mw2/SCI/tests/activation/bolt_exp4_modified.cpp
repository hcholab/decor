

#include "FloatingPoint/fp-math.h"
#include "BuildingBlocks/aux-protocols.h"
#include "NonLinear/argmax.h"
#include <fstream>
#include <iostream>
#include <thread>
#include <cmath>
#include <vector>
#include <cstring>
#include <tuple>
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <iomanip>

using namespace sci;
using namespace std;

#define MAX_THREADS 1
#define ALICE 1
#define BOB 2

int party, port = 32000;
int num_threads = 1;
string address = "127.0.0.1";

int dim = 1ULL << 18;
int bw_x = 37;
int bw_y = 37;
int s_x = 12;
int s_y = 12;

// Range constants for input values: [-1000, -0.0001]
const double MIN_RANGE = -1000.0;
const double MAX_RANGE = -0.001;
const uint64_t MIN_FIXED = (uint64_t)(-MIN_RANGE * (1ULL << s_x)); // 4096000
const uint64_t MAX_FIXED = (uint64_t)(-MAX_RANGE * (1ULL << s_x)); // ~0.4 ≈ 1

uint64_t mask_x = (bw_x == 64 ? -1 : ((1ULL << bw_x) - 1));
uint64_t mask_y = (bw_y == 64 ? -1 : ((1ULL << bw_y) - 1));

IOPack *iopackArr[MAX_THREADS];
OTPack *otpackArr[MAX_THREADS];

// Local signed_val function to avoid ambiguity
inline int64_t local_signed_val(uint64_t x, int bw_x) {
    uint64_t pow_x = (bw_x == 64? 0ULL: (1ULL << bw_x));
    uint64_t mask_x = pow_x - 1;
    x = x & mask_x;
    return int64_t(x - ((x >= (pow_x/2)) * pow_x));
}

double computeULPErr(double calc, double actual, int SCALE) {
  double calc_fixed = calc * (1ULL << SCALE);
  double actual_fixed = actual * (1ULL << SCALE);
  double ulp_err = (calc_fixed - actual_fixed) > 0
                         ? (calc_fixed - actual_fixed)
                         : (actual_fixed - calc_fixed);
  return ulp_err;
}

void exp_thread(int tid, uint64_t *x, uint64_t *y, int num_exp) {
  MathFunctions *math;
  if (tid & 1) {
    math = new MathFunctions(3 - party, iopackArr[tid], otpackArr[tid]);
  } else {
    math = new MathFunctions(party, iopackArr[tid], otpackArr[tid]);
  }
  math->lookup_table_exp(num_exp, x, y, bw_x, bw_y, s_x, s_y);

  delete math;
}

void exp4_thread(int tid, uint64_t *x, uint64_t *y, int num_exp) {
  FPMath *fpmath;
  // ArgMaxProtocol<uint64_t> *argmax_oracle;
  int this_party;
  if (tid & 1) {
    this_party = 3 - party;
  } else {
    this_party = party;
  }
  fpmath = new FPMath(this_party, iopackArr[tid], otpackArr[tid]);
  
  // Create FixArray for input data
  FixArray input_array = fpmath->fix->input(this_party, num_exp, x, true, bw_x, s_x);
  
  // Call exp4 function
  auto result_tuple = fpmath->exp4(input_array);
  FixArray output_array = get<0>(result_tuple);
  
  // Copy results back
  memcpy(y, output_array.data, num_exp * sizeof(uint64_t));
  // printf("num_exp: %d\n", num_exp);
  // printf("bw_x: %d\n", bw_x);
  // printf("bw_y: %d\n", bw_y);
  // printf("s_x: %d\n", s_x);
  // printf("s_y: %d\n", s_y);
  // printf("party: %d\n", party);
  // printf("this_party: %d\n", this_party);
  
  // for (int i = 0; i < num_exp; i++) {
  //   printf("x[%u]: %lu\n", i, (unsigned long)x[i]);
  //   printf("y[%u]: %lu\n", i, (unsigned long)y[i]);
  // }
  delete fpmath;
}

int main(int argc, char **argv) {
  /************* Argument Parsing  ************/
  /********************************************/
  ArgMapping amap;
  amap.arg("r", party, "Role of party: ALICE = 1; BOB = 2");
  amap.arg("p", port, "Port Number");
  amap.arg("N", dim, "Number of exponentiations");
  amap.arg("nt", num_threads, "Number of threads");
  amap.arg("ip", address, "IP Address of server (ALICE)");

  amap.parse(argc, argv);

  assert(num_threads <= MAX_THREADS);

  /********** Setup IO and Base OTs ***********/
  /********************************************/
  for (int i = 0; i < num_threads; i++) {
    iopackArr[i] = new IOPack(party, port + i, address);
    if (i & 1) {
      otpackArr[i] = new OTPack(iopackArr[i], 3 - party);
    } else {
      otpackArr[i] = new OTPack(iopackArr[i], party);
    }
  }
  std::cout << "All Base OTs Done" << std::endl;

  /************ Generate Test Data ************/
  /********************************************/
  PRG128 prg;

  uint64_t *x = new uint64_t[dim];
  uint64_t *y = new uint64_t[dim];

  prg.random_data(x, dim * sizeof(uint64_t));

  if (party == ALICE) {
    iopackArr[0]->io->send_data(x, dim * sizeof(uint64_t));
  } else {
    uint64_t *x0 = new uint64_t[dim];
    iopackArr[0]->io->recv_data(x0, dim * sizeof(uint64_t));
    for (int i = 0; i < dim; i++) {
      // x is in range [-1000, -0.0001]
      // Convert to fixed point: MIN_FIXED to MAX_FIXED
      uint64_t range_size = MIN_FIXED - MAX_FIXED; // from MIN_FIXED to MAX_FIXED
      uint64_t random_val = (x[i] & (mask_x >> 1)) % range_size; // get random value in range
      uint64_t fixed_point_val = MAX_FIXED + random_val; // value from MAX_FIXED to MIN_FIXED
      x[i] = ((1ULL << bw_x) - fixed_point_val) - x0[i]; // make it negative by two's complement
    }
    delete[] x0;
  }
  for (int i = 0; i < dim; i++) {
    x[i] &= mask_x;
  }

  /************** Fork Threads ****************/
  /********************************************/
  uint64_t total_comm = 0;
  std::vector<uint64_t> thread_comm(num_threads);
  for (int i = 0; i < num_threads; i++) {
    thread_comm[i] = iopackArr[i]->get_comm();
  }

  auto start = clock_start();
  std::vector<std::thread> exp_threads(num_threads);
  int chunk_size = dim / num_threads;
  for (int i = 0; i < num_threads; ++i) {
    int offset = i * chunk_size;
    int lnum_exp;
    if (i == (num_threads - 1)) {
      lnum_exp = dim - offset;
    } else {
      lnum_exp = chunk_size;
    }
    exp_threads[i] =
        std::thread(exp4_thread, i, x + offset, y + offset, lnum_exp);
  }
  for (int i = 0; i < num_threads; ++i) {
    exp_threads[i].join();
  }
  long long t = time_from(start);

  for (int i = 0; i < num_threads; i++) {
    thread_comm[i] = iopackArr[i]->get_comm() - thread_comm[i];
    total_comm += thread_comm[i];
  }

  /************** Verification ****************/
  /********************************************/
  if (party == ALICE) {
    iopackArr[0]->io->send_data(x, dim * sizeof(uint64_t));
    iopackArr[0]->io->send_data(y, dim * sizeof(uint64_t));
  } else { // party == BOB
    uint64_t *x0 = new uint64_t[dim];
    uint64_t *y0 = new uint64_t[dim];
    iopackArr[0]->io->recv_data(x0, dim * sizeof(uint64_t));
    iopackArr[0]->io->recv_data(y0, dim * sizeof(uint64_t));

    double total_err = 0.0;
    double max_ULP_err = 0.0;
    for (int i = 0; i < dim; i++) {
      double dbl_x = (local_signed_val(x0[i] + x[i], bw_x)) / double(1LL << s_x);
      double dbl_y = (local_signed_val(y0[i] + y[i], bw_y)) / double(1ULL << s_y);
      double exp_x = exp(dbl_x);
      double err = computeULPErr(dbl_y, exp_x, s_y);
      total_err += err;
      max_ULP_err = std::max(max_ULP_err, err);
    }

    cerr << "Average ULP error: " << fixed << setprecision(6) << total_err / dim << endl;
    cerr << "Max ULP error: " << fixed << setprecision(6) << max_ULP_err << endl;
    cerr << "Number of tests: " << dim << endl;

    delete[] x0;
    delete[] y0;
  }
  cout << "Number of Exp/s:\t" << (double(dim) / t) * 1e6 << std::endl;
  cout << "Exp Time\t" << t / (1000.0) << " ms" << endl;
  cout << "Exp Bytes Sent\t" << total_comm << " bytes" << endl;

  /******************* Cleanup ****************/
  /********************************************/
  delete[] x;
  delete[] y;
  for (int i = 0; i < num_threads; i++) {
    delete iopackArr[i];
    delete otpackArr[i];
  }
}