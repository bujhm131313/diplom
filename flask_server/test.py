BIGGEST_FIVE_DIGIT_NUMBER = 99999
SMALLEST_FIVE_DIGIT_NUMBER = 10000

#99999 * 99999
BIGGEST_POSSIBLE_PALINDROME = 9999800001


def is_palindrome(number):
    """
    Reverts the number and checks for equality with the original one
    :rtype: Boolean
    """
    return str(number) == str(number)[::-1]


def is_prime_number(number):
    """
    :rtype: Boolean
    """
    return all(number % i for i in range(2, number))


def find_five_digits_prime_numbers(from_number, to_number):
    """
    Finds prime numbers in range in reverse order (the biggest prime number
    comes first)
    :param from_number: smallest number (left range edge)
    :param to_number: biggest
    :rtype: list of 5-digits prime numbers
    """

    prime_numbers = []
    for i in range(to_number, from_number, -1):
        if is_prime_number(i):
            prime_numbers.append(i)
    return prime_numbers


def find_biggest_palindrome_list(top_border):
    """
    Finds all palindromes in range 0..top_border in reverse order
    (biggest comes first)
    :rtype: generator of biggest palindromes
    :param top_border: int
    """
    for i in range(top_border, 0, -1):
        if is_palindrome(i):
            yield i


def find_biggest_palindrome():

    # Find all 5-digits prime numbers
    prime_numbers = find_five_digits_prime_numbers(
        SMALLEST_FIVE_DIGIT_NUMBER, BIGGEST_FIVE_DIGIT_NUMBER)

    # Iterate on all palindromes generator
    for palindrome in find_biggest_palindrome_list(
            BIGGEST_POSSIBLE_PALINDROME):

        for prime_number in prime_numbers:
            second_divisor = palindrome/prime_number

            if second_divisor > BIGGEST_FIVE_DIGIT_NUMBER:
                break

            # We check if second divisor is int first to stop
            # program from searching number in a huge list
            if int(second_divisor) == second_divisor\
                    and is_prime_number(int(second_divisor)):
                return palindrome, prime_number, second_divisor


print(find_biggest_palindrome())
