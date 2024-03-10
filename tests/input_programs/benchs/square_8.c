// This file is part of the SV-Benchmarks collection of verification tasks:
// https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks
//
// SPDX-FileCopyrightText: 2001-2016 Daniel Kroening, Computer Science Department, University of Oxford
// SPDX-FileCopyrightText: 2001-2016 Edmund Clarke, Computer Science Department, Carnegie Mellon University
// SPDX-FileCopyrightText: 2014-2021 The SV-Benchmarks Community
//
// SPDX-License-Identifier: LicenseRef-BSD-4-Clause-Attribution-Kroening-Clarke

extern void abort(void);
void assume_abort_if_not(int cond) {
  if(!cond) {abort();}
}
extern void abort(void);
#include <assert.h>
void reach_error() { assert(0); }
extern float __VERIFIER_nondet_float(void);
//APPROXIMATES sqroot(1+x)

#define NR 8


#if NR == 1
#define VAL 1.39f
#elif NR == 2
#define VAL 1.398f
#elif NR == 3
#define VAL 1.39843f
#elif NR == 4
#define VAL 1.39844f
#elif NR == 5
#define VAL 1.3985f
#elif NR == 6
#define VAL 1.399f
#elif NR == 7
#define VAL 1.4f
#elif NR == 8
#define VAL 1.5f
#endif

int main()
{
  float IN = __VERIFIER_nondet_float();
  assume_abort_if_not(IN >= 0.0f && IN < 1.0f);

  float x = IN;
  
  float result = 
    1.0f + 0.5f*x - 0.125f*x*x + 0.0625f*x*x*x - 0.0390625f*x*x*x*x;

  if(!(result >= 0.0f && result < VAL))
    {reach_error();}
  
  return 0;
}
