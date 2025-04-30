import requests
import time
import itertools
import random


def main():
    print("======== OROGOLD.APP WL REGISTRATION ========")
    print(f"Наши ресурсы:\n"
          f"Telegram-канал: @quantumlab_official\n"
          f"Продукты: @quantum_lab_bot\n\n")

    with open("emails.txt", "r", encoding="utf-8") as f:
        emails = [line.strip() for line in f if line.strip()]

    with open("proxies.txt", "r", encoding="utf-8") as f:
        proxies_list = [line.strip() for line in f if line.strip()]

    if len(emails)==0:
        print("[-] Нет emails для регистрации!")
        return

    proxy_cycle = itertools.cycle(proxies_list) if proxies_list else None

    result_filename = f"results_{str(int(time.time()))}.txt"
    error_filename = f"errors_{str(int(time.time()))}.txt"
    rnd_ua = random.randint(131, 134)
    rnd_win = random.randint(10, 11)

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://orogold.app/",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://orogold.app/",
        "sec-ch-ua": f'"Chromium";v="{rnd_ua}", "Not:A-Brand";v="24", "Google Chrome";v="{rnd_ua}"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": f"Mozilla/5.0 (Windows NT {rnd_win}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{rnd_ua}.0.0.0 Safari/537.36"
    }

    url = "https://orogold.app/api/email"

    success_results = []
    error_results = []

    for email in emails:
        proxy = next(proxy_cycle) if proxy_cycle else None

        session = requests.Session()
        if proxy:
            session.proxies = {
                "http": proxy,
                "https": proxy
            }

        payload = {"email": email}

        try:
            response = session.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get("error") is None:
                    resp_id = resp_json["data"][0]["id"]
                    success_results.append(f"{email}:{proxy if proxy else 'NO_PROXY'}:OK:{resp_id}")
                    print(f"[+] WL OK -> {email} | ID: {resp_id} : прокси {proxy if proxy else 'NO_PROXY'}")
                    session.close()
                else:
                    error_results.append(email)
                    print(f"[-] Ошибка для {email}: {resp_json}")
                    session.close()
            else:
                error_results.append(email)
                print(f"[-] Статус: {response.status_code} для {email}")
                session.close()

        except Exception as ex:
            error_results.append(email)
            print(f"[!] Исключение для {email}: {ex}")
            session.close()

        time.sleep(random.randint(2, 5))

    with open(result_filename, "a", encoding="utf-8") as r_file:
        for line in success_results:
            r_file.write(f"{line}\n")

    if error_results:
        with open(error_filename, "a", encoding="utf-8") as e_file:
            for email in error_results:
                e_file.write(f"{email}\n")

main()
print("\n\n======== OROGOLD.APP WL REGISTRATION ========")
print(f"Наши ресурсы:\n"
          f"Telegram-канал: @quantumlab_official\n"
          f"Продукты: @quantum_lab_bot\n\n")