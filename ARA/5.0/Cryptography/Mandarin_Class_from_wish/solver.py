from random import randint

encrypted_flag = "㭪䫴㭪ひ灮带⯠⯠孨囖抸櫲婾懎囖崼敶栴囖溚⾈牂"  # Replace "..." with the actual encrypted flag you want to decrypt


decrypted_flag = ""

while True:
    key = randint(1,500)
    for e in encrypted_flag:
        d = chr(ord(e) // key)
        decrypted_flag += d
    if "ARA" in decrypted_flag:
        print(decrypted_flag)
        break
    else:
        print(key)

