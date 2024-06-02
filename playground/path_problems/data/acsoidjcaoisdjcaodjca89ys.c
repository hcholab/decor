/*
  Cohen's integer division
  returns x % y
  http://www.cs.upc.edu/~erodri/webpage/polynomial_invariants/cohendiv.htm
*/

#include <stdio.h>
#include <stdlib.h>

int cohendiv(int x, int y) {
  vdistr(x, 1, 300);
  vdistr(y, 1, 300);

  vassume(x >= 1 && y >= 1);

  int q = 0;
  int r = x;
  int a = 0;
  int b = 0;
  while (1) {
    // a*r - a*x + b*q == 0;
    // a*y - b == 0;
    // x == q*y + r;
    vtrace1(q, r, a, b, x, y);
    if (!(r >= y)) break;
    a = 1;
    b = y;

    while (1) {
      // a*r - a*x + b*q == 0;
      // a*y - b == 0;
      // x == q*y + r;
      // r >= 0;
      vtrace2(q, r, a, b, x, y);
      if (!(r >= 2 * b)) break;
      // r >= 2 * y * a;
      a = 2 * a;
      b = 2 * b;
    }
    r = r - b;
    q = q + a;
  }
  // q*y + r - x == 0
  vtrace3(q, r, x, y);  // Bitween
  return q;
}
