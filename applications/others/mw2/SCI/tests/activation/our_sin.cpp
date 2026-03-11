#include "LinearOT/linear-ot.h"
#include "utils/emp-tool.h"
#include <cstdint>
#include <cstdio>
#include <iostream>

#include "FloatingPoint/floating-point.h"
#include "FloatingPoint/fp-math.h"
#include <limits>
#include <math.h>
#include <random>
// #include "float_utils.h"
#include "BuildingBlocks/aux-protocols.h"
#include "BuildingBlocks/geometric_perspective_protocols.h"
#include "BuildingBlocks/truncation.h"
#include "Math/math-functions.h"
#include "Millionaire/equality.h"
#include "Millionaire/millionaire.h"
#include "Millionaire/millionaire_with_equality.h"
#include <chrono>
// #include <matplotlibcpp.h>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>

using namespace sci;
using namespace std;
// namespace plt = matplotlibcpp;
// using namespace plt;
int party, port = 32000;
string address = "127.0.0.1";
IOPack *iopack;
OTPack *otpack;
LinearOT *prod;
XTProtocol *ext;

// int bwL = 22;
// uint64_t N = pow(2, bwL);
// uint64_t mask_bwL = (bwL == 64 ? -1 : ((1ULL << bwL) - 1));
bool accumulate = true;
bool precomputed_MSBs = false;
MultMode mode = MultMode::None;

// uint64_t f = 12;

uint64_t f_MW = 28;
uint64_t bwL_MW = f_MW+2;
uint64_t N_f_MW = pow(2, f_MW);
uint64_t N_MW = pow(2, bwL_MW);
uint64_t mask_N_MW = (bwL_MW == 64 ? -1 : ((1ULL << bwL_MW) - 1));
// uint64_t pow_f = pow(2, f);

uint64_t f_input = 16;
int bwL_input = 63;
uint64_t mask_bwL_input = (bwL_input == 64 ? -1 : ((1ULL << bwL_input) - 1));
uint64_t N_input = pow(2, bwL_input);
uint64_t B = 0.5*2*(1ULL << bwL_input)/4;


uint64_t f_output = 16;
uint64_t bwL_output = f_output+10;

Truncation *trunc_oracle;
AuxProtocols *aux;
MillionaireWithEquality *mill_eq;
Equality *eq;
MathFunctions *math;
GeometricPerspectiveProtocols *gp;
// LinearOT *prod;
// int dim = pow(2, 20);
// int dim = 1;
// int dim = 16384;
// int dim = 500;
int dim = (1ULL << 18);
uint64_t acc = 2;
uint64_t init_input = 0;
uint64_t step_size = 1;
uint64_t correct = 1;

void compute_MW_plain(const uint64_t *x0, const uint64_t *x1, uint64_t *MW,
                      size_t len, uint64_t N) {
  for (size_t i = 0; i < len; ++i) {
    uint64_t sum = x0[i] + x1[i];
    if (0 <= sum && sum < N / 2) {
      MW[i] = 0;
    } else if (N / 2 <= sum && sum < 3 * N / 2) {
      MW[i] = 1;
    } else if (3 * N / 2 <= sum && sum < 2 * N) {
      MW[i] = 2;
    } else {
      MW[i] = 3;
    }
  }
}

void ring_exp(const uint64_t *inA, uint64_t *out, size_t len, uint64_t f,
              uint64_t mask_bwL) {
  double pow_f = std::pow(2.0, f);
  for (size_t i = 0; i < len; ++i) {
    double x0_real = static_cast<double>(inA[i]) / pow_f;
    double exp_val = std::exp(x0_real);
    uint64_t exp_fixed =
        static_cast<uint64_t>(std::round(exp_val * pow_f)) & mask_bwL;
    out[i] = exp_fixed;
  }
}

void ring_sin(const uint64_t *inA, uint64_t *out, size_t len, uint64_t f_input,uint64_t f,
              uint64_t mask_bwL) {
  double pow_f = std::pow(2.0, f);
  double pow_f_input = std::pow(2.0, f_input);
  for (size_t i = 0; i < len; ++i) {
    double x0_real = static_cast<double>(inA[i]) / pow_f_input;
    double sin_val = std::sin(x0_real);
    uint64_t sin_fixed =
        static_cast<uint64_t>(std::round(sin_val * pow_f)) & mask_bwL;
    out[i] = sin_fixed;
  }
}

void ring_cos(const uint64_t *inA, uint64_t *out, size_t len, uint64_t f_input,uint64_t f,
              uint64_t mask_bwL) {
  double pow_f = std::pow(2.0, f);
  double pow_f_input = std::pow(2.0, f_input);
  for (size_t i = 0; i < len; ++i) {
    double x0_real = static_cast<double>(inA[i]) / pow_f_input;
    double cos_val = std::cos(x0_real);
    uint64_t cos_fixed =
        static_cast<uint64_t>(std::round(cos_val * pow_f)) & mask_bwL;
    out[i] = cos_fixed;
  }
}

double fix2double(uint64_t x, uint64_t y, uint64_t L, uint64_t f) {
  uint64_t mask = (L == 64) ? ~0ULL : ((1ULL << L) - 1);
  uint64_t sum = (x + y) & mask;
  int64_t signed_val;
  if (sum >= (1ULL << (L - 1))) {
    signed_val = (int64_t)(sum - (1ULL << L));
  } else {
    signed_val = (int64_t)sum;
  }
  return (double)signed_val / (1ULL << f);
}

int64_t sign_extend_l(uint64_t x, int l) {
  uint64_t mask = (1ULL << l) - 1;
  x &= mask;
  if (x & (1ULL << (l - 1)))
      return (int64_t)(x | (~mask));
  else
      return (int64_t)x;
}




int main(int argc, char **argv) {
  ArgMapping amap;

  amap.arg("r", party, "Role of party: ALICE = 1; BOB = 2");
  amap.arg("p", port, "Port Number");
  amap.arg("ip", address, "IP Address of server (ALICE)");
  amap.arg("m", precomputed_MSBs, "MSB_to_Wrap Optimization?");
  amap.arg("a", ::accumulate, "Accumulate?");
  amap.parse(argc, argv);


  iopack = new IOPack(party, port, "127.0.0.1");
  uint64_t *inA = new uint64_t[dim];    // Declare the variable "inA"
  otpack = new OTPack(iopack, party);
  prod = new LinearOT(party, iopack, otpack);
  gp = new GeometricPerspectiveProtocols(party, iopack, otpack);
  aux = new AuxProtocols(party, iopack, otpack);
  ext = new XTProtocol(party, iopack, otpack);
  uint64_t *inB = new uint64_t[dim];  // Declare the variable "inB"
  uint64_t *outC = new uint64_t[dim]; // Declare the variable "inC"

  bool signed_arithmetic = true;
  


  // for (int j = 0; j < 4; j++) {
  //   MW_sin_lut[j] = MW_sin_lut[j] + (1ULL<<(bwL_MW-1));
  //   MW_cos_lut[j] = MW_cos_lut[j] + (1ULL<<(bwL_MW-1));
  // }
  uint64_t *MW = new uint64_t[dim];
  uint64_t *MW_plain = new uint64_t[dim];
  size_t comm_start = iopack->io->counter;
  auto start_time = chrono::high_resolution_clock::now();

  uint seed = 10;
  for (int i = 0; i < dim; i++) {
    // inA[i] = rand() & mask_bwL_input;
    // inB[i] = rand() & mask_bwL_input;

    inA[i] = (rand_r(&seed) & mask_bwL_input) % (B / 2);
    inB[i] = (rand_r(&seed) & mask_bwL_input) % (B / 2); 

    // inA[i] = (rand() & mask_bwL_input) % (B / 2);
    // inB[i] = (rand() & mask_bwL_input) % (B / 2); 

    // inA[i] = ((0 + i * 1) & mask_bwL_input) ;      // ensure inA < B
    // inB[i] = ((init_input + i * 2) & mask_bwL_input); // ensure inB < B
  }
  
  compute_MW_plain(inA, inB, MW_plain, dim, N_input);
  printf("B: %llu\n", B);


  size_t comm_start_mw = iopack->io->counter;
  if (B == N_input/4) {
    if (party == ALICE) {
      gp->mw(dim, inA, MW, bwL_input, 2);
    } else {
      gp->mw(dim, inB, MW, bwL_input, 2);
    }
  } else {
    if (party == ALICE) {
      gp->mwwithB(dim, B, inA, MW, bwL_input, 2);
    } else {
      gp->mwwithB(dim, B, inB, MW, bwL_input, 2);
    }
  }
  size_t comm_end_mw = iopack->io->counter;

  if (party == ALICE) {
    iopack->io->send_data(MW, dim * sizeof(uint64_t));
  }
  else {
    uint64_t *MW_recv = new uint64_t[dim];
    iopack->io->recv_data(MW_recv, dim * sizeof(uint64_t));
    for (int i = 0; i < dim; i++) {
      // if (MW_plain[i] != (MW_recv[i] + MW[i])  & ((1ULL << 2) - 1)) {
      if (MW_plain[i] != ((MW_recv[i] + MW[i]) & ((1ULL << 2) - 1))) {
        printf("inA[%d]: %llu, inB[%d]: %llu\n", i, inA[i], i, inB[i]);
        printf("MW_plain[%d]: %llu, MW_recv[%d]: %llu, MW[%d]: %llu\n", i, MW_plain[i], i, MW_recv[i], i, MW[i]);
        return 0;
      }
      MW[i] = (MW_recv[i] + MW[i])  & ((1ULL << 2) - 1);

    }
    
    delete[] MW_recv;
  }
  // for (int i = 0; i < dim; i++) {
  //   inA[i] = (0 + i * 20 +1048575 ) & mask_bwL_input;
  //   inB[i] = (init_input+1048575 +i * 1111) & mask_bwL_input;
  //   compute_MW_plain(inA, inB, MW, dim, N_input);
  // }

  //step 1: set bitwidth
  uint64_t f_t = 14;
  uint64_t bwL_t = f_t + 2;
  uint64_t mask_bwL_t = (bwL_t == 64 ? -1 : ((1ULL << bwL_t) - 1));
  uint64_t f_T = 30;
  uint64_t bwL_T = f_T + 2;
  uint64_t mask_bwL_T = (bwL_T == 64 ? -1 : ((1ULL << bwL_T) - 1));
  uint64_t N_f_T = pow(2, f_T);
  uint64_t N_bwL_T_minus_1 = pow(2, bwL_T-1);

  uint64_t N_2f_t_f_T = pow(2, 2*f_t+f_T);
  uint64_t mask_2bwL_t_bwL_T_lut = (2*bwL_t+bwL_T == 64 ? -1 : ((1ULL << (2*bwL_t+bwL_T)) - 1));
  uint64_t *MW_sin_lut = new uint64_t[4];
  uint64_t *MW_cos_lut = new uint64_t[4];
  uint64_t *MW_exp = new uint64_t[dim];
  uint64_t *exp_inA = new uint64_t[dim];
  uint64_t *exp_inB = new uint64_t[dim];
  uint64_t *res_exp = new uint64_t[dim];
  uint64_t N_t_input = pow(2, bwL_t);
  for (int i = 0; i < 3; i++) {
    double pow_f_input = std::pow(2.0, f_input);
    double pow_f = std::pow(2.0, f_T);
    double angle = -i * static_cast<double>(N_input) / pow_f_input;
    double sin_val = std::sin(angle);
    double cos_val = std::cos(angle);
    printf("sin_val: %f\n", sin_val);
    printf("cos_val: %f\n", cos_val);
    MW_sin_lut[i] = static_cast<uint64_t>(std::round(sin_val * N_f_T)) & mask_bwL_T;
    MW_cos_lut[i] = static_cast<uint64_t>(std::round(cos_val * N_f_T)) & mask_bwL_T;
    
    // MW_sin_lut[i] = static_cast<uint64_t>(std::round(sin_val * N_2f_t_f_T)) & mask_2bwL_t_bwL_T_lut;
    // MW_cos_lut[i] = static_cast<uint64_t>(std::round(cos_val * N_2f_t_f_T)) & mask_2bwL_t_bwL_T_lut;
    if (MW_sin_lut[i] <=  N_bwL_T_minus_1) {
      MW_sin_lut[i] = MW_sin_lut[i] * (1ULL<<(f_t*2));
    }
    else {
      MW_sin_lut[i] = (1ULL<<(bwL_T+bwL_t*2 )) - (2*N_bwL_T_minus_1-MW_sin_lut[i]) * (1ULL<<(f_t*2));
    }
    if (MW_cos_lut[i] <=  N_bwL_T_minus_1) {
      MW_cos_lut[i] = MW_cos_lut[i] * (1ULL<<(f_t*2));
    }
    else {
      MW_cos_lut[i] = (1ULL<<(bwL_T+bwL_t*2 )) - (2*N_bwL_T_minus_1-MW_cos_lut[i]) * (1ULL<<(f_t*2));
    }


    printf("MW_sin_lut[%d]: %llu\n", i, MW_sin_lut[i]);
    printf("MW_cos_lut[%d]: %llu\n", i, MW_cos_lut[i]);
  }

  printf("N_2f_t_f_T: %llu\n", N_2f_t_f_T);
  printf("mask_2bwL_t_bwL_T_lut: %llu\n", mask_2bwL_t_bwL_T_lut);

  MW_sin_lut[3] = 100;
  MW_cos_lut[3] = 100;
  //step 2: compute sin and cos
  uint64_t *sin_inA = new uint64_t[dim];
  uint64_t *cos_inA = new uint64_t[dim];
  uint64_t *sin_inB = new uint64_t[dim];
  uint64_t *cos_inB = new uint64_t[dim];
  if (party == ALICE) {
      ring_sin(inA, sin_inA, dim, f_input,f_t, mask_bwL_t);
      ring_cos(inA, cos_inA, dim, f_input,f_t, mask_bwL_t);
  } else {
    ring_sin(inB, sin_inB, dim, f_input,f_t, mask_bwL_t);
    ring_cos(inB, cos_inB, dim, f_input,f_t, mask_bwL_t);
  }

  //step3: postive  sin cos

  // if (party == ALICE) {
  //   for (int i = 0; i < dim; i++) {
  //     sin_inA[i] = sin_inA[i] + (1ULL<<(f_t - 1));
  //     cos_inA[i] = cos_inA[i] + (1ULL<<(f_t - 1));
  //   }
  // } else {
  //   for (int i = 0; i < dim; i++) {
  //     sin_inB[i] = sin_inB[i] + (1ULL<<(f_t - 1));
  //     cos_inB[i] = cos_inB[i] + (1ULL<<(f_t - 1));
  //   }
  // }





  // if (party == ALICE) {
  // for (int i = 0; i < dim; i++) {
  //   printf("inA[%d]: %llu\n", i, inA[i]);
  //   printf("sin_inA[%d]: %llu\n", i, sin_inA[i]);
  //   printf("cos_inA[%d]: %llu\n", i, cos_inA[i]);
  // }
  // } else {
  //   for (int i = 0; i < dim; i++) {
  //     printf("inB[%d]: %llu\n", i, inB[i]);
  //     printf("sin_inB[%d]: %llu\n", i, sin_inB[i]);
  //     printf("cos_inB[%d]: %llu\n", i, cos_inB[i]);
  //   }
  // }


  //step 4: compute sin_inA_cos_inB, cos_inA_sin_inB, cos_inA_cos_inB, sin_inA_sin_inB
  uint64_t *sin_inA_cos_inB = new uint64_t[dim];
  uint64_t *cos_inA_sin_inB = new uint64_t[dim];
  uint64_t *cos_inA_cos_inB = new uint64_t[dim];
  uint64_t *sin_inA_sin_inB = new uint64_t[dim];
  uint64_t mask_2bwL_t = (2*bwL_t == 64 ? -1 : ((1ULL << (2*bwL_t)) - 1));
  uint64_t *zero = new uint64_t[dim];
  for (int i = 0; i < dim; i++) {
    zero[i] = 0;
  }

  size_t had_comm_start = iopack->io->counter;

  if (party == ALICE)
  {
    for (int i = 0; i < dim; i++) {
      sin_inA[i] = (sin_inA[i] + (1ULL << f_t)) & mask_bwL_t;
      cos_inA[i] = (cos_inA[i] + (1ULL << f_t)) & mask_bwL_t;
    }
  }
  else {
    for (int i = 0; i < dim; i++) {
      sin_inB[i] = (sin_inB[i] + (1ULL << f_t)) & mask_bwL_t;
      cos_inB[i] = (cos_inB[i] + (1ULL << f_t)) & mask_bwL_t;
    }
  }

  if (party == ALICE)
  {
    gp->cross_term (dim, sin_inA, zero, sin_inA_cos_inB, bwL_t, bwL_t,
      bwL_t+bwL_t);
    gp->cross_term (dim, cos_inA, zero, cos_inA_sin_inB, bwL_t, bwL_t,
        bwL_t+bwL_t);
    gp->cross_term (dim, cos_inA, zero, cos_inA_cos_inB, bwL_t, bwL_t,
          bwL_t+bwL_t);
    gp->cross_term (dim, sin_inA, zero, sin_inA_sin_inB, bwL_t, bwL_t,
            bwL_t+bwL_t);
  }
  else {
    gp->cross_term (dim, zero, cos_inB, sin_inA_cos_inB, bwL_t, bwL_t,
      bwL_t+bwL_t);
    gp->cross_term (dim, zero, sin_inB, cos_inA_sin_inB, bwL_t, bwL_t,
        bwL_t+bwL_t);
    gp->cross_term (dim, zero, cos_inB, cos_inA_cos_inB, bwL_t, bwL_t,
          bwL_t+bwL_t);
    gp->cross_term (dim, zero, sin_inB, sin_inA_sin_inB, bwL_t, bwL_t,
            bwL_t+bwL_t);
  }


  // for (int i = 0; i < 100; i++) {
  //   printf("\n");
  //   if (party == ALICE) {
  //     printf("111111");
  //     printf("sin_inA[%d]: %llu\n", i, sin_inA[i]);
  //     printf("cos_inA[%d]: %llu\n", i, cos_inA[i]);
  //     printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
  //     printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
  //     printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
  //     printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
  //     printf("\n");
  //   } else {
  //     printf("111111");
  //     printf("sin_inB[%d]: %llu\n", i, sin_inB[i]);
  //     printf("cos_inB[%d]: %llu\n", i, cos_inB[i]);
  //     printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
  //     printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
  //     printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
  //     printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
  //     printf("\n");
  //   }
  // }
  


  if (party == ALICE)
  {
    for (int i = 0; i < dim; i++) {
      sin_inA_cos_inB[i] = (sin_inA_cos_inB[i] - (sin_inA[i] ) * (1ULL << f_t) + (1ULL << 2*f_t)) & mask_2bwL_t;
      cos_inA_sin_inB[i] = (cos_inA_sin_inB[i] - (cos_inA[i] ) * (1ULL << f_t) + (1ULL << 2*f_t)) & mask_2bwL_t;
      cos_inA_cos_inB[i] = (cos_inA_cos_inB[i] - (cos_inA[i] ) * (1ULL << f_t) + (1ULL << 2*f_t)) & mask_2bwL_t;
      sin_inA_sin_inB[i] = (sin_inA_sin_inB[i] - (sin_inA[i] ) * (1ULL << f_t) + (1ULL << 2*f_t)) & mask_2bwL_t;
    }
  }
  else {
    for (int i = 0; i < dim; i++) {
      sin_inA_cos_inB[i] = (sin_inA_cos_inB[i] - (cos_inB[i] ) * (1ULL << f_t)) & mask_2bwL_t;
      cos_inA_sin_inB[i] = (cos_inA_sin_inB[i] - (sin_inB[i] ) * (1ULL << f_t)) & mask_2bwL_t;
      cos_inA_cos_inB[i] = (cos_inA_cos_inB[i] - (cos_inB[i] ) * (1ULL << f_t)) & mask_2bwL_t;
      sin_inA_sin_inB[i] = (sin_inA_sin_inB[i] - (sin_inB[i] ) * (1ULL << f_t)) & mask_2bwL_t;
    }
  }


  for (int i = 0; i < 100; i++) {
    printf("\n");
    if (party == ALICE) {
      printf("222222\t");
      printf("dim \t%d\n", dim);
      printf("sin_inA[%d]: %llu\n", i, sin_inA[i]);
      printf("cos_inA[%d]: %llu\n", i, cos_inA[i]);
      printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
      printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
      printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
      printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
      printf("\n");
    } else {
      printf("222222\t");
      printf("dim \t%d\n", dim);
      printf("sin_inB[%d]: %llu\n", i, sin_inB[i]);
      printf("cos_inB[%d]: %llu\n", i, cos_inB[i]);
      printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
      printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
      printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
      printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
      printf("\n");
    }
  }
  

  // if (party == ALICE) {
  //   prod->hadamard_product(dim, sin_inA, zero, sin_inA_cos_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, cos_inA, zero, cos_inA_sin_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, cos_inA, zero, cos_inA_cos_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, sin_inA, zero, sin_inA_sin_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  // } else {
  //   prod->hadamard_product(dim, zero, cos_inB, sin_inA_cos_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, zero, sin_inB, cos_inA_sin_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, zero, cos_inB, cos_inA_cos_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  //   prod->hadamard_product(dim, zero, sin_inB, sin_inA_sin_inB, bwL_t, bwL_t, bwL_t+bwL_t, true, true, MultMode::Alice_has_A);
  // }
  size_t had_comm_end = iopack->io->counter;
  
  // for (int i = 0; i < 100; i++) {
  //   printf("\n");
  //   if (party == ALICE) {
  //     printf("sin_inA[%d]: %llu\n", i, sin_inA[i]);
  //     printf("cos_inA[%d]: %llu\n", i, cos_inA[i]);
  //     printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
  //     printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
  //     printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
  //     printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
  //   } else {
  //     printf("sin_inB[%d]: %llu\n", i, sin_inB[i]);
  //     printf("cos_inB[%d]: %llu\n", i, cos_inB[i]);
  //     printf("sin_inA_cos_inB[%d]: %llu\n", i, sin_inA_cos_inB[i]);
  //     printf("cos_inA_sin_inB[%d]: %llu\n", i, cos_inA_sin_inB[i]);
  //     printf("cos_inA_cos_inB[%d]: %llu\n", i, cos_inA_cos_inB[i]);
  //     printf("sin_inA_sin_inB[%d]: %llu\n", i, sin_inA_sin_inB[i]);
  //   }
  // }

  uint64_t *sc_add_cs_lut_buffer = new uint64_t[dim * 4];
  uint64_t *cc_min_ss_lut_buffer = new uint64_t[dim * 4];
  uint64_t mask_2bwL_t_bwL_T = (2*bwL_t+bwL_T == 64 ? -1 : ((1ULL << (2*bwL_t+bwL_T)) - 1));

  size_t comm_start_sextend_1 = iopack->io->counter;
  //step 14: compute select table
  uint64_t *sc_add_cs = new uint64_t[dim];
  uint64_t *cc_min_ss = new uint64_t[dim];
  uint64_t *sc_add_cs_lut = new uint64_t[dim];
  uint64_t *cc_min_ss_lut = new uint64_t[dim];
  for (int j = 0; j < dim; j++) {
    sc_add_cs[j] = (sin_inA_cos_inB[j] + cos_inA_sin_inB[j]) & mask_2bwL_t;
    cc_min_ss[j] = (cos_inA_cos_inB[j] - sin_inA_sin_inB[j]) & mask_2bwL_t;
  }

  uint64_t *ext_sc_add_cs = new uint64_t[dim];
  uint64_t *ext_cc_min_ss = new uint64_t[dim];
  for (int j = 0; j < dim; j++) {
    ext_sc_add_cs[j] = 0;
    ext_cc_min_ss[j] = 0;
  }
  uint8_t *msb0 = new uint8_t[dim];
  for (int j = 0; j < dim; j++) {
    msb0[j] = 0;
  }
  for (int j = 0; j < dim; j++) {
    sc_add_cs[j] = (sc_add_cs[j] + (1ULL<<(2*f_t )))  & mask_2bwL_t;
    cc_min_ss[j] = (cc_min_ss[j] + (1ULL<<(2*f_t )))  & mask_2bwL_t;
  }
  ext->s_extend(dim, sc_add_cs, ext_sc_add_cs, 2*bwL_t, 2*bwL_t + bwL_T, msb0);
  ext->s_extend(dim, cc_min_ss, ext_cc_min_ss, 2*bwL_t, 2*bwL_t + bwL_T, msb0);
  
  for (int i = 0; i < 4; i++) {

    for (int j = 0; j < dim; j++) {
      ext_sc_add_cs[j] = (ext_sc_add_cs[j] * (1ULL<<(f_T ))- (1ULL<<(2*f_t + f_T))) & mask_2bwL_t_bwL_T;
      ext_cc_min_ss[j] = (ext_cc_min_ss[j] * (1ULL<<(f_T ))- (1ULL<<(2*f_t + f_T))) & mask_2bwL_t_bwL_T;
    }
    if (party == ALICE) {
    for (int j = 0; j < dim; j++) {
      __uint128_t prod = ((__uint128_t)ext_sc_add_cs[j] * (__uint128_t)MW_cos_lut[i]) ;
      sc_add_cs_lut[j] = ((prod ) >> (2*f_t + f_T)) & mask_2bwL_t_bwL_T;
      __uint128_t prod2 = ((__uint128_t)ext_cc_min_ss[j] * (__uint128_t)MW_sin_lut[i]) ;
      cc_min_ss_lut[j] = ((prod2 ) >> (2*f_t + f_T)) & mask_2bwL_t_bwL_T;
    }
  }
  else {
    for (int j = 0; j < dim; j++) {
      __uint128_t prod = ((__uint128_t)ext_sc_add_cs[j] * (__uint128_t)MW_cos_lut[i]) ;
      sc_add_cs_lut[j] = ((prod ) >> (2*f_t + f_T)) & mask_2bwL_t_bwL_T;
      __uint128_t prod2 = ((__uint128_t)ext_cc_min_ss[j] * (__uint128_t)MW_sin_lut[i]) ;
      cc_min_ss_lut[j] = ((prod2 ) >> (2*f_t + f_T)) & mask_2bwL_t_bwL_T;
    }
  }
  


    // for (int j = 0; j < 100; j++) {
    //   printf("sc_add_cs[%d][%d]: %llu\n", i, j, sc_add_cs[j]);
    //   printf("cc_min_ss[%d][%d]: %llu\n", i, j, cc_min_ss[j]);
    //   printf("MW_cos_lut[%d]: %llu\n", i, MW_cos_lut[i]);
    //   printf("MW_sin_lut[%d]: %llu\n", i, MW_sin_lut[i]);
    //   printf("ext_sc_add_cs[%d][%d]: %llu\n", i, j, ext_sc_add_cs[j]);
    //   printf("ext_cc_min_ss[%d][%d]: %llu\n", i, j, ext_cc_min_ss[j]);
    //   // printf("MW_cos_lut_extend[%d][%d]: %llu\n", i, j, MW_cos_lut_extend[j]);
    //   // printf("MW_sin_lut_extend[%d][%d]: %llu\n", i, j, MW_sin_lut_extend[j]);
    //   printf("sc_add_cs_lut[%d][%d]: %llu\n", i, j, sc_add_cs_lut[j]);
    //   printf("cc_min_ss_lut[%d][%d]: %llu\n", i, j, cc_min_ss_lut[j]);
      
    // }
    
    for (int j = 0; j < dim; j++) {
      sc_add_cs_lut_buffer[i * dim + j] = sc_add_cs_lut[j];
      cc_min_ss_lut_buffer[i * dim + j] = cc_min_ss_lut[j];
    }
  }
  size_t comm_end_sextend_1 = iopack->io->counter;

  //step 16: send lut buffer to bob
  size_t comm_start_lut = iopack->io->counter;
  uint64_t *sc_add_cs_lut_buffer_recv = new uint64_t[dim * 4];
  uint64_t *cc_min_ss_lut_buffer_recv = new uint64_t[dim * 4];
  
  if (party != ALICE) {
    iopack->io->send_data(sc_add_cs_lut_buffer, dim * 4 * sizeof(uint64_t));
    iopack->io->send_data(cc_min_ss_lut_buffer, dim * 4 * sizeof(uint64_t));
  } else {
    iopack->io->recv_data(sc_add_cs_lut_buffer_recv, dim * 4 * sizeof(uint64_t));
    iopack->io->recv_data(cc_min_ss_lut_buffer_recv, dim * 4 * sizeof(uint64_t));
    for (int i = 0; i < dim; i++) {
      for (int j = 0; j < 4; j++) {
        sc_add_cs_lut_buffer[i * 4 + j] = (sc_add_cs_lut_buffer[i * 4 + j] + sc_add_cs_lut_buffer_recv[i * 4 + j]) & mask_2bwL_t_bwL_T;
        cc_min_ss_lut_buffer[i * 4 + j] = (cc_min_ss_lut_buffer[i * 4 + j] + cc_min_ss_lut_buffer_recv[i * 4 + j]) & mask_2bwL_t_bwL_T;
      }
    }
  }
  
  

  // uint64_t *temp0 = new uint64_t[dim];
  // uint64_t *temp1 = new uint64_t[dim];
  uint64_t *T_add_T = new uint64_t[dim];
  if (party == ALICE) {
    uint64_t **sc_cs_lut_spec = new uint64_t *[dim];
    // uint64_t **cc_ss_lut_spec = new uint64_t *[dim];
    for (int i = 0; i < dim; i++) {
      sc_cs_lut_spec[i] = new uint64_t[4];
      // cc_ss_lut_spec[i] = new uint64_t[4];
      for (int j = 0; j < 4; j++) {
        sc_cs_lut_spec[i][j] = (sc_add_cs_lut_buffer[j * dim + i] + cc_min_ss_lut_buffer[j * dim + i]) & mask_2bwL_t_bwL_T;
        // cc_ss_lut_spec[i][j] = ;
      }
    }
    aux->lookup_table<uint64_t>(sc_cs_lut_spec, nullptr, nullptr, dim, 2, 2*bwL_t+bwL_T);
    // aux->lookup_table<uint64_t>(cc_ss_lut_spec, nullptr, nullptr, dim, 2, 2*bwL_t+bwL_T);
  }
  else {
    aux->lookup_table<uint64_t>(nullptr, MW, T_add_T, dim, 2,2*bwL_t+bwL_T);

  }
  size_t comm_end_lut = iopack->io->counter;

  uint64_t *T_add_T_reduce = new uint64_t[dim];
  for (int i = 0; i < dim; i++) {
    T_add_T_reduce[i] = T_add_T[i] >> (2*f_t+f_T-f_output);
  }

  uint64_t mask_5_f_output = (1ULL << (f_output+5)) - 1;
  for (int i = 0; i < dim; i++) {
    T_add_T_reduce[i] =( T_add_T_reduce[i] + (1ULL<<(f_output -1))) & mask_5_f_output;
  }
  // uint8_t *msb0 = new uint8_t[dim];
  // for (int j = 0; j < dim; j++) {
  //   msb0[j] = 0;
  // }
  size_t comm_start_sextend_2 = iopack->io->counter;
  ext->s_extend(dim, T_add_T_reduce, res_exp, f_output+5, bwL_output, msb0);
  size_t comm_end_sextend_2 = iopack->io->counter;

  uint64_t mask_output = (1ULL << (bwL_output)) - 1;
  for (int i = 0; i < dim; i++) {
    res_exp[i] = (res_exp[i] - (1ULL<<(f_output -1))) & mask_output;
  }

  size_t comm_end = iopack->io->counter;
  size_t comm_bytes = comm_end - comm_start;
  auto end_time = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);

  uint64_t *res_exp_alice = new uint64_t[dim];
    if (party == ALICE) {
        iopack->io->send_data(res_exp, dim * sizeof(uint64_t));
    } else {
        iopack->io->recv_data(res_exp_alice, dim * sizeof(uint64_t));
    }
    double *res_sin_plain = new double[dim];
    double *ideal_exp_plain = new double[dim];
    double ulp = 1.0 / (1 << f_output); 
    uint64_t mask_MWlut_outC = (1ULL << bwL_output) - 1;
    for (int i = 0; i < dim; i++) {
        // res_sin_plain[i] = static_cast<double>((res_exp_alice[i] + res_exp[i]) & mask_MWlut_outC) / std::pow(2, f_output);
        res_sin_plain[i] = fix2double(res_exp_alice[i], res_exp[i], bwL_output, f_output);
        ideal_exp_plain[i] = std::sin(fix2double(inA[i], inB[i], bwL_input, f_input));
        // printf("inA[%u]: %u\n", i, inA[i]);
        // printf("inB[%u]: %u\n", i, inB[i]);
        // printf("MW[%d]: %d\n", i, MW[i]);
        // printf("res_exp_alice[%d]: %llu\n", i, res_exp_alice[i]);
        // printf("res_exp[%d]: %llu\n", i, res_exp[i]);
        // printf("res_sin_plain[%d]: %.10f\n", i, res_sin_plain[i]);
        // printf("fix2double(inA[%d], inB[%d], bwL_input, f_input): %f\n", i, i, fix2double(inA[i], inB[i], bwL_input, f_input));
        // printf("ideal_exp_plain[%d]: %.10f\n", i, ideal_exp_plain[i]);
        if ( i < 100 ) {
          double error = fabs(ideal_exp_plain[i] - res_sin_plain[i]);
          printf("ULP [%d]: %.6f\n", i, error / ulp);
          printf("Error [%d]: %.6f\n", i, error);
        }
    }
    for (int i = 0; i < 4; i++) {
        printf("MW_cos_lut[%d]: %llu\n", i, MW_cos_lut[i]);
        printf("MW_sin_lut[%d]: %llu\n", i, MW_sin_lut[i]);
    }
    double error_sum = 0.0;
    double ulp_sum = 0.0;
    double ulp_max = 0.0;
    for (int i = 0; i < dim; i++) {
      double ulp = 1.0 / (1 << f_output); 
      double error = std::abs(res_sin_plain[i] - ideal_exp_plain[i]);
      error_sum += error;
      ulp_sum += error / ulp;
      ulp_max = std::max(ulp_max, error / ulp);
  }
  printf("Communication: %zu bytes\n", comm_bytes);
  printf("Hadamard Communication: %zu bytes\n", had_comm_end - had_comm_start);
  printf("Sextend 1 Communication: %zu bytes\n", comm_end_sextend_1 - comm_start_sextend_1);
  printf("MW Communication: %zu bytes\n", comm_end_mw - comm_start_mw);
  printf("LUT Communication: %zu bytes\n", comm_end_lut - comm_start_lut);
  printf("Sextend 2 Communication: %zu bytes\n", comm_end_sextend_2 - comm_start_sextend_2);
  printf("Computation time: %ld ms\n", duration.count());
  printf("Average error: %f\n", error_sum / dim);
  printf("ULP avg: %f\n", ulp_sum / dim);
  printf("ULP max: %f\n", ulp_max);

  delete prod;
  delete[] inA; // Delete the variable "inA" to avoid memory leaks
  delete[] inB;
}