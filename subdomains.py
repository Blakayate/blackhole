import requests
import os
from colors import info, warning, error

FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

def get_subdomains(domain, verbose):
    # Open subdomains list
    with open(FILE_DIR + "subdomains.txt") as f:
        sub_domains=f.read().splitlines()

    domain_count=len(sub_domains)
    count=1

    urls = list()
    info("Enumerating subdomains...")
    for sub_domain in sub_domains:
        url=f"http://{sub_domain}.{domain}"
        try:
            requests.get(url,timeout=2)
        except requests.exceptions.ReadTimeout:
            error('Request timed out')
        except requests.ConnectionError:
            if verbose:
                warning(f"{count}/{domain_count} Sub domain not found : {url}")
            pass
        except KeyboardInterrupt:
            error('Keyboard interruption')
            break
        else:
            # Append URL to list of URLs
            info(f"{count}/{domain_count} Sub domain found : {url}")
            urls.append(url)
        count += 1

    info('Enumeration finished')

    return urls