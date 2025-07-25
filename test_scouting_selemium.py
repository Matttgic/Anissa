from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from webdriver_manager.chrome import ChromeDriverManager

def get_scouting_report_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    # Attendre un peu que la page charge (FBref est rapide, 2s suffisent)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    report = {}
    scouting_table = soup.find("table", {"id": "scout_summary"})
    if not scouting_table:
        print("❌ Scouting Report introuvable (même avec Selenium).")
        return report

    for row in scouting_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            stat_name = cells[0].text.strip()
            percentile = cells[1].text.strip()
            if percentile.isdigit():
                report[stat_name] = int(percentile)

    return report

if __name__ ==
