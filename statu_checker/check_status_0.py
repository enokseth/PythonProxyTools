import requests
import socks
import socket
import re
import time
import itertools
from concurrent.futures import ThreadPoolExecutor

# Fonction pour charger les proxys à partir du fichier
def load_proxies_from_file(file_path):
    """Charge les proxys à partir d'un fichier texte."""
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip() and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', line.strip())]
    return proxies

# Fonction pour obtenir le pays d'un proxy
def get_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['country']
    except:
        return "Unknown"
    return "Unknown"

# Enregistrer les proxys fonctionnels
def save_working_proxy(proxy, proxy_type, country):
    with open(f'{proxy_type}_working_proxies.txt', 'a') as file:
        file.write(f"{proxy} - {country}\n")

# Tester un seul proxy
def test_single_proxy(proxy, url_to_test, proxy_type):
    ip, port = proxy.split(":")
    try:
        if proxy_type == 'http':
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            response = requests.get(url_to_test, proxies=proxy_dict, timeout=2)
        elif proxy_type == 'socks4':
            socks.set_default_proxy(socks.SOCKS4, ip, int(port))
            socket.socket = socks.socksocket
            response = requests.get(url_to_test, timeout=2)
        elif proxy_type == 'socks5':
            socks.set_default_proxy(socks.SOCKS5, ip, int(port))
            socket.socket = socks.socksocket
            response = requests.get(url_to_test, timeout=2)

        # Vérifier si le proxy fonctionne
        if response.status_code == 200:
            country = get_country(ip)  # Obtenir le pays du proxy
            print(f"Proxy {proxy} ({proxy_type.upper()}) fonctionne. Pays: {country}")
            save_working_proxy(proxy, proxy_type, country)  # Enregistrer les proxys qui fonctionnent
    except:
        pass

def test_proxies(proxies, url_to_test, proxy_type):
    """Teste chaque proxy en utilisant ThreadPoolExecutor pour une exécution rapide."""
    with ThreadPoolExecutor(max_workers=10) as executor:  # Ajuster max_workers selon tes besoins
        futures = [executor.submit(test_single_proxy, proxy, url_to_test, proxy_type) for proxy in proxies]
        for future in futures:
            future.result()  # On peut attraper les exceptions ici si nécessaire

if __name__ == "__main__":
    # Chemins des fichiers contenant les proxys
    http_proxies_file = 'http.txt'
    https_proxies_file = 'https.txt'
    socks4_proxies_file = 'socks4.txt'
    socks5_proxies_file = 'socks5.txt'

    # URL à tester
    url_to_test = 'http://httpbin.org/ip'

    # Charger les différents types de proxys
    http_proxies = load_proxies_from_file(http_proxies_file)
    https_proxies = load_proxies_from_file(https_proxies_file)
    socks4_proxies = load_proxies_from_file(socks4_proxies_file)
    socks5_proxies = load_proxies_from_file(socks5_proxies_file)

    # Tester les proxies
    print(f"Test des {len(http_proxies)} proxies HTTP...")
    test_proxies(http_proxies, url_to_test, 'http')

    print(f"Test des {len(https_proxies)} proxies HTTPS...")
    test_proxies(https_proxies, url_to_test, 'http')

    print(f"Test des {len(socks4_proxies)} proxies SOCKS4...")
    test_proxies(socks4_proxies, url_to_test, 'socks4')

    print(f"Test des {len(socks5_proxies)} proxies SOCKS5...")
    test_proxies(socks5_proxies, url_to_test, 'socks5')
