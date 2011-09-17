function is_prime(n) {
    var i;
    i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i += 1;
    }
    return true;
}
function count_primes(n) {
    var count, i;
    count = 0;
    i = 2;
    while (i < n) {
        if (is_prime(i)) {
            count += 1;
        }
        i += 1;
    }
    return count;
}
print(count_primes(100000), "\n");

