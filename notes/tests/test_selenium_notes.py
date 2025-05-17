
from selenium.webdriver.common.by import By
from time import sleep
from notes.tests.genericSeleniumTest import LoginTest

import unittest


class TestNote(LoginTest):
    """
    Test class that tests the basic funcationality of notes.
    """
    @classmethod
    def setUpClass(cls):
        """
        Overriding the setUpClass method to add a shared_data class variable, which is need
        for the tests to share data about created notes.
        """
        super().setUpClass()
        cls.shared_data = {}

    def test_open_existing_note(self):
        self.driver.get('http://localhost:8000')
        sleep(2)
        self.driver.find_element(By.ID, '329').click()
        sleep(2)
        self.assertEqual(
            'http://localhost:8000/note/329/',
            self.driver.current_url)

    def test_create_new_note(self):
        self.driver.get('http://localhost:8000')
        self.driver.find_element(By.ID, 'newNoteButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'modalNewNoteButton').click()
        sleep(2)
        self.assertIn('http://localhost:8000/note/', self.driver.current_url)
        self.shared_data['new_note_url'] = self.driver.current_url
 
    def test_trash_note(self):
        self.driver.get(self.shared_data['new_note_url'])
        self.driver.find_element(By.ID, 'settingsButton').click()
        sleep(0.5) 
        self.driver.find_element(By.ID, 'deleteNoteButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'modalDeleteNoteButton').click()
        sleep(2)
        self.assertIn('http://localhost:8000/notes/', self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
