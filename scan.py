import nmap3
import json
import argparse

# Objet nmap
nmap = nmap3.Nmap()

# Objet argparse
args_parser = argparse.ArgumentParser(description="Blackhole : Pentest Toolbox")

# Création des arguments attendus
args_parser.add_argument(
    'target',
    help="Scan target",
)

# --tor : flag optionnel
args_parser.add_argument(
    '--tor',
    help="Route all trafic through Tor network.",
    action="store_true"
)

# Stock les **valeurs** des arguments passé a la ligne de commande.
args = args_parser.parse_args()


target = args.target

# test args
if args.tor:
    print("tor activated")

print(target)
#####

# Arguments custom
results = nmap.scan_top_ports(target, args="-sV -O")

# Sortie vers json + indentation pour lisibilité
with open("results.json", "w") as f:
    json.dump(results, f, indent=4)