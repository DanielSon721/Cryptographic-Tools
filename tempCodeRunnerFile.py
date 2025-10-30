import sys
import random

def diffie_hellman(p, g, a_private, b_private):
    """Perform Diffie–Hellman key exchange.

    p: prime modulus
    g: base (generator)
    a_private: Alice's private key
    b_private: Bob's private key
    """
    # Public keys
    A = pow(g, a_private, p)
    B = pow(g, b_private, p)

    # Shared secrets
    shared_secret_a = pow(B, a_private, p)
    shared_secret_b = pow(A, b_private, p)

    return A, B, shared_secret_a, shared_secret_b


def main():
    print("=== Diffie–Hellman Key Exchange ===")

    try:
        p = int(input("Enter a large prime number (p): "))
        g = int(input("Enter a primitive root modulo p (g): "))
    except ValueError:
        print("Error: p and g must be integers.")
        sys.exit(1)

    # Random private keys (you could prompt for these instead)
    a_private = random.randint(2, p - 2)
    b_private = random.randint(2, p - 2)

    print(f"\nAlice's private key: {a_private}")
    print(f"Bob's private key: {b_private}")

    A, B, shared_a, shared_b = diffie_hellman(p, g, a_private, b_private)

    print(f"\nAlice sends public key A = {A}")
    print(f"Bob sends public key B = {B}")

    print(f"\nAlice computes shared secret: {shared_a}")
    print(f"Bob computes shared secret:   {shared_b}")

    if shared_a == shared_b:
        print("\n✅ Shared secret successfully established!")
    else:
        print("\n❌ Error: Shared secrets do not match.")


if __name__ == "__main__":
    main()
