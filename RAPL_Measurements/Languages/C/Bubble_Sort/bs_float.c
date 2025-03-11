#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Bubble Sort for float
void bubbleSortFloat(float arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                float temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
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
    bubbleSortFloat(float_arr, size);
    free(float_arr);

    return 0;
}