# Float to Binary and Binary to Float Converter
This repository contains two C programs that facilitate the conversion between floating-point numbers and their binary representations. The programs are named ftob.c and btof.c.

### Compile
```bash
gcc ftob.c -o ftob
gcc btof.c -o btof
```

***

## Float to Binary `ftob.c`

This C program, **ftob.c**, converts a floating-point number to its binary representation when passed as a parameter.


### Usage

Compile **ftob.c** using a C compiler, and then run the compiled program with the desired floating-point number as a parameter.

Run:
```bash
./ftob 0.75
```

This would print:
```bash
00111111010000000000000000000000
```

***

## Binary to Float `btof`

This C program, **btof.c**, converts a binary string to its decimal floating-point representation when passed as a parameter.

### Usage

Compile **btof.c** using a C compiler, and then run the compiled program with the desired binary string as a parameter.

Run:
```bash
./btof '00111110100110011001100110011010'
```

This would print:
```bash
0.3
```

