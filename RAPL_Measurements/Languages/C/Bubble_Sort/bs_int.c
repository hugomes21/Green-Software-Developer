#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Bubble Sort for int
void bubbleSortInt(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// Helper function to generate random int array
void generateRandomIntArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <size>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    int *int_arr = malloc(size * sizeof(int));
    if (!int_arr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    srand(time(NULL));
    generateRandomIntArray(int_arr, size);
    bubbleSortInt(int_arr, size);
    free(int_arr);

    return 0;
}