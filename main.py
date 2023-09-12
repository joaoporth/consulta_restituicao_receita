import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import base64

PROXY_HOST = 'zproxy.lum-superproxy.io'
PROXY_PORT = 22225
PROXY_USER = 'brd-customer-hl_c4113741-zone-data_center-country-br'
PROXY_PASS = 'nwlgbfb867og' # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "https",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        service=ChromeService(ChromeDriverManager().install()),
        chrome_options=chrome_options)

    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    #driver.get('http://www.httpbin.org/ip')
    driver.get('https://www.restituicao.receita.fazenda.gov.br/#/')
    #print(driver.find_element(By.TAG_NAME, "body").text)

    wait = WebDriverWait(driver, 10)

    try:

        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'flt-glass-pane')))


        element.click()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    for i in range(4):
        driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.TAB)
        time.sleep(1)

    cpf = ''
    driver.find_element(By.TAG_NAME ,'body').send_keys(cpf)
    time.sleep(1)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.TAB)

    dataNascimento = ''
    driver.find_element(By.TAG_NAME ,'body').send_keys(dataNascimento)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.TAB)
    time.sleep(1)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.TAB)
    time.sleep(1)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.SPACE)
    time.sleep(1)

    currentYear = int(time.strftime('%Y'))
    year = 2022
    downs = currentYear - year

    for _ in range(downs + 1):
        driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.ARROW_DOWN)
        time.sleep(1)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.SPACE)
    time.sleep(1)

    captcha_element = driver.find_element(By.CSS_SELECTOR,'.h-captcha')
    captcha_element.click()

    for _ in range(6):
        driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.TAB)

    driver.find_element(By.TAG_NAME ,'body').send_keys(Keys.SPACE)
    time.sleep(10)

    screenshot = driver.get_screenshot_as_base64()

    driver.quit()

    with open('screenshot.png', 'wb') as file:
        file.write(base64.b64decode(screenshot))

if __name__ == '__main__':
    main()