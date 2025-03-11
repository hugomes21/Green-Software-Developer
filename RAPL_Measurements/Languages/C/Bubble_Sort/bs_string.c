#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Bubble Sort for string
void bubbleSortString(char *arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (strcmp(arr[j], arr[j + 1]) > 0) {
                char *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
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
    bubbleSortString(string_arr, size);

    for (int i = 0; i < size; i++) {
        free(string_arr[i]);
    }
    free(string_arr);

    return 0;
}