from selenium.webdriver.common.by import By

from time import sleep
from notes.tests.genericSeleniumTest import LoginTest




class SettingsTest(LoginTest):
    def test_settings_dropdown_link(self):
        self.driver.get('http://localhost:8000')
        self.driver.find_element(By.ID, 'navbarProfileIcon').click()
        sleep(2)
        self.assertEqual('http://localhost:8000/account/', self.driver.current_url)
    
    def test_update_account_info(self):
        self.driver.get('http://localhost:8000/account/')
        sleep(0.5)
        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'username').send_keys('TestingAccount111')
        sleep(0.5)
        self.click('updateAccountButton')
        sleep(2)

        self.driver.get('http://localhost:8000/account/')
        self.assertEqual('TestingAccount111', self.driver.find_element(By.ID, 'username').get_attribute('value'))
        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'username').send_keys('TestingAccount')
        self.click('updateAccountButton')
        sleep(2)

        self.driver.get('http://localhost:8000/account/')
        self.assertEqual('TestingAccount', self.driver.find_element(By.ID, 'username').get_attribute('value'))
    
    def click(self, id):
        element = self.driver.find_element(By.ID, id)
        self.driver.execute_script("arguments[0].click();", element)