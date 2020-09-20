# Pohlig Hellman Python Implementation
The Pohlig-Hellmann algorithm is an algorithm for computing the discrete logarithm problem in a cyclic group. By reducing the problem to subgroups, this happens in significantly fewer steps than with a naive brute force attack, especially
fast when the group order is factored out of small prime numbers. First, the prime factors of the group order are determined, then for each of these factors the discrete logarithm problem in the subgroup is solved. The partial results are then unambiguously connected to the overall solution using the
Chinese remainder theorem.
