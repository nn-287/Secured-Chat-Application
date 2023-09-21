# modular exponentiation
def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result




def perform_key_exchange():

    q = 353
    a = 3

    # Private keys for Alice and Bob
    a_key = 97
    b_key = 233

    # Calculate public keys for Alice and Bob
    A_key = mod_exp(a, a_key, q)
    B_key = mod_exp(a, b_key, q)

    # Perform key exchange
    shared_key_a = mod_exp(B_key, a_key, q)
    shared_key_b = mod_exp(A_key, b_key, q)

    # Ensure both shared keys are equal
    assert shared_key_a == shared_key_b
    shared_key_a = str(shared_key_a)\
    # print(shared_key_a)

    # Return the shared key
    return shared_key_a