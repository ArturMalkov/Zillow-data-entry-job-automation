import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from time import sleep

#you can create your own Google Form containing three fields: link, price, and address or use the one below
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdeKRx2nWmaXTafN_blWgaixOj40De__DsqVVPt3cMwIq1fIg/viewform?usp=sf_link"
CHROME_DRIVER_PATH = "C:\Program Files\Development\chromedriver.exe"
#please provide your own link to Zillow rental search results based on your criteria
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
ZWSID = os.environ.get("ZWSID") #please register with Zillow API to obtain your own ZWSID (needs to be passed with the headers later)

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

#BeautifulSoup Section
headers = {
    ZWSID: ZWSID,
    "User-Agent": "My personal project/2.0",
    "language": "Python/3.9"
}

response = requests.get(ZILLOW_LINK, headers=headers)
zillow_html = response.text

soup = BeautifulSoup(zillow_html, "html.parser")

# links = soup.findAll(name='a', class_='list-card-link list-card-link-top-margin list-card-img')
links = soup.select(".list-card-top a")
prices = soup.findAll(name="div", class_="list-card-price")
addresses = soup.findAll(name="address", class_="list-card-addr")

links_list = []
for link in links:
    final_link = link['href']
    # print(final_link)
    if "http" not in final_link:
        links_list.append(f"https://www.zillow.com{final_link}")
    else:
        links_list.append(final_link)

# print(links_list)

prices_list = [price.string for price in prices]
# print(prices_list)

addresses_list = [address.string for address in addresses]
# print(addresses_list)

# Selenium Section
for n in range(len(links_list)):

    driver.get(GOOGLE_FORM_LINK)
    sleep(5)

    link_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(links_list[n])

    price_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(prices_list[n])

    address_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(addresses_list[n])

    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_button.click()


# You can later access all the Google Forms data in Google Sheets

################ GOING TO GOOGLE SHEETS#################
# edit_button = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]')
# edit_button.click()
#
# responses = driver.find_element_by_xpath('//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]/span/div')
# responses.click()
#
# view_in_sheets = driver.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div/span')
# view_in_sheets.click()
#
