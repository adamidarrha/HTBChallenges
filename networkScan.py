import os
import argparse

def run_network_scan(ip_address, interface = 'tun0'):
    # Command 1: Run masscan
    masscan_command = f"masscan -p1-65535 {ip_address} --rate=1000 -e {interface} -oG masscan_output"
    print(f"Running masscan on {ip_address}...")
    os.system(masscan_command)

    # Command 2: Process the results to get the list of ports
    print("Processing the port list...")
    with open('masscan_output', 'r') as file:
        lines = file.readlines()

    ports = ','.join(sorted(set(line.split()[3].split('/')[0] for line in lines if line.strip())))

    # Command 3: Run nmap
    if ports:
        nmap_command = f"nmap -Pn -sV -sC -p{ports} {ip_address}"
        print(f"Running nmap on {ip_address} with ports {ports}...")
        os.system(nmap_command)
    else:
        print("no ports found")

# Create the parser
parser = argparse.ArgumentParser(description="Run a network scan")

# Add the arguments
parser.add_argument("ip_address", type=str, help="The IP address to scan")
parser.add_argument("--interface", type=str, default='tun0', help="The network interface to use")

# Parse the arguments
args = parser.parse_args()

# Call the function with the arguments
run_network_scan(args.ip_address, args.interface)
