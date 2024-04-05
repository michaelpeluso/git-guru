/* Print a float in binary: btof.c */

/*
  Write a C program to print the decimal value of a binary string passed as a parameter. 
  For example, it would print 0.75 when you type "btof '0 01111110 10000000000000000000000'".
  As another example, it would print 0.125 when you type "btof '0 01111100 00000000000000000000000'".
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

//void float_to_string(float f, char *s, int n);
void string_to_float(float,char *,int);
void organize_input(char *s);
 
#define LEN 32
#define EXP_32 8		/* ending index of s for exponent */
#define MAN_32 9		/* starting index of s for significand */

int main(int argc, char **argv) {
  int n=LEN;
  float f;
  char s[LEN];
  
  // manage user input
  strcpy(s, argv[1]);
  organize_input(s);
  
  // conversion
  string_to_float(f,s,n);
  
  return 0;
}

/* format user input for processing */
void organize_input(char *s) {

  int readIndex = 0, writeIndex = 0;

  while (s[readIndex]) {
    if (s[readIndex] != ' ') {
      s[writeIndex++] = s[readIndex];
    }
    readIndex++;
  }

    s[writeIndex] = '\0';
}

/* convert binary string to float  */
void string_to_float(float f, char *s, int n){
  float v, bias, m, e;
  int i, j;
  
  // sign
  int sign = s[0] == '1' ? -1 : 1;

  // exp
  char exp_str[EXP_32];
  for (i = 1, j = 0; j < EXP_32 && s[i] != '\0'; i++, j++) {
      exp_str[j] = s[i];
  }
  exp_str[j] = '\0';
  
  float exp = (float)strtol(exp_str, NULL, 2);
  
  // frac
  char frac_str[LEN - MAN_32];
  for (i = MAN_32, j = 0; j < LEN - MAN_32 && s[i] != '\0'; i++, j++) {
      frac_str[j] = s[i];
  }
  frac_str[j] = '\0';
  
  float frac = (float)strtol(frac_str, NULL, 2);
  
  // bias
  bias = pow(2, EXP_32 - 1) - 1;
  
  // m & e
  if (exp == 0) {
    m = frac / pow(2, LEN - MAN_32);
    e = 1 - bias;
  }
  else if (exp == pow(2, EXP_32) - 1) {
    printf("Infinity\n");
    return;
  }
  else {
    m = frac / pow(2, LEN - MAN_32) + 1;
    e = exp - bias;
  }
  
  // v
  v = (float)sign * m * pow(2, e);
  
  // print to console
  printf("\nbits: %s", s);
  printf("\nsign = %i\nexp = %f\nfrac = %f\n", sign, exp, frac);
  printf("\nv= %f\n\n\n", v);
}

/* End of btof.c */