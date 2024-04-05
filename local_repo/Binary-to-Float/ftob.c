/* Print a float in binary: ftob.c */

/*
  Write a C program to print the binary values of a floating point number passed as a parameter, 
  as demonstrated in class, by filling in ftob.c. 
  For example, it would print "0 01111110 10000000000000000000000" when you type "ftob 0.75." 
  So would it "0 01111101 00110011001100110011010" when you type "ftob 0.3" as demonstrated in class. 
*/

#include <stdio.h>
#include <stdlib.h>

//void float_to_string(float f, char *s, int n);
void float_to_string(float,char *,int);
void print_float();

#define LEN 32
#define EXP_32 8		/* ending index of s for exponent */
#define MAN_32 9		/* starting index of s for significand */

int main(int argc, char **argv) {
  int n=LEN;
  float f;
  char s[LEN];

  f = atof(argv[1]);
  printf("f=%f\n",f);

  float_to_string(f,s,n);
  print_float(s,n);

  return 0;
}

/* convert float to binary and store in s, a string of 32 chars */
void float_to_string(float f, char *s, int n){
  unsigned int u_int;
  int i;			/* for loop index */

  /* fill here */
  
  u_int = *(unsigned int*)&f; // read float bits as an int
  
  // sign bit
  int sign = f >= 0 ? 0 : 1;
  s[0] = sign + '0';
  
  
  // exp bits
  int exp = (u_int >> 23);  // remove frac
  exp = exp & 0xFF; // remove sign bit
  
  for (i = EXP_32; i >= 1; i--) {
    s[i] = (exp & 0x01) + '0';
    exp >>= 1;
  }

  // frac bits
  unsigned int frac = u_int & 0x7FFFFF;
   
  for (i = LEN - 1; i >= MAN_32; i--) {
    s[i] = (frac & 0x01) + '0';
    frac >>= 1;
  }

  s[LEN] = '\0';  
}

/* print space in between sign bit, exponent, and frac */
void print_float(char *s, int n) {
  int i=0;

  /* fill here */
  
  for (i = 0; i < n; i++) {
    printf("%c", s[i]);
    if (i == 0 || i == EXP_32) printf(" ");
  }
  printf("\n");

}

/* End of ftob.c */