from bs4 import BeautifulSoup as bs
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def scrape_cis(url) -> set:
    driver = webdriver.Firefox()
    driver.get(url)
    refresh = True
    driver.implicitly_wait(4)
    wait = WebDriverWait(driver, timeout=20,ignored_exceptions=(NoSuchElementException))
    while refresh:
        try:
            wait.until(lambda d : driver.find_element(By.CLASS_NAME, "pdfViewer").is_displayed())
        except TimeoutException:
            driver.refresh()
        else:
            refresh = False
    a = ActionChains(driver)
    layer = driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/span/div/span/div/main/div/div/div/div/div/div[2]/div[1]/div[5]")
    ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/span/div/span/div/main/div/div/div/div/div/div[2]/div[1]/div[5]/div/div[1]/div[2]/div/button[2]")
    a.move_to_element(layer).click(ele)
    a.move_to_element(layer).click(ele)
    a.move_to_element(layer).click(ele)
    a.move_to_element(layer).click(ele)
    
    webpage = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = bs(webpage, "html.parser")
    pdf = soup.find("div", attrs={"class" : "pdfViewer"})
    ci_set = list()
    i = 1
    
    while (pdf.find("div", attrs={"id" : "bp-page-" + str(i)}) != None):
        page = pdf.find("div", attrs={"id" : "bp-page-" + str(i)})
        print(page)
        objects = page.find_all("span")
        for obj in objects:
            if "style" in obj.attrs and "left: 12.71%" in obj.attrs['style']:
                temp = str(obj.text)
                course = temp.rsplit("-", 1)[0]
                if len(course) != 9:
                    continue
                ci_set.append(course)
        i += 1
    print(ci_set)
    driver.quit()
    
    

scrape_cis("https://rpi.app.box.com/s/d4ihh7yh5kyj4g2r04r8xpmi5ru7vog5/file/1550366279837")