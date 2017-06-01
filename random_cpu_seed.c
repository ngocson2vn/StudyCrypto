# include <stdio.h>

unsigned long long rdtsc(){
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((unsigned long long)hi << 32) | lo;
}

unsigned long long rdrnd(void) {
    typedef unsigned long long qword;
    unsigned int low, high;
    
    // Get a random number from the rdrand assembly instruction
    __asm__ volatile ( "rdrand %0;" : "=r" ( low ) );
    __asm__ volatile ( "rdrand %0;" : "=r" ( high ) );
    return ((qword)high << 32U) | low;
}

int main() {
    printf("%llu\n", rdtsc());
    printf("%llu\n", rdrnd());
    return 0;   
}
