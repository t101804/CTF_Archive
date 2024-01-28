import string
import itertools
import zipfile

fav_chars = ['kAor1', 's3nKu', 'sTev3', 'Lev1', 'L1Ly']

special_chars = {'*', '#', '!', '%', '&', '+'}

fav_numbers = list(range(10))

alphabet = list(string.ascii_uppercase)

combinations = itertools.product(
    range(1, 13),  # Months
    fav_chars,
    special_chars,
    fav_numbers,
    alphabet,
    special_chars
)

def bruteforce_password(zip_file_path, combinations):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for combination in combinations:
            month, fav_char, special_char, fav_number, alphabet_char, extra_special_char = combination
            password = f"{month}{fav_char}{special_char}{fav_number}{alphabet_char}{extra_special_char}"
            try:
                zip_file.extractall(pwd=password.encode())
                print(f"Password found: {password}")
                return password
            except Exception as e:
                if "Bad" not in e.__str__():
                    print(password)
                    print(e.__str__())
                    break
                print(e.__str__())
                continue

    print("Password not found")
    return None

if __name__ == "__main__":
    zip_file_path = r"new2.zip"  # Replace with the path to your repaired zip file
    bruteforce_password(zip_file_path, combinations)

