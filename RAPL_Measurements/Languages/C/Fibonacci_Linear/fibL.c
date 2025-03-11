#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_terms>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    int i;

    // Inicializar os dois primeiros termos
    int t1 = 0, t2 = 1;

    // Inicializar o próximo termo
    int nextTerm = t1 + t2;

    // print 3rd to nth terms
    for (i = 3; i <= n; i++) {
        printf("%d ", nextTerm);
        t1 = t2;
        t2 = nextTerm;
        nextTerm = t1 + t2;
    }

    return 0;
}