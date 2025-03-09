# Decrypting-Ciphertexts

This exercise involves decrypting two different pieces of ciphertext using two different methods to find the encryption keys and the original plaintext messages.

## How To Run

To run the Java version:

```bash
cd <project_dir>

javac rotor96Crypto/*.java

java rotor96Crypto.KPA # to run the Known Plaintext Attack
java rotor96Crypto.COA # to run the Ciphertext Only Attack
```

To run the Python version:

```bash
cd <project_dir/python>

python KPA.py # to run the Known Plaintext Attack
python COA.py # to run the Ciphertext Only Attack
```

## Problem Statement

1. All of the secret messages have been encyrpted by an 8-rotor encryption machine called Rotor96Crypto.
2. All keys have been taken from a file of common passwords called 'passwords'.
3. The ciphertexts are stored in 'ciphertext1.txt' and 'ciphertext2.txt'.
4. The first two letters of the plaintext are 'We' and it's stored in 'plaintext_start_chars.txt'.
5. Two methods are used to decrypt the ciphertexts:
    - **Known Plaintext Attach (KPA)**: The first two letters of the plaintext are known.
    - **Ciphertext Only Attack (COA)**: Only the ciphertext is known.

## Rotor96 Encryption & Decryption Equations  

### 1. **Normalisation**  

Convert input character to a byte value in range `[0, 95]`:  

$$
B = \text{ord}(P) - 32
$$

### 2. **Encryption Process**  

For each rotor \( k \) (from `0` to `7`):  

$$
B = R_k(B) = \text{rotor}[k] \left( (B + O_k) \mod 96 \right)
$$

After transformation, update rotor offset:  

$$
O_k = (O_k + I_k) \mod 96
$$

Final ASCII conversion:  

$$
C = B + 32
$$

### 3. **Decryption Process**  

For each rotor \( k \) (from `7` to `0`):  

$$
B = R_k^{-1}(B) = (\text{rotor}[k][B] + 96 - O_k) \mod 96
$$

Update rotor offset:  

$$
O_k = (O_k + I_k) \mod 96
$$

Final ASCII conversion:  

$$
P = B + 32
$$

### 4. **Overall Encryption Equation**  

$$
C_i = R_7(R_6(R_5(R_4(R_3(R_2(R_1(R_0(B_i))))))))
$$

### 5. **Overall Decryption Equation**  

$$
P_i = R_0^{-1}(R_1^{-1}(R_2^{-1}(R_3^{-1}(R_4^{-1}(R_5^{-1}(R_6^{-1}(R_7^{-1}(B_i))))))))
$$

Each rotor transformation introduces a key-dependent substitution, making the encryption scheme a polyalphabetic cipher similar to classical rotor-based encryption machines.

## Known Plaintext Attack (KPA)

Given a chunk of ciphertext with the first two characters of the plaintext, perform a dictionary attach to find the key. Use this key to decode the rest of the message.

## Ciphertext Only Attack (COA)

Given another chunk of ciphertext but with no information about the plaintext, perform a dictionary attack but this time decide whether a key produces the correct plaintext given that the plaintext is an English message.
