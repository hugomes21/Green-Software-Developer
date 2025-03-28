#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Merge Sort for double
void mergeDouble(double arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    double L[n1], R[n2];

    for (i = 0; i < n1; i++) {
        L[i] = arr[l + i];
    }
    for (j = 0; j < n2; j++) {
        R[j] = arr[m + 1 + j];
    }

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSortDouble(double arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSortDouble(arr, l, m);
        mergeSortDouble(arr, m + 1, r);

        mergeDouble(arr, l, m, r);
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
    mergeSortDouble(double_arr, 0, size - 1);
    free(double_arr);

    return 0;
}