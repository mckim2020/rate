// Transition Rate Calculation (mu = 1) //
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846
#define kB 8.617333262e-5 // Boltzmann constant



// Potential function
double pot(long double x) {
    return 4/3*x*x*x*x - 10/3*x*x + 2;
}

double dvdx(long double x) {
    return 16/3*x*x*x - 20/3*x;
}



// Random number generator (0, 1]
double r2() {
    return ((long double)rand() + 1) / ((long double)RAND_MAX + 2);
}

// Gaussian RV generator - saves via pointer
// Box-Mueller method
void gauss(long double* z1) {
    long double u1, u2;

    u1 = r2();
    u2 = r2();

    *z1 = sqrt(-2 * log(u1)) * cos(2 * PI * u2);
    // *z2 = sqrt(-2 * log(u1)) * sin(2 * PI * u2);
}



// Kramers' rate rule (theory)
double kramers(double temp) {
    double factor = 0.0;
    double rate = 0.0;

    factor = 1.5005271936;
    rate = factor * exp(-2.08333333333 / kB / temp);

    return rate;
}



// Random walk (discretized time)
double ranWalk(double temp, double dt) {
    long double z1;
    long double z2;

    long double x = -1.1;
    long double dx;

    int itr = 0;
    long double fpt;
    double rate;


    while (1) {
        // Generate Gaussian RV
        gauss(&z1);
        // gauss(&z1, &z2);

        // Calculate deviation
        dx = - dvdx(x) * dt + sqrt(2 * kB * temp * dt) * z1;

        // Update positions
        x = x + dx;

        // // Calculate deviation
        // dx = - dvdx(x) * dt + sqrt(2 * kB * temp * dt) * z2;

        // // Update positions
        // x = x + dx;

        // Termination criteria
        if ((x-1.1)*(x-1.1) < 1e-1) {
            fpt = dt * itr;
            rate = 1 / fpt;
            printf("Transition rate: %.10e\n", rate);
            return fpt;
        }

        // Update count
        itr = itr + 1;
        
        // Print progress
        if (itr%100000000==0) {
            printf("Current iteration: %d\n", itr);
        }
    }
}



int main() {
    double temp = 5000; // Temperature
    double dt = 1e-6;
    double fpt = 0.0;
    double fpt_avg = 0.0;
    double rate_theory = 0.0;

    int count;
    int count_max = 100;

    clock_t start, end;
    double cpu_time_used;

    srand(time(NULL)); // Random seed
    start = clock();

    // Random walk result
    for (count = 0; count < count_max; count++) {
        printf("Current iteration: %d\n", count);
        fpt = ranWalk(temp, dt);
        fpt_avg = fpt_avg + fpt;
    }
    fpt_avg = fpt_avg / count_max;
    printf("Average transition rate (random walk): %.6e\n", 1/fpt_avg);

    // Theoretical result
    rate_theory = kramers(temp);
    printf("Transition rate (Kramers' rule): %.6e\n", rate_theory);

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Rate calculation took %f seconds to execute \n", cpu_time_used); 

    return 0;
}