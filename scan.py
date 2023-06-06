import colors
from nmap3 import Nmap

def get_services(target, ports_range, verbose):
    nmap = Nmap()
    if ports_range:
        # Scan range
        nmap_args = '-T4 -sV -p ' + ports_range
    else:
        # Scan top ports
        nmap_args = '-T4 -sV'
    # nmap scan
    colors.info(f"Scanning {target} ...")
    output = nmap.scan_top_ports(target, args=nmap_args)
    
    # Extract relevant keys from nmap output
    service_info = ["name", "product", "version"]

    services = []
    index = 0

    # Loading the first key of output dictionnary to get data
    target = list(output.keys())[0]

    for port in output[target]["ports"]:
        services.append({})
        
        for info in service_info:
            try:
                services[index][info] = port["service"][info]
                # Get port ID
                services[index]['port'] = port['portid']
            except KeyError:
                if verbose:
                    colors.warning(f"{port['service']['name']} : No results about {info}")
                else:
                    pass

        index += 1

    return services