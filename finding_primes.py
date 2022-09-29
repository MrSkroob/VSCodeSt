import time
numbers = 10000000
primes = [True] * numbers
primes[0] = False

def find_primes_wikipedia(): # translated from what wikipedia gave
    for i in range(int(numbers ** 0.5)):
        if primes[i] == True: # check if result is a prime
            for j in range(i ** 2, numbers, i): # iterate through the rest of the list to find multiples of said prime
                primes[j] = False


def find_primes(): # my attempt
    multiple = 2
    number_to_test = multiple
    for _ in range(int(numbers ** 0.5)):
        for _ in range(multiple, int(numbers / multiple), multiple):
            number_to_test += multiple
            primes[number_to_test - 1] = False # set every multiple to false
        multiple += 1 # increment to the next multiple
        number_to_test = multiple 


start = time.process_time()
find_primes()
print("My solution: ", time.process_time() - start)

start = time.process_time()
find_primes_wikipedia()
print("Their solution: ", time.process_time() - start)


"""find_primes(primes)

find_primes_wikipedia()"""
