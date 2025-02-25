with open("../known_data/ciphertext1.txt") as f:
    ciphertext = f.read()
    print("Ciphertext: ", ciphertext)
    with open("../known_data/ciphertext1_ascii.txt", "w") as f2:
        for char in ciphertext:
            if char != " ":
                print(ord(char), end="")
                f2.write(str(ord(char)))
            else:
                print(char)
                f2.write("\n\n")

    print()
