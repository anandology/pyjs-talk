
def is_prime(n):
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def count_primes(n):
    count = 0
    i = 2
    while i < n:
        if is_prime(i): 
            count += 1 
        i += 1
    return count
        
print count_primes(100000)
        
