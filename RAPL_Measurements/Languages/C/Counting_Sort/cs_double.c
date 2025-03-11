#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Counting Sort for double
void countingSortDouble(double arr[], int n) {
    // Assuming the range of double values is known and limited
    int range = 100; // Example range
    int count[range + 1];
    double output[n];

    for (int i = 0; i <= range; ++i) {
        count[i] = 0;
    }
    for (int i = 0; i < n; i++) {
        count[(int)arr[i]]++;
    }
    for (int i = 1; i <= range; i++) {
        count[i] += count[i - 1];
    }
    for (int i = n - 1; i >= 0; i--) {
        output[count[(int)arr[i]] - 1] = arr[i];
        count[(int)arr[i]]--;
    }
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
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
    countingSortDouble(double_arr, size);
    free(double_arr);

    return 0;
}