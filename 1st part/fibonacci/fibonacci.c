#include <stdio.h>

int main() {
    int n = 20;// The number of terms to be calculated
    int t1 = 0; // First term
    int t2 = 1; // Second term
    int nextTerm; // Next term of the series

    printf("Fibonacci Sequence: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", t1); // Print the current term
        nextTerm = t1 + t2; // Calculate the next term
        t1 = t2; // Assign the second term to the first term
        t2 = nextTerm; // Assign the next term to the second term
    }

    return 0;
}
