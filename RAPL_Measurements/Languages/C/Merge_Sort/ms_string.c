#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Merge Sort for string
void mergeString(char *arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    char *L[n1], *R[n2];

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
        if (strcmp(L[i], R[j]) <= 0) {
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

void mergeSortString(char *arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSortString(arr, l, m);
        mergeSortString(arr, m + 1, r);

        mergeString(arr, l, m, r);
    }
}

// Helper function to generate random string array
void generateRandomStringArray(char *arr[], int n) {
    const char charset[] = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < n; i++) {
        arr[i] = malloc(6);
        for (int j = 0; j < 5; j++) {
            arr[i][j] = charset[rand() % (sizeof(charset) - 1)];
        }
        arr[i][5] = '\0';
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <size>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    char **string_arr = malloc(size * sizeof(char *));
    if (!string_arr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    srand(time(NULL));
    generateRandomStringArray(string_arr, size);
    mergeSortString(string_arr, 0, size - 1);

    for (int i = 0; i < size; i++) {
        free(string_arr[i]);
    }
    free(string_arr);

    return 0;
}