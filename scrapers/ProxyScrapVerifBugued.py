import requests
import time
import random
import os
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Center, Write
import urllib3

# Désactiver les avertissements InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_request(url):
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        headers = {
            'User-Agent': UserAgent().random,
            'X-Forwarded-For': '.'.join(str(random.randint(0, 255)) for _ in range(4)),
        }

        response = session.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête à {url}: {e}")
        return b""

def save_file(file_path, url_list, protocol_name):
    valid_count = 0
    invalid_count = 0
    with open(file_path, 'wb') as f:
        for url in url_list:
            proxies = send_request(url)
            if proxies:
                f.write(proxies)
                f.write(b'\n')
                valid_count += 1
            else:
                invalid_count += 1
            
            # Mise à jour de l'affichage
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Colorate.Horizontal(Colors.purple_to_red, Center.XCenter(banner)))
            Write.Print(f"\n[+] Téléchargement des proxy {protocol_name} . . . \n", Colors.red_to_purple, interval=0)
            Write.Print(f"\nProxies valides : {valid_count} ", Colors.green, interval=0)
            Write.Print(f"Proxies invalides : {invalid_count}\n", Colors.red, interval=0)
    
    return valid_count, invalid_count

def check_proxies(file_path, protocol_name):
    valid_count = 0
    invalid_count = 0
    total_proxies = 0

    with open(file_path, 'r') as f:
        proxies = f.readlines()
    total_proxies = len(proxies)

    for index, proxy in enumerate(proxies):
        proxy = proxy.strip()
        try:
            response = requests.get("http://ipinfo.io/json", proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=5)
            if response.status_code == 200:
                valid_count += 1
            else:
                invalid_count += 1
        except:
            invalid_count += 1
        
        # Mise à jour de l'affichage
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Colorate.Horizontal(Colors.purple_to_red, Center.XCenter(banner)))
        Write.Print(f"\n[{protocol_name}] Vérification des proxy . . . \n", Colors.red_to_purple, interval=0)
        Write.Print(f"\nProxies valides : {valid_count} ", Colors.green, interval=0)
        Write.Print(f"Proxies invalides : {invalid_count}\n", Colors.red, interval=0)
        Write.Print(f"Total proxies vérifiés : {index + 1}/{total_proxies}\n", Colors.yellow, interval=0)
    
    return valid_count, invalid_count

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    global banner
    banner = '''                   
                                           
                                ╔══════════════════════════════════════════════╗
                                ║              PROXY SCRAPER 1.2.3             ║
                                ║              Crée par EnokSseth              ║
                                ║      PROTOCOLS: HTTP/S | SOCKS4 | SOCKS5     ║
                                ╚══════════════════════════════════════════════╝                                           
    '''
    print(Colorate.Horizontal(Colors.purple_to_red, Center.XCenter(banner)))

    os.system(f'title Proxy Scraper - Crée par: WxeneOne' if os.name == 'nt' else '')
    print()
    Write.Print("[+] Ce programme récupérera automatiquement les proxys dans des fichiers séparés", Colors.red_to_yellow, interval=0.01)
    print()

    # HTTP Proxies
    http_urls = [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-https.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxyscan.io/download?type=http",
        "https://www.proxyscan.io/download?type=https",
        "https://api.openproxylist.xyz/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt"
    ]

    http_valid, http_invalid = save_file('http.txt', http_urls, 'HTTP')
    Write.Print(f"[HTTP] Proxies valides : {http_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides : {http_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    # Vérifier les proxies HTTP
    http_valid, http_invalid = check_proxies('http.txt', 'HTTP')
    Write.Print(f"[HTTP] Proxies valides après vérification : {http_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides après vérification : {http_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    # SOCKS4 Proxies
    socks4_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://www.proxyscan.io/download?type=socks4",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt"
    ]

    socks4_valid, socks4_invalid = save_file('socks4.txt', socks4_urls, 'SOCKS4')
    Write.Print(f"[SOCKS4] Proxies valides : {socks4_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides : {socks4_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    # Vérifier les proxies SOCKS4
    socks4_valid, socks4_invalid = check_proxies('socks4.txt', 'SOCKS4')
    Write.Print(f"[SOCKS4] Proxies valides après vérification : {socks4_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides après vérification : {socks4_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    # SOCKS5 Proxies
    socks5_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://www.proxyscan.io/download?type=socks5",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
    ]

    socks5_valid, socks5_invalid = save_file('socks5.txt', socks5_urls, 'SOCKS5')
    Write.Print(f"[SOCKS5] Proxies valides : {socks5_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides : {socks5_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    # Vérifier les proxies SOCKS5
    socks5_valid, socks5_invalid = check_proxies('socks5.txt', 'SOCKS5')
    Write.Print(f"[SOCKS5] Proxies valides après vérification : {socks5_valid} ", Colors.green, interval=0)
    Write.Print(f"Proxies invalides après vérification : {socks5_invalid}\n", Colors.red, interval=0)
    time.sleep(1)

    print()
    print()
    Write.Print("Rejoignez le canal @waxeneone sur Telegram\n", Colors.red_to_yellow, interval=0.06)
    Write.Print("Appuyez sur n'importe quelle touche pour quitter . . .", Colors.white_to_red, interval=0)
    input()

if __name__ == "__main__":
    main()
