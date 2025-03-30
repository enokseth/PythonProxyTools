import requests
import re
import time
import os
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Center, Write
import urllib3

# Désactiver les avertissements InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_request(url):
    """Envoie une requête à l'URL et retourne le contenu."""
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        headers = {
            'User-Agent': UserAgent().random,
        }

        response = session.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        return response.text.splitlines()  # Retourner une liste de proxys
    except requests.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête à {url}: {e}")
        return []

def save_file(file_path, proxies):
    """Enregistre les proxys dans le fichier sans ajouter de type."""
    with open(file_path, 'a') as f:
        for proxy in proxies:
            f.write(f"{proxy.strip()}\n")

def process_proxies(urls, proxy_type, file_path):
    """Processus pour récupérer et enregistrer les proxys, et afficher un compteur."""
    all_proxies = []

    proxy_count = 0  # Compteur de proxys

    # Regex pour extraire l'hôte de l'URL
    regex = r'https?://([^/]+)'
    
    # Regex pour extraire le nom d'utilisateur GitHub
    username_regex = r'https?://raw\.githubusercontent\.com/([^/]+)/'

    for url in urls:
        proxies = send_request(url)
        all_proxies.extend(proxies)

        # Compteur mis à jour pour chaque URL traitée
        proxy_count += len(proxies)

        # Extraire l'hôte
        match = re.search(regex, url)
        host = match.group(1) if match else "Inconnu"

        # Extraire l'utilisateur si c'est un dépôt GitHub
        username_match = re.search(username_regex, url)
        username = username_match.group(1) if username_match else "Inconnu"

        # Pour les dépôts GitHub, ajuster le format
        if "github.com" in host:
            host = "github + " + host.split('.')[0]

        # Afficher le compteur en fonction du type de proxy
        if proxy_type == 'HTTP':
            print(Colorate.Horizontal(Colors.green_to_blue, f"[+] HTTP Proxys récupérés: {proxy_count} [+] Hôte: {host} [+] Utilisateur: {username}", 1))
        elif proxy_type == 'HTTPS':
            print(Colorate.Horizontal(Colors.blue_to_red, f"[+] HTTPS Proxys récupérés: {proxy_count} [+] Hôte: {host} [+] Utilisateur: {username}", 1))
        elif proxy_type == 'SOCKS4':
            print(Colorate.Horizontal(Colors.purple_to_red, f"[+] SOCKS4 Proxys récupérés: {proxy_count} [+] Hôte: {host} [+] Utilisateur: {username}", 1))
        elif proxy_type == 'SOCKS5':
            print(Colorate.Horizontal(Colors.red_to_yellow, f"[+] SOCKS5 Proxys récupérés: {proxy_count} [+] Hôte: {host} [+] Utilisateur: {username}", 1))

    # Enregistrer les proxys dans un fichier
    save_file(file_path, all_proxies)

    return proxy_count 

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    banner = '''                   
                                ╔══════════════════════════════════════════════╗
                                ║              PROXY SCRAPER 1.3.4             ║
                                ║              Crée par EnokSseth              ║
                                ║      PROTOCOLS: HTTP/S | SOCKS4 | SOCKS5     ║
                                ╚══════════════════════════════════════════════╝                                           
    '''
    print(Colorate.Horizontal(Colors.purple_to_red, Center.XCenter(banner)))

    print()
    Write.Print("[+] Ce programme récupérera automatiquement les proxys dans des fichiers séparés", Colors.red_to_yellow, interval=0.01)
    print()

    # URLs pour les proxys HTTP
    http_urls = [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://api.openproxylist.xyz/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    ]

    # Récupérer et enregistrer les proxys HTTP
    total_http = process_proxies(http_urls, 'HTTP', 'http.txt')

    # URLs pour les proxys HTTPS
    https_urls = [
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-https.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://www.proxy-list.download/api/v1/get?type=https",
    ]

    # Récupérer et enregistrer les proxys HTTPS
    total_https = process_proxies(https_urls, 'HTTPS', 'https.txt')

    # URLs pour les proxys SOCKS4
    socks4_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://api.openproxylist.xyz/socks4.txt",
    ]

    # Récupérer et enregistrer les proxys SOCKS4
    total_socks4 = process_proxies(socks4_urls, 'SOCKS4', 'socks4.txt')

    # URLs pour les proxys SOCKS5
    socks5_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://api.openproxylist.xyz/socks5.txt",
    ]

    # Récupérer et enregistrer les proxys SOCKS5
    total_socks5 = process_proxies(socks5_urls, 'SOCKS5', 'socks5.txt')

    ####### PRINT LE NOMBRE DE PROXIES 
    Write.Print(f"[+] Total des proxies HTTP : {total_http}", Colors.red, interval=0.03)
    Write.Print(f"[+] Total des proxies HTTPS : {total_https}", Colors.orange, interval=0.03)
    Write.Print(f"[+] Total des proxies SOCKS4 : {total_socks4}", Colors.cyan, interval=0.03)
    Write.Print(f"[+] Total des proxies SOCKS5 : {total_socks5}", Colors.green, interval=0.03)
    Write.Print(f"[+] Total des proxies SOCKS5 : {total_socks5}", Colors.green, interval=0.03)
    Write.Print("[+] Récupération des proxys terminée.", Colors.green, interval=0.01)

if __name__ == "__main__":
    main()
