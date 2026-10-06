

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import undetected_chromedriver as uc #   pip install undetected-chromedriver
 
url1 = "https://letterboxd.com/"
url2 = 

driver = uc.Chrome()


driver.get("https://letterboxd.com/")

time.sleep(2)


boton_aceptar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
)
boton_aceptar.click()

time.sleep(3)


boton_films = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navlink[href='/films/']"))
)
boton_films.click()

time.sleep(10)

driver.implicitly_wait(15)


driver.quit()