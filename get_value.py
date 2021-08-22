from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, datetime
from pathlib import Path


class HostPlus():
    def __init__(self, client_id: str, pw: str,  fname: str) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.wd = webdriver.Chrome(options=chrome_options)
        self.id = client_id
        self.pw = pw
        self.historical_data = Path.cwd() / fname
        if not self.historical_data.is_file():
            self.historical_data.open('w+').close()

    def log_in(self):
        self.wd.get('https://member.aas.com.au/signin?redirectUri=https%3a%2f%2fmember.aas.com.au%2f%3fPlanCode%3dHC')
        time.sleep(30)
        
        username = self.wd.find_element_by_id("UserName")
        password = self.wd.find_element_by_id("Password")

        username.send_keys(self.id)
        time.sleep(3)
        password.send_keys(self.pw)
        time.sleep(3)

        self.wd.find_element_by_id('btnLogin').click()

        time.sleep(30)
        return

    def get_balence(self):
        balence =  self.wd.find_element_by_id('prominentCurrentBalance')
        return float(balence.text.strip()[1:].replace(',', ''))

    def write_balence(self, balence):
        today = str(datetime.datetime.now()).split(' ')[0]
        with self.historical_data.open('a') as f:
             f.write(f'{today}, {balence}\n')


if __name__ == '__main__':
    with open('credentials.txt', 'r') as f:
        client_id = f.readline().strip()
        password = f.readline().strip()

    hp = HostPlus(client_id,
                  password,
                  'historical_data.txt')

    hp.log_in()
    balence = hp.get_balence()
    hp.write_balence(balence)
    hp.wd.quit()
