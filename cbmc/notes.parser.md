I want a python parser which is going to parse IRs that show intermediate representation of a bounded symbolic execution engine for C programs, namely CBMC. It uses SSA, phi-instuctions (guards) and formulas. The number after the exclamation mark represents the thread number, the number after @ represents the frame number, the number after # represents the SSA. The line numbers in comments just before statements indicates where the formulas come from. There are two types of statements and they all begin with a counting number in parenthesis, e.g. (10): there are statements that represent the assignment of a value to a variable, and there are statements that represent the guard of a phi-instruction. The parser should be able to parse the following example. The guards uses the negation operator, the disjunction operator and the conjunction operator, equalities and inequalities. All outputs should be in Z3py format. The logic expects only  Int, Real, String types.

The parser should be able to parse the IR of the following C program:

```c
int candidate(int x, int y) {
  int res;
  if (x > 0) {
    res = x + y * 3;
  } else {
    res = x + y * 4;
  }
  assert(res == (x > 0 ? x + y * 3 : x + y * 4));
  return res;
}
```

```IR
Program constraints:
// 15 
// 15 
...
// 5 
// 16 file program.c line 1 function candidate
// 17 file program.c line 1 function candidate
(10) x!0@1#2 == nondet_symbol<signed int>(symex::nondet0)
// 18 file program.c line 1 function candidate
// 19 file program.c line 1 function candidate
// 20 file program.c line 1 function candidate
(11) y!0@1#2 == nondet_symbol<signed int>(symex::nondet1)
// 21 file program.c line 1 function candidate
// 22 file program.c line 1
// 22 file program.c line 1
// 22 file program.c line 1
(12) x!0@1#1 == x!0@1#2
// 22 file program.c line 1
(13) y!0@1#1 == y!0@1#2
// 6 file program.c line 2 function candidate
// 7 file program.c line 3 function candidate
// 7 file program.c line 3 function candidate
(14) \guard#1 == x!0@1#1 >= 1
// 8 file program.c line 4 function candidate
(15) res!0@1#2 == x!0@1#1 + y!0@1#1 * 3
     guard: \guard#1
// 9 file program.c line 4 function candidate
// 10 file program.c line 6 function candidate
(16) res!0@1#3 == x!0@1#1 + y!0@1#1 * 4
     guard: !\guard#1
// 11 file program.c line 8 function candidate
(17) res!0@1#4 == (\guard#1 ? res!0@1#2 : res!0@1#3)
// 11 file program.c line 8 function candidate
(18) ASSERT(x!0@1#1 >= 1 ? x!0@1#1 + y!0@1#1 * 3 == res!0@1#4 : x!0@1#1 + y!0@1#1 * 4 == res!0@1#4)
// 12 file program.c line 9 function candidate
(sliced) candidate!0#1 == res!0@1#4
// 14 file program.c line 10 function candidate
// 22 file program.c line 1
(sliced) return'!0#1 == candidate!0#1
// 23 file program.c line 1
// 26 
```

I want the parser to return a dictionary with the following structure where it should replace reference by substitutions.

for candidate!0#1:

candidate!0#1 ==
    (x!0@1#1 >= 1 
        ? x!0@1#1 + y!0@1#1 * 3 
        : x!0@1#1 + y!0@1#1 * 4)

    x1 = Int('x1')
    y1 = Int('y1')
    candidate1 = Int('candidate1')
    candidate == If(x1 >= 1, x1 + y1 * 3, x1 + y1 * 4)

for res!0@1#4:
    res!0@1#4 == (x!0@1#1 >= 1 ? x!0@1#1 + y!0@1#1 * 3 : x!0@1#1 + y!0@1#1 * 4)

...

Which variables are non-deterministic such as:
x!0@1#2 == nondet_symbol<int16_t>(symex::nondet0)
    x2 = Int('x2')
y!0@1#2 == nondet_symbol<int16_t>(symex::nondet1)
    y2 = Int('y2')

if there is an assertion, such as the following:
    I want to have the assertion in the dictionary as well:
    ASSERT(x!0@1#1 >= 1 ? x!0@1#1 + y!0@1#1 * 3 == res!0@1#4 : x!0@1#1 + y!0@1#1 * 4 == res!0@1#4)


```c
float program(float x, float y) {
    if (x >= 1) {
        return x + y * 3;
    } else {
        return x + y * 4;
    }
}
```

```IR
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
// 15 file program.float.c line 1 function program
// 16 file program.float.c line 1 function program
(10) x!0@1#2 == nondet_symbol<float>(symex::nondet0)
// 17 file program.float.c line 1 function program
// 18 file program.float.c line 1 function program
// 19 file program.float.c line 1 function program
(11) y!0@1#2 == nondet_symbol<float>(symex::nondet1)
// 20 file program.float.c line 1 function program
// 21 file program.float.c line 1
// 21 file program.float.c line 1
// 21 file program.float.c line 1
(12) x!0@1#1 == x!0@1#2
// 21 file program.float.c line 1
(13) y!0@1#1 == y!0@1#2
// 6 file program.float.c line 2 function program
// 6 file program.float.c line 2 function program
(14) \guard#1 == x!0@1#1 >= 1.0f
// 7 file program.float.c line 3 function program
(15) program!0#1 == FLOAT+(x!0@1#1, FLOAT*(y!0@1#1, 3.0f, 0), 0)
     guard: \guard#1
// 8 file program.float.c line 3 function program
// 10 file program.float.c line 5 function program
(16) program!0#2 == FLOAT+(x!0@1#1, FLOAT*(y!0@1#1, 4.0f, 0), 0)
     guard: !\guard#1
// 11 file program.float.c line 5 function program
// 13 file program.float.c line 7 function program
(17) program!0#3 == (\guard#1 ? program!0#1 : program!0#2)
// 13 file program.float.c line 7 function program
// 21 file program.float.c line 1
(18) return'!0#1 == program!0#3
// 22 file program.float.c line 1
// 25 
```

```c
unsigned program(unsigned x, unsigned y) {
    if (x >= 1) {
        return x * y * 3;
    } else {
        return (x % y) * 4;
    }
}
```

```IR
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
```

First in <scratchpad> tags consider your approach, then return you final answer in python code.
 
