
with open("passwords") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if len(line) == 8:
            with open("passwords_8_chars.txt", "a") as f:
                f.write(line)