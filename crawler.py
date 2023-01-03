import traceback
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Crawler:
    def __init__(self):
        chromedriver_autoinstaller.install()
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_argument('window-size=900,900')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=options, desired_capabilities=caps)
        self.driver.implicitly_wait(5)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'navigator.'})
        self.driver.set_page_load_timeout(30)

    def req(self, url):
        try:
            print(f"[+] doing crawler req {url}")
            self.driver.get(url)
        except:
            print(f"[x] crawler driver req fail - {url}")
            print(traceback.format_exc())
            return False

        return self.driver
