import subprocess
import ipaddress
import sys

def block_ip_subnet(ip_subnet):
    if ip_subnet.version == 4:
        command = f"iptables -A INPUT -s {ip_subnet} -j DROP"
    elif ip_subnet.version == 6:
        command = f"ip6tables -A INPUT -s {ip_subnet} -j DROP"
    else:
        print(f"Invalid IP subnet: {ip_subnet}")
        return

    subprocess.run(command, shell=True, check=True)

def read_ip_subnets(filename):
    with open(filename, "r") as file:
        ip_subnets = file.readlines()
    ip_subnets = [subnet.strip() for subnet in ip_subnets]
    return ip_subnets

def main():
    filename = sys.argv[1]
    ip_subnets = read_ip_subnets(filename)

    for subnet in ip_subnets:
        try:
            ip_subnet = ipaddress.ip_network(subnet)
            block_ip_subnet(ip_subnet)
        except ValueError:
            print(f"Invalid IP subnet: {subnet}")


if __name__ == "__main__":
    main()