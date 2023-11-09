import requests
from bs4 import BeautifulSoup
import re
import subprocess
from termcolor import colored

u = int(input("Enter num country : \n1 - Iran\n2 - Turkey\n3 - Germany\n===> "))

if u == 1:
    url = "https://publicdnsserver.com/iran/"
elif u == 2:
    url = "https://publicdnsserver.com/turkey/"
elif u == 3:
    url = "https://publicdnsserver.com/germany/"
else:
    print("Invalid country selection")
    exit()

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    ip_addresses = [text for text in soup.stripped_strings if re.match(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', text)]

    for ip in ip_addresses:
        command = f'ping {ip}'
        result = subprocess.getoutput(command)
        lines = result.split('\n')
        if len(lines) >= 4:
            ping_info = lines[2]
            ping_time = ping_info.split()[-2]
            ping_time = ping_time.replace("time=", "").rstrip("ms")  # حذف "time=" و "ms"
            if ping_time and float(ping_time) < 100:
                colored_ip = colored(ip, 'green')
                print(f"IP: {colored_ip} - PING: {ping_time}")
            else:
                print(f"IP: {ip} - PING: {ping_time}")
else:
    print(f"خطا در درخواست وب‌سایت. وضعیت: {response.status_code}")
