#include <stdio.h>
#include <stdlib.h>

void write_to_csv(const char* filename, int* values, int count) {
  FILE* fp = fopen(filename, "a");  // Open the file in append mode
  if (fp == NULL) {
    perror("Unable to open file!");
    exit(1);
  }
  for (int i = 0; i < count; ++i) {
    fprintf(fp, "%d", values[i]);
    if (i < count - 1) {
      fputc(',', fp);  // Add a comma after all but the last value
    }
  }
  fputc('\n', fp);  // Add a newline at the end of the row
  fclose(fp);       // Close the file
}

void vtrace1(int q, int r, int a, int b, int x, int y) {
  int values[] = {q, r, a, b, x, y};
  write_to_csv("vtrace1.csv", values, 6);
}

void vtrace2(int q, int r, int a, int b, int x, int y) {
  int values[] = {q, r, a, b, x, y};
  write_to_csv("vtrace2.csv", values, 6);
}

void vtrace3(int q, int r, int x, int y) {
  int values[] = {q, r, x, y};
  write_to_csv("vtrace3.csv", values, 4);
}

// void vassume(int b){}
// void vtrace1(int q, int r, int a, int b, int x, int y){}
// void vtrace2(int q, int r, int a, int b, int x, int y){}
// void vtrace3(int q, int r, int x, int y){}

int test(int x, int y) {
  // vassume(x >= 1 && y >= 1);

  int q = 0;
  int r = x;
  int a = 0;
  int b = 0;
  while (1) {
    vtrace1(q, r, a, b, x, y);
    if (!(r >= y)) break;
    a = 1;
    b = y;

    while (1) {
      vtrace2(q, r, a, b, x, y);
      if (!(r >= 2 * b)) break;

      a = 2 * a;
      b = 2 * b;
    }
    r = r - b;
    q = q + a;
  }
  vtrace3(q, r, x, y);
  return q;
}