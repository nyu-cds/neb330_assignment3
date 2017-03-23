%%cython
cimport numpy as cnp
import numpy as np
from itertools import combinations


'''
In this module I initialize all variables and functions with cdef.  I also change all list variables
to numpy arrays so I'm able to use efficient indexing.
'''


#define update_vs function with specific input types
cdef void update_vs(cnp.ndarray[cnp.float_t, ndim=1] v1, cnp.ndarray[cnp.float_t, ndim=1] v2, float dt, float dx, float dy, float dz, float m1, float m2):
    cdef float dx_dy_dz = ((dx**2 + dy**2 + dz**2) ** (-1.5))
    cdef float value_to_add_1 = m1 * dt * dx_dy_dz
    cdef float value_to_add_2 = m2 * dt * dx_dy_dz
    v1[0] -= dx * value_to_add_2
    v1[1] -= dy * value_to_add_2
    v1[2] -= dz * value_to_add_2
    v2[0] += dx * value_to_add_1
    v2[1] += dy * value_to_add_1
    v2[2] += dz * value_to_add_1


#define update_rs function with specific input types
cdef void update_rs(cnp.ndarray[cnp.float_t, ndim=1] r, float dt, float vx, float vy, float vz):
    r[0] += dt * vx
    r[1] += dt * vy
    r[2] += dt * vz

#define report_energy function with specific input types
cdef void report_energy(int loops, str reference, int iterations, float dt = 0.01):
    '''
        Combined version of the functions offset_momentum, report_energy, and advance.
        Start by offsetting the momentum. Then, perform the nested loop from the original 
        nbody function, but change it to one single loop.  In each iteration, either 
        perform the advance or report energy based on the iteration number.
    '''
    cdef float PI = 3.14159265358979323
    cdef float SOLAR_MASS = 4 * PI * PI
    cdef float DAYS_PER_YEAR = 365.24

    #change BODIES dictionary to include numpy arrays instead of lists
    BODIES = {
    'sun': (np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), SOLAR_MASS),

    'jupiter': (np.array([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01]),
                np.array([1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR]),
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': (np.array([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01]),
               np.array([-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR]),
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': (np.array([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01]),
               np.array([2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR]),
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': (np.array([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01]),
                np.array([2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR]),
                5.15138902046611451e-05 * SOLAR_MASS)}
    
    
    #offset momentum
    cdef float px, py, pz=0.0
    
    
    for body in BODIES.keys():
        (r, [vx, vy, vz], m) = BODIES[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = BODIES[reference]
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

    #change the nested loop from nbody function to one loop
    for i in range(loops*iterations):
        e = 0.0
        seenit = set()
        
        #use the built-in combinations func to iterate through the keys
        for body1, body2 in combinations(BODIES.keys(), 2):
            ((x1, y1, z1), v1, m1) = BODIES[body1]
            ((x2, y2, z2), v2, m2) = BODIES[body2]
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
            #depending on the value of i, either advance or report energy
            if i % iterations == 0:
                #step for report energy
                e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
            else:
                #advance
                update_vs(v1, v2, dt, dx, dy, dz, m1, m2)
            seenit.add(body1)
        
        #again, check whether its an advance or report_energy step based on i
        for body in BODIES.keys():
            (r, [vx, vy, vz], m) = BODIES[body]
            if i % iterations == 0:
                e += m * (vx * vx + vy * vy + vz * vz) / 2.
            else:
                update_rs(r, dt, vx, vy, vz)
        #report energy
        if i % iterations == 0:
            print(e)



if __name__ == '__main__':
    report_energy(100, 'sun', 20000)
