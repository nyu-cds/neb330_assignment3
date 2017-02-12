"""
    N-body simulation.
    
    Here I try to change all lists to arrays, and all computations to vector
    computations. However, it doesn't yeild the correct results. Requires more
    testing to figure out why.
    
"""
from itertools import combinations
import numpy as np



    
def report_energy(loops, reference, iterations, dt = 0.01):
    '''
        compute the energy and return it so that it can be printed. 
        If advance = True, advance one time step instead of reporting the energy.
    '''
    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    BODIES = {
    'sun': (np.zeros(3), np.zeros(3), SOLAR_MASS),

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
    

    p = np.zeros(3)
    for body in BODIES.keys():
        (r, v, m) = BODIES[body]
        p -= m*v
        
    (r, v, m) = BODIES[reference]
    v = p/m
    
    
    for i in range(100000):
        e = 0.0
        seenit = {}
        
        #use the built-in combinations func to iterate through the keys
        for body1, body2 in combinations(BODIES.keys(), 2):
            if not (body2 in seenit.keys()):
                (xyz_1, v1, m1) = BODIES[body1]
                (xyz_2, v2, m2) = BODIES[body2]
                dxyz = xyz_1 - xyz_2
                if i % iterations == 0:
                    e -= (m1 * m2) / np.linalg.norm(dxyz)
                else:
                    dx_dy_dz =  np.dot(dxyz,dxyz)**(-1.5)
                    v1 -= (dxyz * m1 * dt * dx_dy_dz)
                    v2 += (dxyz * m2 * dt * dx_dy_dz)
                seenit[body1] = 1
        
        for body in BODIES.keys():
            (r, v, m) = BODIES[body]
            if i % iterations == 0:
                e += m * np.dot(v,v) / 2.
            else:
                r += dt * v
        if i % iterations == 0:
            print(e)



if __name__ == '__main__':
    report_energy(100, 'sun', 20000)

