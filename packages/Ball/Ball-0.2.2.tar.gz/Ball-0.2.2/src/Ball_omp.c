#include "Ball_omp.h"

int omp_get_thread_num() { return 0; }
int omp_get_num_threads() { return 1; }
int omp_get_num_procs() { return 1; }
void omp_set_num_threads(int nthread) {}
void omp_set_dynamic(int flag) {}