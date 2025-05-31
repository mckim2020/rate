// Transition Rate Calculation (mu = 1) //
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846
#define kB 8.617333262e-5 // Boltzmann constant



// Potential function
double pot(double x) {
    return x*x*x*x - 2*x*x;
}

double dvdx(double x) {
    return 4*x*x*x - 4*x;
}



// Random number generator (0, 1)
double r2() {
    // return (double)rand() / RAND_MAX;
    // return ((double)rand() + 1) / ((double)RAND_MAX + 2);
    // return ((double)rand()) / ((double)RAND_MAX + 1.0);
    double random_number = (double)rand() / (RAND_MAX + 1.0);
    return random_number;
}

// Gaussian RV generator - saves via pointer
// Box-Mueller method
void gauss(double* z1, double* z2) {
    double u1, u2;

    u1 = r2();
    u2 = r2();

    // *z1 = sqrt(-2.0 * log(u1)) * cos(2.0 * PI * u2);
    *z1 = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
    *z2 = sqrt(-2.0 * log(u1)) * sin(2.0 * M_PI * u2);
}

double box_mueller() {
    static int has_spare = 0;
    static double spare;
    
    if (has_spare) {
        has_spare = 0;
        return spare;
    } else {
        double u1, u2, radius, theta;
        double z1;
        
        // Get two uniform random numbers in (0,1)
        do {
            u1 = r2();
            u2 = r2();
        } while (u1 <= 0); // Ensure u1 is not 0
        
        // Box-Mueller transformation
        radius = sqrt(-2.0 * log(u1));
        theta = 2.0 * M_PI * u2;
        
        // Generate two normal random variables
        z1 = radius * cos(theta);
        spare = radius * sin(theta);
        
        has_spare = 1;
        return z1;
    }
}



// Kramers' rate rule (theory)
double kramers(double temp, double mu) {
    double factor = 0.0;
    double rate = 0.0;

    factor = 0.9003163162;
    rate = mu * factor * exp(-1.0 / kB / temp);

    return rate;
}



// Random walk (discretized time)
double ranWalk(double temp, double mu, double dt) {
    double z1;
    double z2;

    double x = -1.0;
    double dx;

    int itr = 0;
    double fpt = 0.0;

    // Initialize random numbers
    z1 = box_mueller();
    z2 = box_mueller();

    while (1) {
        // Leimkuhler Matthews (2012) https://arxiv.org/abs/1203.5428
        dx = - mu * dvdx(x) * dt + sqrt(mu * kB * temp * dt / 2.0) * (z1 + z2);
        z1 = z2;
        z2 = box_mueller();

        // Update positions
        x = x + dx;

        // Update count
        itr = itr + 1;

        // Termination criteria
        if (x >= 1.0) {
            fpt = dt * itr;
            return fpt;
        }

        // Print progress
        if (itr%100000000==0) {
            printf("Current iteration: %d\n", itr);
        }
    }
}



int main() {
    double temp = 1300.0; // Temperature
    double mu = 0.02; // Mobility tensor
    double dt = 1e-2; // Time step
    double fpt = 0.0; // First passage time
    double fpt_avg = 0.0; // Average first passage time
    double rate_theory = 0.0; // Theoretical rate

    int count;
    int count_max = 10000; // 0.9 seconds (1500K), 22.9 seconds (1000K)

    clock_t start, end;
    double cpu_time_used;

    // Open file to save fpt values
    char filename[100]; // Buffer to hold the filename
    sprintf(filename, "./data/fpt_values_%d.txt", (int)temp);
    FILE *file = fopen(filename, "w");

    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    srand(time(NULL)); // Random seed
    start = clock();

    // Random walk result
    for (count = 0; count < count_max; count++) {
        printf("Current iteration: %d\n", count);
        fpt = ranWalk(temp, mu, dt);
        fpt_avg = fpt_avg + fpt;

        // Write the fpt value to the file
        fprintf(file, "%.6e\n", fpt);
    }
    fpt_avg = fpt_avg / count_max;
    printf("Estimated transition rate (random walk): %.6e\n", 1/fpt_avg);

    // Close the file
    fclose(file);

    // Theoretical result
    rate_theory = kramers(temp, mu);
    printf("Ground truth transition rate (Kramers' rule): %.6e\n", rate_theory);

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Rate calculation took %f seconds to execute \n", cpu_time_used); 

    return 0;
} 