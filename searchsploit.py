from colors import info, warning
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def searchsploit_by_cve(cve, verbose):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)

    url = f"https://www.exploit-db.com/search?cve={cve}"
    search_result_xpath = "//table[@id='exploits-table']/tbody/tr"
    
    if verbose:
        info(f"Looking for {cve}'s exploits...")
        
    driver.get(url)

    # Waiting for search results to appear
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, search_result_xpath))
    )

    # Result of the research
    results_row = driver.find_elements(By.XPATH, search_result_xpath)

    # Get exploit's webpage and download links in a list
    exploits = list()

    # Look for the presence of class "dataTables_empty", returns a list. If the list is empty, then the class isn't present = edb search returned data/exploits list
    if driver.find_elements(By.CLASS_NAME, "dataTables_empty"):
        exploits.append("No data available")
        if verbose:
            warning("No data available")
    else:
        if verbose:
            info("Got them !")
        for row in results_row:

            # Select all <a> tags
            anchors = row.find_elements(By.TAG_NAME, "a")

            # Extract each value of href attributes using list comprehension
            links = [elem.get_attribute('href') for elem in anchors]

            exploits_links = {
                "exploitdb_link" : "",
                "download_link" : ""
                }

            for link in links:
                if 'download' in link:
                    exploits_links["download_link"] = link
                elif 'exploits' in link:
                    exploits_links["exploitdb_link"] = link
                
            exploits.append(exploits_links)
    driver.quit()
    return exploits