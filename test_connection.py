import socket
import sys

ip = "169.254.46.177"
ports = [22, 80, 443, 9559]

print(f"Testing connection to NAO at {ip}...")
for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        res = s.connect_ex((ip, port))
        if res == 0:
            print(f"Port {port}: OPEN")
        else:
            print(f"Port {port}: CLOSED / UNREACHABLE (error {res})")
    except Exception as e:
        print(f"Port {port}: Error -> {e}")
    finally:
        s.close()
