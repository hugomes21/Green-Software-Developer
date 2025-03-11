#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Counting Sort for float
void countingSortFloat(float arr[], int n) {
    // Assuming the range of float values is known and limited
    int range = 100; // Example range
    int count[range + 1];
    float output[n];

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

// Helper function to generate random float array
void generateRandomFloatArray(float arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = (float)rand() / (float)(RAND_MAX / 100);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <size>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    float *float_arr = malloc(size * sizeof(float));
    if (!float_arr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    srand(time(NULL));
    generateRandomFloatArray(float_arr, size);
    countingSortFloat(float_arr, size);
    free(float_arr);

    return 0;
}