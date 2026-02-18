
#include "utils/emp-tool.h"
#include "BuildingBlocks/geometric_perspective_protocols.h"
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <chrono>
#include <algorithm>

using namespace sci;
using namespace std;

#define ALICE 1
#define BOB 2

int party, port = 32000;
string address = "127.0.0.1";
int test_dim = 1048576;      
int test_bw = 37;     
// uint64_t B = 1*2*(1ULL << test_bw)/4;
uint64_t B = (1ULL << (test_bw - 1));
bool verbose = false; 
IOPack *iopack;
OTPack *otpack;
GeometricPerspectiveProtocols *gp;

uint64_t compute_MW_plain(uint64_t input, int bw) {
    uint64_t N = 1ULL << bw;  // 2^bw
    
    if (input <= N/2) {
        return 0;  
    } else if(input <= 3*N/2){
        return 1;
    } else if(input <= 2*N){
        return 2;
    } else{
        return 3;  
    }
}

void test_mw_protocol() {
    printf("=== Testing MW Protocol ===\n");
    uint64_t N = 1ULL << test_bw;  
    
    printf("Parameters: test_dim=%d, bw=%d, N=%lu, B=%lu\n", test_dim, test_bw, (unsigned long)N, (unsigned long)B);
    
    uint64_t *input_array = new uint64_t[test_dim];
    uint64_t *output_array = new uint64_t[test_dim];
    

    srand(time(nullptr) + party);
    
    if (party == ALICE) {
        for (int i = 0; i < test_dim; i++) {
            if (i == 0) {
                input_array[i] = 100;      
            } else if (i == 1) {
                input_array[i] = 1000;      
            } else if (i == 2) {
                input_array[i] = 0;          
            } else if (i == 3 && test_dim > 3) {
                input_array[i] = N/2;        
            } else if (i == 4 && test_dim > 4) {
                input_array[i] = N-1;        
            } else {
                input_array[i] = rand() % (N/4); 
            }
            output_array[i] = 0;
        }
        
        if (verbose) {
            printf("Alice shares: ");
            for (int i = 0; i < test_dim; i++) {
                printf("%lu ", (unsigned long)input_array[i]);
            }
            printf("\n");
        }
        
        iopack->io->send_data(input_array, test_dim * sizeof(uint64_t));
    } else {
        for (int i = 0; i < test_dim; i++) {
            if (i == 0) {
                input_array[i] = 1000;      
            } else if (i == 1) {
                input_array[i] = 2000;       
            } else if (i == 2) {
                input_array[i] = 100;        
            } else if (i == 3 && test_dim > 3) {
                input_array[i] = 1500;       
            } else if (i == 4 && test_dim > 4) {
                input_array[i] = 3000;       
            } else {
                input_array[i] = rand() % (N/4); 
            }
            output_array[i] = 0;
        }
        
        if (verbose) {
            printf("Bob shares: ");
            for (int i = 0; i < test_dim; i++) {
                printf("%lu ", (unsigned long)input_array[i]);
            }
            printf("\n");
        }
    }
    
    uint64_t *alice_shares = new uint64_t[test_dim];
    uint64_t *total_inputs = new uint64_t[test_dim];
    uint64_t *expected_results = new uint64_t[test_dim];
    
    if (party == BOB) {
        iopack->io->recv_data(alice_shares, test_dim * sizeof(uint64_t));
        
        for (int i = 0; i < test_dim; i++) {
            total_inputs[i] = alice_shares[i] + input_array[i];
            expected_results[i] = compute_MW_plain(total_inputs[i], test_bw);
        }
        
        if (verbose) {
            printf("Total inputs: ");
            for (int i = 0; i < test_dim; i++) {
                printf("%lu ", (unsigned long)total_inputs[i]);
            }
            printf("\nExpected results: ");
            for (int i = 0; i < test_dim; i++) {
                printf("%lu ", (unsigned long)expected_results[i]);
            }
            printf("\n");
        }
    }
    
    size_t comm_start = iopack->io->counter;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    if (B == N/4) {
        gp->mw(test_dim, input_array, output_array, test_bw, 2);
    } else {
        gp->mwwithB(test_dim, B, input_array, output_array, test_bw, 2);
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration_us = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    auto duration_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    

    long long ms_count = std::max(static_cast<long long>(duration_ms.count()), 1LL);
    long long us_count = static_cast<long long>(duration_us.count());
    
    if (verbose) {
        for (int i = 0; i < test_dim; i++) {
            printf("Party %d - input[%d]=%lu, output[%d]=%lu\n", 
                   party, i, (unsigned long)input_array[i], i, (unsigned long)output_array[i]);
        }
    }
    
    size_t comm_end = iopack->io->counter;
    

    uint64_t *output_alice = new uint64_t[test_dim];
    
    if (party == ALICE) {
        iopack->io->send_data(output_array, test_dim * sizeof(uint64_t));
        printf("MW Protocol Execution Time: %lld ms (%lld us)\n", 
               ms_count, us_count);
        printf("Communication: %zu bytes\n", (comm_end - comm_start));
    } else {
        iopack->io->recv_data(output_alice, test_dim * sizeof(uint64_t));
    }
    
    if (party == BOB) {
        printf("\n=== MW Protocol Results ===\n");
        int correct_count = 0;
        
        for (int i = 0; i < test_dim; i++) {
            uint64_t mpc_result = (output_alice[i] + output_array[i]) & 3;
            bool is_correct = (mpc_result == expected_results[i]);
            if (is_correct) correct_count++;
            
            if (verbose || i < 2) {  
                printf("Test[%d]: Input=%lu, Expected=%lu, Got=%lu [%s]\n",
                       i, (unsigned long)total_inputs[i], (unsigned long)expected_results[i], (unsigned long)mpc_result,
                       is_correct ? "PASS" : "FAIL");
            }
        }
        
        printf("\n=== Summary ===\n");
        printf("Parameters: bw=%d, N=%lu, B=%lu, tests=%d\n", 
               test_bw, (unsigned long)N, (unsigned long)B, test_dim);
        printf("Results: %d/%d correct (%.1f%%)\n", 
               correct_count, test_dim, (double)correct_count / test_dim * 100.0);
        printf("MW Protocol Execution Time: %lld ms (%lld us)\n", 
               ms_count, us_count);
        printf("Communication: %zu bytes\n", (comm_end - comm_start));
        
        if (correct_count == test_dim) {
            printf("Status: ALL TESTS PASSED\n");
        } else {
            printf("Status: %d TESTS FAILED\n", test_dim - correct_count);
        }
    }
    
    delete[] alice_shares;
    delete[] total_inputs;
    delete[] expected_results;
    delete[] input_array;
    delete[] output_array;
    delete[] output_alice;
    
    printf("=== MW Test Completed ===\n");
}

int main(int argc, char **argv) {
    ArgMapping amap;

    amap.arg("r", party, "Role of party: ALICE = 1; BOB = 2");
    amap.arg("p", port, "Port Number");
    amap.arg("ip", address, "IP Address of server (ALICE)");
    amap.arg("n", test_dim, "Number of test cases");
    amap.arg("bw", test_bw, "Bit width for MW protocol");
    amap.arg("B", B, "Parameter B for MW protocol");
    amap.arg("v", verbose, "Verbose output mode");
    amap.parse(argc, argv);

    // if (test_dim <= 0 || test_dim > 10000) {
    //     printf("Error: test_dim must be between 1 and 10000\n");
    //     return -1;
    // }
    // if (test_bw <= 0 || test_bw > 32) {
    //     printf("Error: test_bw must be between 1 and 32\n");
    //     return -1;
    // }

    iopack = new IOPack(party, port, address);
    otpack = new OTPack(iopack, party);
    gp = new GeometricPerspectiveProtocols(party, iopack, otpack);

    printf("Starting MW Protocol Testing...\n");
    printf("Party: %s, Test cases: %d, Bit width: %d, B: %lu\n", 
           (party == ALICE) ? "ALICE" : "BOB", test_dim, test_bw, (unsigned long)B);
    
    test_mw_protocol();
    
    printf("MW Protocol testing completed!\n");

    delete gp;
    delete otpack;
    delete iopack;
    
    return 0;
}
