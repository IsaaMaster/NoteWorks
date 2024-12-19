
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        sleep(0.5)
        self.driver.find_element(By.ID, '173').click()
        sleep(2)
        self.assertEqual(
            'http://localhost:8000/note/173/',
            self.driver.current_url)

    def test_create_new_note(self):
        self.driver.get('http://localhost:8000')
        self.driver.find_element(By.ID, 'newNoteButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'modalNewNoteButton').click()
        sleep(2)
        self.assertIn('http://localhost:8000/note/', self.driver.current_url)
        self.shared_data['new_note_url'] = self.driver.current_url

    
    
    """
    Makes sure that the user is able to rename a note
    

    def test_rename_note(self):
        self.driver.get(self.shared_data['new_note_url'])
        sleep(2)

        # Scroll the element into view
        settings_button = self.driver.find_element(By.ID, 'settingsButton')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", settings_button)
        
        # Wait until the element is clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'settingsButton')))

        settings_button.click()

        sleep(0.5)
        self.driver.find_element(By.ID, 'newNoteTitle').send_keys(
            'New Note! Do not delete!')
        self.driver.find_element(By.ID, 'renameNoteButton').click()
        sleep(2)
        self.driver.get(self.shared_data['new_note_url'])
        sleep(2)

        self.assertIn('New Note! Do not delete!', self.driver.find_element(By.ID, 'noteTitle').text)
    """
        
    """
    Makes sure that the user is able to delete a note. 
    Note: is the same note that was just created in a previous test so that we 
    do not build up test notes in the databse. 
    """

    def test_trash_note(self):
        """
        Makes sure that the user is able to delete a note.
        Note: is the same note that was just created in a previous test so that we
        do not build up test notes in the databse.
        """
        self.driver.get(self.shared_data['new_note_url'])
        self.driver.find_element(By.ID, 'deleteNoteButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'modalDeleteNoteButton').click()
        sleep(2)
        self.assertIn('http://localhost:8000/notes/', self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
