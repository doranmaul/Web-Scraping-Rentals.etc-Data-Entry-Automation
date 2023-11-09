from bs4 import BeautifulSoup
import requests
import lxml
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os
from pprint import pprint

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORMS_URL = "https://forms.gle/zMgex2TqZJ94EKu8A"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORMS_URL)

headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

contents = requests.get(ZILLOW_URL, headers=headers)
response = contents.text

soup = BeautifulSoup(response, "lxml")

# I want to get all anchor tags with class "property-card-link" then get href from those
# Then I want to find all elements that include text "property-card-price" or class -> they are spans with the class "PropertyCardWrapper__StyledPriceLine"
# Then find all <address> elements or all elements that have the text "property-card-addr"

property_links = []
for a in soup.find_all('a', href=True, class_="property-card-link"):
    property_links.append(a["href"])

property_prices = []
for span in soup.find_all('span', class_="PropertyCardWrapper__StyledPriceLine"):
    if "+" in span.text:
        new_price = span.text.split("+")[0]
    elif "/" in span.text:
        new_price = span.text.split("/")[0]
    property_prices.append(new_price)

property_addresses = []
for address in soup.find_all('address'):
    property_addresses.append(address.text.strip().replace(" |", ""))


pprint(property_links)
pprint(property_prices)
pprint(property_addresses)

num_loops = len(property_prices)

time.sleep(2)
for rentals in range(0, num_loops):
    driver.find_element(By.XPATH, '// input[ @ type = "text" and contains( @class , "whsOnd") and contains( @ class, "zHQkBf") and @ jsname="YPqjbf" and @ autocomplete="off" and @ tabindex="0" and @ aria-labelledby="i1" and @ aria-describedby="i2 i3" and @ dir="auto" and @ data-initial-dir="auto" and @ data-initial-value=""]').send_keys(property_addresses[rentals])  # enter address details on form
    driver.find_element(By.XPATH, '//input[@type="text" and contains(@class, "whsOnd") and contains(@class, "zHQkBf") and @jsname="YPqjbf" and @autocomplete="off" and @tabindex="0" and @aria-labelledby="i5" and @aria-describedby="i6 i7" and @dir="auto" and @data-initial-dir="auto" and @data-initial-value=""]').send_keys(property_prices[rentals]) # enter price details on form
    links = driver.find_element(By.XPATH, '//input[@type="text" and contains(@class, "whsOnd") and contains(@class, "zHQkBf") and @jsname="YPqjbf" and @autocomplete="off" and @tabindex="0" and @aria-labelledby="i9" and @aria-describedby="i10 i11" and @dir="auto" and @data-initial-dir="auto" and @data-initial-value=""]')
    links.send_keys(property_links[rentals])  # enter link details on form
    time.sleep(2)
    driver.find_element(By.XPATH, '//span[contains(@class, "NPEfkd") and contains(@class, "RveJvd") and contains(@class, "snByac")]').click()
    time.sleep(1)
    driver.get(FORMS_URL)

time.sleep(2)
driver.get("https://docs.google.com/forms/d/1DXyvzQiD63FtJh1I0KaQdmKL9FYkcj3Af4iR6vQWmic/edit#responses")
time.sleep(2)
driver.find_element(By.XPATH, '//div[@role="button" and contains(@class, "uArJ5e") and contains(@class, "cd29Sd") and contains(@class, "UQuaGc") and contains(@class, "kCyAyd") and contains(@class, "l3F1ye") and contains(@class, "M9Bg4d") and @aria-label="Link to Sheets"]').click()





#use split and strip and replace on address and price lists to get rid of unnecessary text/etc
