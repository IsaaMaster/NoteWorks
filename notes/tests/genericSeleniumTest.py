from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


import unittest
"""
Basic Test class that sets up the webdriver and
provides a framework for teardown and setup methods
"""


class BasicTest(unittest.TestCase):

    """
    setUpClass method that sets up the chrome webdriver
    --headless: runs the browser in headless mode, meaning that there is no GUI
    --log-level=3: sets the log level to 3, which means that only critical errors will be logged,
     we have this to avoid dev tools logs that are not related to tests.
    """
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        cls.driver = webdriver.Chrome(options=options)
        cls.addClassCleanup(cls.driver.quit)
        cls.addClassCleanup(cls.driver.close)

    def tearDown(self):
        pass

    def setUp(self):
        pass


"""
LoginTest class that inherits from BasicTest and provides a
framework for tests were login is required. In order to be more
computationally efficient, the login is done only once and the
the cookies are stored in the class variable cookies.
"""


class LoginTest(BasicTest):

    """
    logs in once and stores the cookies in the class variable cookies so that tests that
    need to login do not have to login every time.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cookies = cls.login()

    """
    logs in the Testing user and returns the cookies for the login session.
    """
    @classmethod
    def login(cls):
        cls.driver.get('http://localhost:8000/login')
        cls.driver.find_element(By.ID, 'username').send_keys('TestingAccount')
        cls.driver.find_element(By.ID, 'password').send_keys('password')
        cls.driver.find_element(By.ID, 'login').click()
        cookies = cls.driver.get_cookies()
        return cookies

    """
    gives the driver the cookies for the login session.
    """

    def setUp(self):
        super().setUp()
        self.driver.get('http://localhost:8000')
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
