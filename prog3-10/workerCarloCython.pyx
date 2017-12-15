from libc.stdlib cimport rand, srand, RAND_MAX
cimport cython

cpdef monte_carlo(quantity, seed):
    return cdef_monte_carlo(quantity, seed)

@cython.cdivision(True)
cdef long cdef_monte_carlo(long quantity, long seed):
    cdef long hits = 0
    cdef double width = 0.0
    cdef double height = 0.0
    cdef double temp = 0.0
    srand(seed)
    
    for _ in range(quantity):
        width = <double>rand()/RAND_MAX
        height = <double>rand()/RAND_MAX
        if width * width + height * height < 1:
            hits += 1

    return hits