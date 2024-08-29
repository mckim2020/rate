// Transition Rate Calculation (mu = 1) //
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846
#define kB 8.617333262e-5 // Boltzmann constant



// Potential function
double pot(long double x) {
    return x*x*x*x - 2*x*x;
}

double dvdx(long double x) {
    return 4*x*x*x - 4*x;
}



// Random number generator (0, 1]
double r2() {
    // return (double)rand() / RAND_MAX;
    return ((long double)rand() + 1) / ((long double)RAND_MAX + 2);
}

// Gaussian RV generator - saves via pointer
// Box-Mueller method
void gauss(long double* z1, long double* z2) {
    long double u1, u2;

    u1 = r2();
    u2 = r2();

    // *z1 = sqrt(-2.0 * log(u1)) * cos(2.0 * PI * u2);
    *z1 = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
    *z2 = sqrt(-2.0 * log(u1)) * sin(2.0 * M_PI * u2);
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
    long double z1;
    long double z2;

    long double x = -1.0;
    long double dx;

    int itr = 0;
    long double fpt = 0.0;
    // double rate;

    while (1) {
        // Generate Gaussian RV
        // gauss(&z1);
        gauss(&z1, &z2);

        // Calculate deviation
        dx = - mu * dvdx(x) * dt + sqrt(2 * mu * kB * temp * dt) * z1;

        // Update positions
        x = x + dx;

        // Update count
        itr = itr + 1;

        // Termination criteria
        if (x >= 1.0) {
            fpt = dt * itr;
            // rate = 1.0 / fpt;
            // printf("Transition rate: %.10e\n", rate);
            return fpt;
        }

        // Calculate deviation
        dx = - mu * dvdx(x) * dt + sqrt(2 * mu * kB * temp * dt) * z2;

        // Update positions
        x = x + dx;

        // Update count
        itr = itr + 1;

        // Termination criteria
        // if ((x-1.1)*(x-1.1) < 1e-1) {
        if (x >= 1.0) {
            fpt = dt * itr;
            // rate = 1.0 / fpt;
            // printf("Transition rate: %.10e\n", rate);
            return fpt;
        }

        // // Update count
        // itr = itr + 1;

        // // Print progress
        // if (itr%100000000==0) {
        //     printf("Current iteration: %d\n", itr);
        // }
    }
}



int main() {
    double temp = 1150; // Temperature
    double mu = 1.0; // Mobility tensor
    double dt = 5e-3;
    double fpt = 0.0;
    double fpt_avg = 0.0;
    double rate_theory = 0.0;

    int count;
    int count_max = 1000;

    clock_t start, end;
    double cpu_time_used;

    srand(time(NULL)); // Random seed
    start = clock();

    // Random walk result
    for (count = 0; count < count_max; count++) {
        printf("Current iteration: %d\n", count);
        fpt = ranWalk(temp, mu, dt);
        fpt_avg = fpt_avg + fpt;
    }
    fpt_avg = fpt_avg / count_max;
    printf("Estimated transition rate (random walk): %.6e\n", 1/fpt_avg);

    // Theoretical result
    rate_theory = kramers(temp, mu);
    printf("Ground truth transition rate (Kramers' rule): %.6e\n", rate_theory);

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Rate calculation took %f seconds to execute \n", cpu_time_used); 

    return 0;
} 