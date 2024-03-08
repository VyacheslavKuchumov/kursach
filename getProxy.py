from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# enable headless mode in Selenium
options = Options()
options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)
# visit your target site
driver.get('https://free-proxy-list.net/')

soup = BeautifulSoup(driver.page_source, 'lxml')

proxies = soup.find_all('td')

proxyList = []
counter = 0
for index, proxy in enumerate(proxies):

    if counter == 0 or counter == 1:
        proxyList.append(proxy)
    if counter == 7:
        counter = 0
    else:
        counter +=1

    if index > 2000:
        break

cleanedProxyList = []
for p in proxyList:
    proxy = str(p)
    proxy = proxy.replace("<td>", "")
    proxy =  proxy.replace("</td>", "")
    cleanedProxyList.append(proxy)

finProxyList = []
for index, p in enumerate(cleanedProxyList):
    if (index+1) % 2 != 0:
        finProxyList.append(p)
    else:
        finProxyList[-1] += (":" + p)



with open("proxyList.txt", "w") as f:
    for proxy in finProxyList:
        f.write(proxy)
        f.write("\n")
