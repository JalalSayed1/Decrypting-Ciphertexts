from Rotor96Crypto import Rotor96Crypto


# Load passwords from file
def load_passwords(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def load_text(filename):
    with open(filename, 'r') as file:
        return file.read().strip()


def KPA_dictionary_attack(ciphertext, known_plaintext, password_file):
    passwords = load_passwords(password_file)
    possible_decipher = {}
    for password in passwords:
        try:
            # Rotor96Crypto.set_key(password)
            decrypted_text = Rotor96Crypto.encdec(
                Rotor96Crypto.DEC, password, ciphertext)
            if decrypted_text[:len(known_plaintext)] == known_plaintext:
                print(f"Key found: {password}")
                print(f"Decrypted text: {decrypted_text}")
                possible_decipher[password] = decrypted_text
                
        except Exception as e:
            print(f"Error with key {password}: {e}")
    
    if len(possible_decipher) == 0:
        print("Key not found in dictionary.")
        return None
    
    return possible_decipher


if __name__ == "__main__":

    ciphertext = load_text("../known_data/ciphertext1.txt")
    known_plaintext = load_text("../known_data/known_plaintext.txt")
    password_filename = "../passwords"  # File containing passwords

    print("Deciphering...")
    possible_decipher = KPA_dictionary_attack(ciphertext, known_plaintext, password_filename)
    print("Done.")
    
    if len(possible_decipher) > 0:
        with open(f"decrypted_text/decrypted_text1.txt", 'w') as f:
            f.write("key \t decrypted_text\n")
            for password, decrypted_text in possible_decipher.items():
                f.write(f"{password} \t {decrypted_text}\n")
