# Search for CVEs on https://nvd.nist.gov

import nvdlib
import re

# Take a dictionnary about a single service, build keyword and take other infos to build the final API request

def get_CVE(service):
    if 'product' in service:
        CVEs = list()
            
        # Build keyword for NVDLIB request
        if 'version' in service:
            # Extracting a 'correct' version pattern for keyword search
            r_version = re.match(r"(\d+\.)+\w{0,4}", service['version'])
            service['version'] = r_version.group()

            keyword = service["product"] + ' ' + service['version']
        else:
            keyword = service["product"]

        # Makes a NVD NIST API call and return an object
        cve_list = nvdlib.searchCVE(keyword=keyword)
        
        # Build a list of CVEs. Each item is a dictionnary
        index = 0
        for cve in cve_list:
            CVEs.append(dict())
            
            CVEs[index]["id"] = cve.id
            CVEs[index]["score"] = cve.score
            CVEs[index]["url"] = cve.url

            index += 1

        # Sort by score
        CVEs.sort(key=lambda item: item['score'][1], reverse=True)

        return CVEs
    else:
        return "Not enough enumeration info"