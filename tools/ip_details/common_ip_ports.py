import os
import socket

from ipwhois import IPWhois


def get_ip_details(ip_address):
    obj = IPWhois(ip_address)
    results = obj.lookup_rdap(depth=1)
    return results


def scan_ports(ip_address):
    # List of common ports to check
    common_ports = {
        21: 'FTP',
        22: 'SSH',
        23: 'TELNET',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        587: 'SMTP',
        993: 'IMAPS',
        995: 'POP3S',
        3306: 'MYSQL',
        3389: 'RDP',
        5432: 'POSTGRESQL',
        5900: 'VNC',
        8080: 'HTTP-ALT'
    }

    open_ports = {}

    for port, service in common_ports.items():
        try:
            with socket.create_connection((ip_address, port), timeout=1) as s:
                open_ports[port] = service
        except (socket.timeout, socket.error):
            pass

    return open_ports


ip_address = "138.197.121.207"

result = scan_ports(ip_address)
details = get_ip_details(ip_address)

print(f"Below is the Details related to IP: {ip_address}")
for key, value in details.items():
    print(f"{key}: {value}")


def get_running_services():
    services = os.popen('systemctl list-units --type=service --state=running').read()
    return services


def get_listening_ports():
    ports = os.popen('ss -tuln').read()
    return ports


print("Running Services:\n")
print(get_running_services())

print("\nListening Ports:\n")
print(get_listening_ports())

if result:
    print(f"Open ports on {ip_address}:")
    for port, service in result.items():
        print(f"Port {port}: {service}")
else:
    print(f"No common ports are open on {ip_address}.")
