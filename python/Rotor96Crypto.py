import random


class Rotor96Crypto:
    ENC = 1  # Encryption mode
    DEC = 2  # Decryption mode

    started = False  # Indicates if the rotor system has been initialised
    rote = [None] * 8  # Forward rotor mappings
    rotd = [None] * 8  # Reverse rotor mappings
    offset = [0] * 8  # Rotor offsets for shifting
    # Step increments for each rotor
    increment = [5, 7, 11, 13, 19, 23, 29, 31]
    DEBUG_PRINT = False

    @staticmethod
    def encdec(mode, key, pt):
        """
        Encrypts or decrypts the given plaintext based on the mode.
        :param mode: ENC for encryption, DEC for decryption
        :param key: Encryption key
        :param pt: Plaintext or ciphertext (as string)
        :return: Transformed text (encrypted or decrypted)
        """
        Rotor96Crypto.set_key(key)  # Initialise key and rotors
        ctb = bytearray(pt, 'utf-8')  # Convert text to bytearray

        for i in range(len(pt)):
            b = ctb[i]
            if 32 <= b <= 127:  # Process only printable ASCII characters
                b -= 32  # Normalise to range 0-95
                if Rotor96Crypto.DEBUG_PRINT:
                    print(f"Initial byte {i}: {b}")

                for r in range(8):  # Pass through 8 rotors
                    if mode == Rotor96Crypto.ENC:
                        b = Rotor96Crypto.rote1(r, Rotor96Crypto.rote, b)
                    else:
                        b = Rotor96Crypto.rotd1(7 - r, Rotor96Crypto.rotd, b)
                    if Rotor96Crypto.DEBUG_PRINT:
                        print(
                            f"   After rotor {r} ({'ENC' if mode == Rotor96Crypto.ENC else 'DEC'}): {b}+32 = '{chr(b+32)}'")

                b += 32  # Convert back to ASCII range
                ctb[i] = b  # Store transformed byte

        return ctb.decode('utf-8')

    @staticmethod
    def rote1(r, rotor, b):
        """
        Forward transformation through rotor `r`.
        :param r: Rotor index
        :param rotor: Rotor mappings
        :param b: Input byte
        :return: Transformed byte
        """
        transformed_b = rotor[r][(b + Rotor96Crypto.offset[r]) % 96]
        if Rotor96Crypto.DEBUG_PRINT:
            print(
                f"   rote1 - Rotor {r}, Input {b}, Offset {Rotor96Crypto.offset[r]}, Output {transformed_b}")
        Rotor96Crypto.offset[r] = (
            Rotor96Crypto.offset[r] + Rotor96Crypto.increment[r]) % 96
        return transformed_b

    @staticmethod
    def rotd1(r, rotor, b):
        """
        Reverse transformation through rotor `r`.
        :param r: Rotor index
        :param rotor: Rotor mappings
        :param b: Input byte
        :return: Transformed byte
        """
        transformed_b = (rotor[r][b] + 96 - Rotor96Crypto.offset[r]) % 96
        if Rotor96Crypto.DEBUG_PRINT:
            print(
                f"   rotd1 - Rotor {r}, Input {b}, Offset {Rotor96Crypto.offset[r]}, Output {transformed_b}")
        Rotor96Crypto.offset[r] = (
            Rotor96Crypto.offset[r] + Rotor96Crypto.increment[r]) % 96
        return transformed_b

    @staticmethod
    def set_key(key):
        """
        Sets the key and initialises rotors if needed.
        :param key: Encryption key as a string
        """
        Rotor96Crypto.initialise()  # Ensure the system is initialised
        kb = bytearray(key, 'utf-8')
        length = len(kb)

        for r in range(8):  # Generate offsets based on key bytes
            b = kb[r % length]
            if b < 32 or b > 127:
                raise ValueError("Invalid key")
            Rotor96Crypto.offset[r] = b - 32
            if Rotor96Crypto.DEBUG_PRINT:
                print(f"Key offset for rotor {r}: {Rotor96Crypto.offset[r]}")

    @staticmethod
    def initialise():
        """
        Initialises the rotor mappings and marks the system as started.
        """
        if Rotor96Crypto.started:
            return  # Already initialised
        Rotor96Crypto.started = True

        Rotor96Crypto.rote[0] = [
            0, 79, 11,  9, 58,  2, 87, 32, 16, 42, 81, 31, 27, 34, 93, 37,
            29, 76, 19, 77, 94, 91, 38, 35, 10, 56,  5, 67, 68, 40, 43, 92,
            84, 89, 41,  8, 82, 15, 47, 39, 45, 20, 50,  4, 52, 75, 25, 83,
            21,  1, 26, 72, 69, 74, 80, 18, 70, 86, 30, 90, 17, 36, 33, 28,
            78, 13, 63, 46, 51, 53, 12, 55, 54, 85, 66,  3, 24, 48, 88, 49,
            23, 14, 62, 71, 65, 95, 64, 61, 44, 22, 60,  6, 57, 59,  7, 73
        ]
        Rotor96Crypto.rotd[0] = [
            0, 49,  5, 75, 43, 26, 91, 94, 35,  3, 24,  2, 70, 65, 81, 37,
            8, 60, 55, 18, 41, 48, 89, 80, 76, 46, 50, 12, 63, 16, 58, 11,
            7, 62, 13, 23, 61, 15, 22, 39, 29, 34,  9, 30, 88, 40, 67, 38,
            77, 79, 42, 68, 44, 69, 72, 71, 25, 92,  4, 93, 90, 87, 82, 66,
            86, 84, 74, 27, 28, 52, 56, 83, 51, 95, 53, 45, 17, 19, 64,  1,
            54, 10, 36, 47, 32, 73, 57,  6, 78, 33, 59, 21, 31, 14, 20, 85
        ]
        Rotor96Crypto.rote[1] = [
            92, 59, 28, 51, 91,  4, 93, 10, 66, 64, 23, 20, 37, 50, 48, 11,
            67, 14, 88, 27, 21, 90, 29, 70, 79, 60, 31, 61, 22, 15, 42, 80,
            16, 39, 32, 71,  3, 75, 33, 58, 25,  0, 53, 30, 72, 87, 63, 26,
            49, 43, 73, 41, 85, 38, 36, 13,  9,  8, 81, 44, 56, 35,  7, 68,
            62, 65, 82, 89, 17, 55, 12, 47, 78, 40,  1, 95, 84, 46, 34, 76,
            45, 57, 18, 77,  2, 83,  5, 74, 94,  6, 52, 86, 24, 69, 19, 54
        ]
        Rotor96Crypto.rotd[1] = [
            41, 74, 84, 36,  5, 86, 89, 62, 57, 56,  7, 15, 70, 55, 17, 29,
            32, 68, 82, 94, 11, 20, 28, 10, 92, 40, 47, 19,  2, 22, 43, 26,
            34, 38, 78, 61, 54, 12, 53, 33, 73, 51, 30, 49, 59, 80, 77, 71,
            14, 48, 13,  3, 90, 42, 95, 69, 60, 81, 39,  1, 25, 27, 64, 46,
            9, 65,  8, 16, 63, 93, 23, 35, 44, 50, 87, 37, 79, 83, 72, 24,
            31, 58, 66, 85, 76, 52, 91, 45, 18, 67, 21,  4,  0,  6, 88, 75
        ]
        Rotor96Crypto.rote[2] = [
            74, 56, 37, 27, 69, 30, 60, 93, 90, 65,  4, 49, 82, 66, 42, 92,
            89, 72, 78, 14, 40, 46, 73, 43, 16, 15, 39, 36,  5, 75, 32, 95,
            7, 52, 62, 34,  6, 48, 67, 80, 77, 33,  2, 64, 23, 26, 11, 71,
            35, 18, 88,  0, 21, 51, 59, 55, 10, 70, 17, 54, 61, 76, 57, 47,
            85, 22, 31,  8, 45, 63, 19, 86,  3, 87, 20, 68, 94, 24,  1, 29,
            83,  9, 84, 79, 41, 58, 50, 38, 44, 25, 28, 53, 12, 81, 91, 13
        ]
        Rotor96Crypto.rotd[2] = [
            51, 78, 42, 72, 10, 28, 36, 32, 67, 81, 56, 46, 92, 95, 19, 25,
            24, 58, 49, 70, 74, 52, 65, 44, 77, 89, 45,  3, 90, 79,  5, 66,
            30, 41, 35, 48, 27,  2, 87, 26, 20, 84, 14, 23, 88, 68, 21, 63,
            37, 11, 86, 53, 33, 91, 59, 55,  1, 62, 85, 54,  6, 60, 34, 69,
            43,  9, 13, 38, 75,  4, 57, 47, 17, 22,  0, 29, 61, 40, 18, 83,
            39, 93, 12, 80, 82, 64, 71, 73, 50, 16,  8, 94, 15,  7, 76, 31
        ]
        Rotor96Crypto.rote[3] = [
            20, 35, 56, 38, 37, 77, 13, 91, 64, 11, 94, 14, 47,  5, 73, 79,
            82, 49, 51, 44,  3, 22, 34, 40, 30, 54, 74, 24,  2, 95, 89, 61,
            66, 33, 45, 42,  7, 25, 41, 16,  8, 27, 29, 10, 92, 88, 21, 12,
            55, 53, 65, 58, 15, 86, 50, 57, 32,  4, 93, 43,  0, 70, 19, 69,
            59, 48, 80, 60,  6, 72, 75, 39, 78, 83, 90, 63, 87,  1, 31, 28,
            81, 23, 46, 62, 36, 26, 17, 84, 76, 68, 52, 71, 67,  9, 85, 18
        ]
        Rotor96Crypto.rotd[3] = [
            60, 77, 28, 20, 57, 13, 68, 36, 40, 93, 43,  9, 47,  6, 11, 52,
            39, 86, 95, 62,  0, 46, 21, 81, 27, 37, 85, 41, 79, 42, 24, 78,
            56, 33, 22,  1, 84,  4,  3, 71, 23, 38, 35, 59, 19, 34, 82, 12,
            65, 17, 54, 18, 90, 49, 25, 48,  2, 55, 51, 64, 67, 31, 83, 75,
            8, 50, 32, 92, 89, 63, 61, 91, 69, 14, 26, 70, 88,  5, 72, 15,
            66, 80, 16, 73, 87, 94, 53, 76, 45, 30, 74,  7, 44, 58, 10, 29
        ]
        Rotor96Crypto.rote[4] = [
            8, 80, 94, 87, 79, 67, 11, 65, 53, 62, 61, 73, 66, 55, 27, 41,
            25, 83,  0, 90, 13, 28, 37,  3, 77, 59, 89, 72, 39, 85, 26, 43,
            52,  1, 32, 17, 33,  7, 23, 15, 18, 24, 51, 47,  9, 81, 30, 68,
            29,  2, 58, 19, 78, 56, 76, 63,  6, 54, 21, 10, 42, 49, 44, 71,
            91, 35, 60, 34, 86, 64, 92, 16, 46, 38, 20, 82, 70, 40, 14, 57,
            31, 12, 22, 88, 75, 93,  5, 45, 50, 74, 84, 36, 69, 95, 48,  4
        ]
        Rotor96Crypto.rotd[4] = [
            18, 33, 49, 23, 95, 86, 56, 37,  0, 44, 59,  6, 81, 20, 78, 39,
            71, 35, 40, 51, 74, 58, 82, 38, 41, 16, 30, 14, 21, 48, 46, 80,
            34, 36, 67, 65, 91, 22, 73, 28, 77, 15, 60, 31, 62, 87, 72, 43,
            94, 61, 88, 42, 32,  8, 57, 13, 53, 79, 50, 25, 66, 10,  9, 55,
            69,  7, 12,  5, 47, 92, 76, 63, 27, 11, 89, 84, 54, 24, 52,  4,
            1, 45, 75, 17, 90, 29, 68,  3, 83, 26, 19, 64, 70, 85,  2, 93
        ]
        Rotor96Crypto.rote[5] = [
            81, 87, 61, 94, 19, 77, 10, 59, 55, 90, 11, 91,  7, 12, 32, 82,
            52, 42, 13, 27, 79,  6, 46, 68, 43, 23, 15, 39,  9, 14,  0, 44,
            4, 56, 31, 28, 66, 21, 54, 49, 47, 24, 84, 26, 74, 88, 29, 76,
            73, 50, 67, 63, 62,  2, 57, 51, 17, 89,  1, 48,  3, 20, 41, 40,
            69, 37, 64, 38, 95,  8, 85, 22, 58, 53, 75, 35, 80, 36, 78, 71,
            5, 65, 25, 86, 60, 92, 83, 30, 34, 16, 72, 70, 18, 33, 93, 45
        ]
        Rotor96Crypto.rotd[5] = [
            30, 58, 53, 60, 32, 80, 21, 12, 69, 28,  6, 10, 13, 18, 29, 26,
            89, 56, 92,  4, 61, 37, 71, 25, 41, 82, 43, 19, 35, 46, 87, 34,
            14, 93, 88, 75, 77, 65, 67, 27, 63, 62, 17, 24, 31, 95, 22, 40,
            59, 39, 49, 55, 16, 73, 38,  8, 33, 54, 72,  7, 84,  2, 52, 51,
            66, 81, 36, 50, 23, 64, 91, 79, 90, 48, 44, 74, 47,  5, 78, 20,
            76,  0, 15, 86, 42, 70, 83,  1, 45, 57,  9, 11, 85, 94,  3, 68
        ]
        Rotor96Crypto.rote[6] = [
            28, 32,  8, 53, 84, 52,  3, 95, 77, 75, 78, 14, 68, 76, 44, 81,
            67, 69, 27, 79, 42, 38, 16, 37, 41,  7, 80, 86, 90, 82, 92, 33,
            10,  2, 11, 34, 12, 49, 35, 22, 18, 19, 46, 63, 50, 85, 88, 93,
            21, 56, 83, 23, 66, 24, 26, 47,  4, 71, 20, 51, 70, 55, 43, 74,
            87,  6, 64,  1, 17, 36, 48, 45, 62, 61, 13, 15, 65,  5, 29, 94,
            30, 58,  9, 25, 60,  0, 91, 89, 40, 72, 54, 31, 73, 59, 57, 39
        ]
        Rotor96Crypto.rotd[6] = [
            85, 67, 33,  6, 56, 77, 65, 25,  2, 82, 32, 34, 36, 74, 11, 75,
            22, 68, 40, 41, 58, 48, 39, 51, 53, 83, 54, 18,  0, 78, 80, 91,
            1, 31, 35, 38, 69, 23, 21, 95, 88, 24, 20, 62, 14, 71, 42, 55,
            70, 37, 44, 59,  5,  3, 90, 61, 49, 94, 81, 93, 84, 73, 72, 43,
            66, 76, 52, 16, 12, 17, 60, 57, 89, 92, 63,  9, 13,  8, 10, 19,
            26, 15, 29, 50,  4, 45, 27, 64, 46, 87, 28, 86, 30, 47, 79,  7
        ]
        Rotor96Crypto.rote[7] = [
            84,  9, 78, 81, 79, 70, 52, 56, 24, 49, 13, 23, 83, 53, 80, 28,
            64, 74, 40, 63, 77, 58, 82,  4, 16, 41, 22, 39, 51, 65, 26, 87,
            17, 91, 10,  2,  8, 43, 38, 68,  0, 61, 46, 89, 90, 35, 29, 30,
            32, 42, 62, 67, 27, 69, 15, 73, 50,  1,  3, 76, 47, 19, 14, 21,
            12, 18, 48,  7, 85,  6, 71, 86, 66, 37, 94, 54, 20, 92, 72, 31,
            33, 95, 57, 36, 55, 88, 75, 25, 45, 59, 60, 93, 34, 44, 11,  5
        ]
        Rotor96Crypto.rotd[7] = [
            40, 57, 35, 58, 23, 95, 69, 67, 36,  1, 34, 94, 64, 10, 62, 54,
            24, 32, 65, 61, 76, 63, 26, 11,  8, 87, 30, 52, 15, 46, 47, 79,
            48, 80, 92, 45, 83, 73, 38, 27, 18, 25, 49, 37, 93, 88, 42, 60,
            66,  9, 56, 28,  6, 13, 75, 84,  7, 82, 21, 89, 90, 41, 50, 19,
            16, 29, 72, 51, 39, 53,  5, 70, 78, 55, 17, 86, 59, 20,  2,  4,
            14,  3, 22, 12,  0, 68, 71, 31, 85, 43, 44, 33, 77, 91, 74, 81
        ]


if __name__ == "__main__":
    def random_string(length):
        return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length))

    # key = random_string(8)
    key = "OcmagHu8"
    pt = "Hello"
    ct = Rotor96Crypto.encdec(Rotor96Crypto.ENC, key, pt)

    Rotor96Crypto.DEBUG_PRINT = True

    if Rotor96Crypto.DEBUG_PRINT:
        print(f"Key: {key}")
    if Rotor96Crypto.DEBUG_PRINT:
        print(f"EncRotor('{pt}'): '{ct}'")
    if Rotor96Crypto.DEBUG_PRINT:
        print()
    # pt = Rotor96Crypto.encdec(Rotor96Crypto.DEC, key, ct)
    # if Rotor96Crypto.DEBUG_PRINT:
    # print(f"DecRotor('{ct}'): '{pt}'")
