import sys

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

    try:
        a_private = int(input("Enter Alice's private key: "))
        b_private = int(input("Enter Bob's private key: "))
    except ValueError:
        print("Error: private keys must be integers.")
        sys.exit(1)

    A, B, shared_a, shared_b = diffie_hellman(p, g, a_private, b_private)

    print(f"\nAlice's public key (A): {A}")
    print(f"Bob's public key (B):   {B}")

    if shared_a == shared_b:
        print(f"\nShared secret {shared_a} successfully established!")
    else:
        print("\nError: Shared secrets do not match.")


if __name__ == "__main__":
    main()
