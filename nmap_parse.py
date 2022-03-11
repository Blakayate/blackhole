import json
import logs

def get_services(target, output):
    output = json.load(output)

    # Keys from nmap output that we want to parse.
    service_info = ["name", "product", "version"]

    services = []
    index = 0

    for port in output[target]["ports"]:
        services.append({})

        for info in service_info:
            try:
                services[index][info] = port["service"][info]
            except KeyError:
                logs.warning(f"{port['service']['name']} : No result about {info}")

        index += 1

    return services
    
# print(json.dumps(services, indent=4))
# print("\n\n")