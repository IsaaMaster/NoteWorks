from selenium.webdriver.common.by import By

from time import sleep
from notes.tests.genericSeleniumTest import BasicTest

import unittest


class TestAuth(BasicTest):
    def test_home_page(self):
        print('testing home page')
        self.driver.get('https://noteworks5-0c3e8b44eefc.herokuapp.com/')
        self.assertIn('NoteWorks', self.driver.title)

    def test_login_page(self):
        self.driver.get('http://localhost:8000/login')
        self.assertIn('http://localhost:8000/login', self.driver.current_url)

    def test_register_page(self):
        self.driver.get('http://localhost:8000/register')
        self.assertIn(
            'http://localhost:8000/register',
            self.driver.current_url)

    def test_login(self):
        self.driver.get('http://localhost:8000/login')
        self.driver.find_element(By.ID, 'username').send_keys('TestingAccount')
        self.driver.find_element(By.ID, 'password').send_keys('password')
        self.driver.find_element(By.ID, 'login').click()
        sleep(3)
        self.assertIn('notes', self.driver.current_url)

    def test_logout(self):
        self.driver.get('http://localhost:8000/login')
        self.driver.find_element(By.ID, 'username').send_keys('TestingAccount')
        self.driver.find_element(By.ID, 'password').send_keys('password')
        self.driver.find_element(By.ID, 'login').click()
        sleep(3)
        self.driver.find_element(By.ID, 'navbarProfileIcon').click()
        sleep(1)
        self.driver.find_element(By.ID, 'logout').click()
        sleep(2)
        self.assertEqual('http://localhost:8000/', self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
