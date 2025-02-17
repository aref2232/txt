import requests
import os
import ipaddress

# URL of the text files
urls = [
    "https://raw.githubusercontent.com/firehol/blocklist-ipsets/refs/heads/master/firehol_anonymous.netset"
    # Add more URLs as needed
]

def fetch_ips(urls):
    ip_set = set()
    
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            for line in response.text.splitlines():
                line = line.strip()
                if line:
                    try:
                        if '/' in line:
                            network = ipaddress.ip_network(line, strict=False)
                            ip_set.update(str(ip) for ip in network)
                        else:
                            ip_set.add(line)
                    except ValueError:
                        print(f"Invalid IP or range: {line}")
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
    
    return ip_set

def split_ips(ip_set, max_per_file=120000):
    ip_list = sorted(ip_set)
    for i in range(0, len(ip_list), max_per_file):
        yield ip_list[i:i + max_per_file]

def save_files(ip_set):
    os.makedirs("output", exist_ok=True)

    # Split IPs and write to files
    for index, ip_chunk in enumerate(split_ips(ip_set)):
        file_name = f"output/ips_part_{index + 1}.txt"
        with open(file_name, 'w') as f:
            f.write("\n".join(ip_chunk))
        print(f"Wrote {len(ip_chunk)} IPs to {file_name}")

def main():
    ip_set = fetch_ips(urls)
    print(f"Total unique IPs: {len(ip_set)}")
    save_files(ip_set)

if __name__ == "__main__":
    main()
