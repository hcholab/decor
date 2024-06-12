CBMC version 5.95.1 (cbmc-5.95.1) 64-bit arm64 macos
Parsing program.unsigned.c
Converting
Type-checking program.unsigned
Generating GOTO Program
Adding CPROVER library (arm64)
Removal of function pointers and virtual functions
Generic Property Instrumentation
Running with 8 object bits, 56 offset bits (default)
Starting Bounded Model Checking
Runtime Symex: 0.000776541s
size of program expression: 33 steps
simple slicing removed 0 assignments
Generated 0 VCC(s), 0 remaining after simplification
Runtime Postprocess Equation: 5.5e-06s

Program constraints:
// 14 
// 14 
// 0 file <built-in-additions> line 8
(1) SHARED_WRITE(__CPROVER_dead_object#1)
// 0 file <built-in-additions> line 8
(2) __CPROVER_dead_object#1 == NULL
// 1 file <built-in-additions> line 7
(3) SHARED_WRITE(__CPROVER_deallocated#1)
// 1 file <built-in-additions> line 7
(4) __CPROVER_deallocated#1 == NULL
// 2 file <built-in-additions> line 12
(5) SHARED_WRITE(__CPROVER_max_malloc_size#1)
// 2 file <built-in-additions> line 12
(6) __CPROVER_max_malloc_size#1 == 36028797018963968ul
// 3 file <built-in-additions> line 9
(7) SHARED_WRITE(__CPROVER_memory_leak#1)
// 3 file <built-in-additions> line 9
(8) __CPROVER_memory_leak#1 == NULL
// 4 file <built-in-additions> line 16
(9) __CPROVER_rounding_mode!0#1 == 0
// 5 
// 15 file program.unsigned.c line 1 function program
// 16 file program.unsigned.c line 1 function program
(10) x!0@1#2 == nondet_symbol<unsigned int>(symex::nondet0)
// 17 file program.unsigned.c line 1 function program
// 18 file program.unsigned.c line 1 function program
// 19 file program.unsigned.c line 1 function program
(11) y!0@1#2 == nondet_symbol<unsigned int>(symex::nondet1)
// 20 file program.unsigned.c line 1 function program
// 21 file program.unsigned.c line 1
// 21 file program.unsigned.c line 1
// 21 file program.unsigned.c line 1
(12) x!0@1#1 == x!0@1#2
// 21 file program.unsigned.c line 1
(13) y!0@1#1 == y!0@1#2
// 6 file program.unsigned.c line 2 function program
// 6 file program.unsigned.c line 2 function program
(14) \guard#1 == x!0@1#1 >= 1u
// 7 file program.unsigned.c line 3 function program
(15) program!0#1 == x!0@1#1 * y!0@1#1 * 3u
     guard: \guard#1
// 8 file program.unsigned.c line 3 function program
// 10 file program.unsigned.c line 5 function program
(16) program!0#2 == (x!0@1#1 % y!0@1#1) * 4u
     guard: !\guard#1
// 11 file program.unsigned.c line 5 function program
// 13 file program.unsigned.c line 7 function program
(17) program!0#3 == (\guard#1 ? program!0#1 : program!0#2)
// 13 file program.unsigned.c line 7 function program
// 21 file program.unsigned.c line 1
(18) return'!0#1 == program!0#3
// 22 file program.unsigned.c line 1
// 25 
