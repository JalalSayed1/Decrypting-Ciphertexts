from Rotor96Crypto import Rotor96Crypto


def load_passwords(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def load_text(filename):
    with open(filename, 'r') as file:
        return file.read().strip()


def cipher_only_attack(ciphertext, password_file):
    passwords = load_passwords(password_file)
    possible_decipher = {}

    common_words = [
        "hello", "world", "this", "is", "the", "and", "of", "to", "in", "that",
        "have", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "be", "by", "are", "or", "from", "but", "my", "if", "your", "has", "they",
        "we", "can", "her", "was", "said", "there", "use", "an", "each", "which",
        "she", "doe", "about", "out", "many", "then", "them", "these", "so", "some",
    ]

    for password in passwords:
        try:
            decrypted_text = Rotor96Crypto.encdec(
                Rotor96Crypto.DEC, password, ciphertext)

            decrypted_words = [word.lower() for word in decrypted_text.split()]
            for word in common_words:
                if word in decrypted_words:
                    possible_decipher[password] = decrypted_text
                    print(f"Key found: {password}")
                    print(
                        f"Found '{word}' in Decrypted text: \n{decrypted_text}")
                    print()
                    break

        except Exception as e:
            print(f"Error with key {password}: {e}")

    return possible_decipher


if __name__ == "__main__":
    ciphertext = load_text("../known_data/ciphertext2.txt")
    password_filename = "../passwords"

    print("Deciphering...")
    possible_decipher = cipher_only_attack(ciphertext, password_filename)
    print("Done.")

    if len(possible_decipher) > 0:
        with open(f"decrypted_text/decrypted_text2.txt", 'w') as f:
            f.write("key \t decrypted_text\n")
            for password, decrypted_text in possible_decipher.items():
                f.write(f"{password} \t {decrypted_text}\n")
