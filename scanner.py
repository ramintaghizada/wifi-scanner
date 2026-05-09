import scapy.all as scapy
import socket
import subprocess
import csv
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
from mac_vendor_lookup import MacLookup


init(autoreset=True)

logging.basicConfig(
    filename="network_scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Scanner started")



def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]

    except Exception:
        ip = '127.0.0.1'

    finally:
        s.close()

    return ip


def scan(ip_range):

    arp_request = scapy.ARP(pdst=ip_range)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(
        arp_request_broadcast,
        timeout=2,
        verbose=False
    )[0]

    clients = []

    for element in answered_list:

        client_dict = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc
        }

        clients.append(client_dict)

    return clients



def get_hostname(ip):

    try:
        return socket.gethostbyaddr(ip)[0]

    except:
        return "Unknown"



def get_vendor(mac):

    try:
        return MacLookup().lookup(mac)

    except:
        return "Unknown Vendor"



def ping_host(ip):

    result = subprocess.run(
        ["ping", "-c", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def scan_port(ip, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(1)

    result = s.connect_ex((ip, port))

    s.close()

    return result == 0



COMMON_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-ALT"
}


def process_device(client):

    ip = client['ip']
    mac = client['mac']

    hostname = get_hostname(ip)

    vendor = get_vendor(mac)

    alive = ping_host(ip)

    open_ports = []

    for port, service in COMMON_PORTS.items():

        if scan_port(ip, port):
            open_ports.append(f"{port}({service})")

    return {
        "ip": ip,
        "mac": mac,
        "hostname": hostname,
        "vendor": vendor,
        "alive": alive,
        "open_ports": open_ports
    }


def export_csv(results):

    with open("scan_results.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "IP",
            "MAC",
            "Hostname",
            "Vendor",
            "Alive",
            "Open Ports"
        ])

        for device in results:

            writer.writerow([
                device['ip'],
                device['mac'],
                device['hostname'],
                device['vendor'],
                device['alive'],
                ", ".join(device['open_ports'])
            ])



def export_json(results):

    with open("scan_results.json", "w") as file:

        json.dump(results, file, indent=4)



def main():

    my_ip = get_my_ip()

    print(Fore.CYAN + f"\nYour IP Address: {my_ip}")

    ip_parts = my_ip.split('.')

    network_range = (
        f"{ip_parts[0]}."
        f"{ip_parts[1]}."
        f"{ip_parts[2]}.0/24"
    )

    print(Fore.YELLOW + f"Scanning network: {network_range}\n")

    logging.info(f"Scanning network: {network_range}")

    scan_results = scan(network_range)

    detailed_results = []

    previous_devices = set()

    with ThreadPoolExecutor(max_workers=20) as executor:

        detailed_results = list(
            executor.map(process_device, scan_results)
        )

    current_devices = set(
        device['ip']
        for device in detailed_results
    )

    new_devices = current_devices - previous_devices

    if new_devices:

        print(Fore.GREEN + "\nNEW DEVICES DETECTED:")

        for device in new_devices:
            print(Fore.GREEN + f" - {device}")

    previous_devices = current_devices

    print(
        Fore.MAGENTA +
        "-" * 120
    )

    print(
        f"{'IP ADDRESS':<18}"
        f"{'MAC ADDRESS':<20}"
        f"{'HOSTNAME':<25}"
        f"{'VENDOR':<25}"
        f"{'STATUS':<10}"
        f"{'OPEN PORTS'}"
    )

    print(
        Fore.MAGENTA +
        "-" * 120
    )

    for device in detailed_results:

        status = (
            Fore.GREEN + "ONLINE"
            if device['alive']
            else Fore.RED + "OFFLINE"
        )

        print(
            f"{device['ip']:<18}"
            f"{device['mac']:<20}"
            f"{device['hostname']:<25}"
            f"{device['vendor']:<25}"
            f"{status:<18}"
            f"{', '.join(device['open_ports'])}"
        )

    export_csv(detailed_results)

    export_json(detailed_results)

    logging.info("Scan completed successfully")

    print(Fore.CYAN + "\nResults exported:")
    print(Fore.CYAN + " - scan_results.csv")
    print(Fore.CYAN + " - scan_results.json")
    print(Fore.CYAN + " - network_scanner.log")


if __name__ == "__main__":
    main()