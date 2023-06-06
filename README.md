# Blackhole
Multiplatform Pentest Toolbox  
 - Scan a target using nmap, retrieve CVEs and exploits. 
 - Enumerate subdomains
 - Bruteforce FTP and SSH

## Requirements

### Nmap
You have to install Nmap on your computer. 
https://nmap.org/download.html

### Chrome webdriver
Blackhole use Selenium and Chrome webdriver to retrieve exploits data from exploitdb.com  
You need Chrome webdriver installed in your system PATH (fastest way is to put webdriver in %system32%), check your Chrome version and install the corresponding webdriver version :  
https://chromedriver.chromium.org/downloads

## Installation
You must install all dependencies python dependencies using :
    
    pip install -r requirements.txt
