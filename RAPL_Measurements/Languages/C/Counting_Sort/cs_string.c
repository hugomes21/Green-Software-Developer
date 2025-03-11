#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Counting Sort for string
void countingSortString(char *arr[], int n) {
    int range = 256; // ASCII range
    int count[range + 1];
    char *output[n];

    for (int i = 0; i <= range; ++i) {
        count[i] = 0;
    }
    for (int i = 0; i < n; i++) {
        count[(int)arr[i][0]]++;
    }
    for (int i = 1; i <= range; i++) {
        count[i] += count[i - 1];
    }
    for (int i = n - 1; i >= 0; i--) {
        output[count[(int)arr[i][0]] - 1] = arr[i];
        count[(int)arr[i][0]]--;
    }
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
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
    countingSortString(string_arr, size);

    for (int i = 0; i < size; i++) {
        free(string_arr[i]);
    }
    free(string_arr);

    return 0;
}