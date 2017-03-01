
from itertools import permutations


def zbits(n, k):
    init_string = ''
    for i in range(k):
        init_string = init_string + '0'
    for i in range(n-k):
        init_string = init_string + '1'
    bits = set(list(permutations(init_string, n)))
    bits_clean = []
    for bit in bits:
        bits_clean.append(''.join(bit))
    return set(bits_clean)
          
          
if __name__ == '__main__':
    zbits(4,1)




