import socket
import re
from common_ports import ports_and_services

default_timeout = 3

def is_ip(target):
    ip_regex = "^\\d{1,3}(\\.\\d{1,3}){3}$" 
    is_ip = False
    if re.search(ip_regex, target):
        is_ip = True

    return is_ip

def get_open_ports(target, port_range, verbose = False):
    is_ip_format = is_ip(target)
    ip = ''
    host = ''

    if is_ip_format:
        ip = target
        try:
            host_info = socket.gethostbyaddr(target)
            host = host_info[0]
        except:
            return "Error: Invalid IP address"
    else:
        host = target
        try:
            ip = socket.gethostbyname(target)
        except:
            return "Error: Invalid hostname"
    
    print(f"host: {host}, ip: {ip}")

    open_ports = []

    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(default_timeout)
            # returning zero means success
            if not s.connect_ex((target, port)):
                open_ports.append(port)

    if verbose:
        verbose_result = f"Open ports for {host} ({ip})\nPORT     SERVICE"
        for port in open_ports:
            space_length = 9
            space_length = space_length - len(str(port))
            space = ' ' * space_length
            service_name = ports_and_services.get(port, port)
            verbose_result += f"\n{port}{space}{service_name}"

        return(verbose_result)

    return(open_ports)