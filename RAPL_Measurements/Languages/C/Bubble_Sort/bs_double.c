#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Bubble Sort for double
void bubbleSortDouble(double arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                double temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// Helper function to generate random double array
void generateRandomDoubleArray(double arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = (double)rand() / (double)(RAND_MAX / 100);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <size>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    double *double_arr = malloc(size * sizeof(double));
    if (!double_arr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    srand(time(NULL));
    generateRandomDoubleArray(double_arr, size);
    bubbleSortDouble(double_arr, size);
    free(double_arr);

    return 0;
}