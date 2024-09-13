import time
import random
import string
import asyncio
import aiohttp
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from datetime import datetime

percobaan = 20
nunggu = 20
output_file = "voucher.txt"
init(autoreset=True)
ua = UserAgent()

# Proxy configuration
proxy = 'http://z6sn7xy2xx7xonq:c8xcqq8rup12wgs@rp.proxyscrape.com:6060'

# Store all app tokens and promo IDs in a list of dictionaries
apps = [
    {'app_token': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af', 'promo_id': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af'}
]

def generate_client_id():
    timestamp = str(int(time.time() * 1000))
    random_digits = ''.join(random.choices(string.digits, k=19))
    return f"{timestamp}-{random_digits}"

def generate_event_id():
    first_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    second_part = ''.join(random.choices(string.digits, k=4))
    third_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    fourth_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    fifth_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"{first_part}-{second_part}-{third_part}-{fourth_part}-{fifth_part}"

async def get_promo_code(app_token: str, promo_id: str, max_attempts: int, event_timeout: int):
    headers = {"Content-Type": "application/json; charset=utf-8", "Host": "api.gamepromo.io", "User-Agent": ua.random}
    
    async with aiohttp.ClientSession(headers=headers) as http_client:
        client_id = generate_client_id()
        print(Fore.LIGHTCYAN_EX + "\rMulai...           ", end="", flush=True)

        # Send request through the proxy
        json_data = {"appToken": app_token, "clientId": client_id, "clientOrigin": "deviceid"}
        response = await http_client.post(url="https://api.gamepromo.io/promo/login-client", json=json_data, proxy=proxy)
        response_json = await response.json()
        access_token = response_json.get("clientToken")

        if not access_token:
            print(Fore.LIGHTRED_EX + f"\rCoba ambil token lagi..", end="", flush=True)
            return

        http_client.headers["Authorization"] = f"Bearer {access_token}"
        await asyncio.sleep(delay=1)

        attempts = 0
        while attempts <= max_attempts:
            try:
                event_id = generate_event_id()
                json_data = {"promoId": promo_id, "eventId": event_id, "eventOrigin": "undefined"}
                
                # Send request through the proxy
                response = await http_client.post(url="https://api.gamepromo.io/promo/register-event", json=json_data, proxy=proxy)
                response_json = await response.json()

                has_code = response_json.get("hasCode", False)
                if has_code:
                    json_data = {"promoId": promo_id}
                    response = await http_client.post(url="https://api.gamepromo.io/promo/create-code", json=json_data, proxy=proxy)
                    response_json = await response.json()
                    promo_code = response_json.get("promoCode")

                    if promo_code:
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m %H:%M:%S")
                        print(Fore.LIGHTGREEN_EX + f"\r[ {dt_string} ] Pocer: {promo_code}  ", flush=True)
                        with open(output_file, 'a') as f:
                            f.write(f"{promo_code}\n")
                        return promo_code
            except Exception as error:
                print(Fore.LIGHTRED_EX + f"\rErrore: {error}", flush=True)
            attempts += 1
            print(Fore.LIGHTRED_EX + f"\rGagal {attempts}x | Coba lagi ke-{attempts + 1}-> {event_timeout} detik", end="", flush=True)
            await asyncio.sleep(delay=event_timeout)
    print(Fore.LIGHTRED_EX + f"\r{max_attempts}x nyoba, gak nemu Voucher")

print(Fore.LIGHTBLUE_EX + "\rKEYGEN BIKE HAMSTER KOMBAT")
print(Fore.LIGHTCYAN_EX + f"\r t.me/unadavina             \n", end="", flush=True)

# Main loop to run promo for each app_token and promo_id
async def main():
    for app in apps:
        acak = random.randint(1, 5)
        await get_promo_code(app['app_token'], app['promo_id'], percobaan, nunggu)
        print(f"\rJeda acak: {acak} detik           ", end="", flush=True)
        time.sleep(acak)

# Run the main function
asyncio.run(main())
