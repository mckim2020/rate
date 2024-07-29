#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define SIZE 1000000000

// Function to generate normally distributed random numbers
void generate_normal_distribution(double* array, size_t size) {
    for (size_t i = 0; i < size; i += 2) {
        // Generate two uniformly distributed random numbers
        double u1 = (double)rand() / RAND_MAX;
        double u2 = (double)rand() / RAND_MAX;

        // Apply the Box-Muller transform
        double z1 = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
        double z2 = sqrt(-2.0 * log(u1)) * sin(2.0 * M_PI * u2);

        // Store the results
        if (i < size) array[i] = z1;
        if (i + 1 < size) array[i + 1] = z2;
    }
}

int main() {
    // Seed the random number generator
    srand((unsigned int)time(NULL));

    // Allocate memory for the array
    double* array = (double*)malloc(SIZE * sizeof(double));
    if (array == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Generate the random numbers
    generate_normal_distribution(array, SIZE);

    // Optionally: Print the first few numbers to verify
    for (int i = 0; i < 10; i++) {
        printf("%f\n", array[i]);
    }

    // Free allocated memory
    free(array);

    return 0;
}