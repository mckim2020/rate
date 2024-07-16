#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846



// Potential function
double pot(double x, double y) {
    return 0.02*y + (4*(1-x*x-y*y)*(1-x*x-y*y) + 2*(x*x-2)*(x*x-2) + ((x+y)*(x+y)-1)*((x+y)*(x+y)-1) + ((x-y)*(x-y)-1)*((x-y)*(x-y)-1) - 2) / 6;
}

double dvdx(double x, double y) {
    return (4*x*(4*x*x + 5*y*y - 5))/3;
}

double dvdy(double x, double y) {
    return (20*x*x*y)/3 + 4*y*y*y - 4*y + 1/50;
}



// Random number generator (0, 1]
double r2_old2() {
    return (double)rand() / (double)RAND_MAX ;
}

double r2_old() {
    double rand_val = (double)rand() / (RAND_MAX + 1.0);
    return rand_val + 1.0 / (RAND_MAX + 1.0);
}

double r2() {
    return ((double)rand() + 1) / ((double)RAND_MAX + 2);
}

// Gaussian RV generator - saves via pointer
// Box-Mueller method
double gauss0() {
    double u1, u2;

    u1 = r2();
    u2 = r2();

    return sqrt(-2 * log(u1)) * cos(2 * PI * u2);
}

void gauss1(double* z1, double* z2) {
    double u1, u2;

    u1 = r2();
    u2 = r2();

    *z1 = sqrt(-2 * log(u1)) * cos(2 * PI * u2);
    *z2 = sqrt(-2 * log(u1)) * sin(2 * PI * u2);
}

// Gaussian RV generator - saves via pointer
// Marsaglia polar method
void gauss2(double *z1, double *z2) {
    double x, y, s;

    x = r2();
    y = r2();
    s = x*x + y*y;

    if (s > 0 && s < 1) {
        *z1 = x * sqrt(-2 * log(s) / s);
        *z2 = y * sqrt(-2 * log(s) / s);
    }

    else {
        gauss2(z1, z2);
    }
}



double ranWalk(double temp, double dt) {
    double kB = 8.617333262e-5;
    double z1, z2;
    double z3, z4;

    double x=-1.1, y=0.0;
    double dx, dy;

    int itr = 0;
    double fpt;
    double rate;


    while (1) {
        // Generate Gaussian RV
        gauss1(&z1, &z2);
        gauss1(&z3, &z4);

        // Calculate deviation
        dx = - dvdx(x, y) * dt + sqrt(2 * kB * temp * dt) * z1;
        dy = - dvdy(x, y) * dt + sqrt(2 * kB * temp * dt) * z4;

        // Update positions
        x = x + dx;
        y = y + dy;

        // Termination criteria
        if ((x-1.1)*(x-1.1) + (y-0.0)*(y-0.0) < 1e-2) {
            fpt = dt * itr;
            rate = 1 / fpt;
            printf("Transition rate: %.10e\n", rate);
            return rate;
        }

        // Update count
        itr = itr + 1;
        
        // // Print coordinates
        // if (itr%1000000==0) {
        //     printf("Current iteration: %d\n", itr);
        // }
    }
}



int main() {
    double temp = 1000; // Temperature
    double dt = 5e-3;
    double rate = 0.0;
    double rate_avg = 0.0;

    int count;
    int count_max = 1;

    clock_t start, end;
    double cpu_time_used;

    start = clock();

    // Run random walk
    for (count = 0; count < count_max; count++) {
        srand(time(NULL)); // Random seed
        printf("Current iteration: %d\n", count);
        rate = ranWalk(temp, dt);
        rate_avg = rate_avg + rate;
    }
    rate_avg = rate_avg / count_max;
    printf("Average transition rate: %.2e\n", rate_avg);

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Rate calculation took %f seconds to execute \n", cpu_time_used); 

    return 0;
}