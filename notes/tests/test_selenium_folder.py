
from selenium.webdriver.common.by import By

from time import sleep
from notes.tests.genericSeleniumTest import LoginTest


class TestFolder(LoginTest):
    """
    TestFolder class that inherits from LoginTest and tests the basic functionality of the Folders
    from a user perspective.
    """
    @classmethod
    def setUpClass(cls):
        """
        Overriding the setUpClass method to add a shared_data class variable, which is
        needed for the tests to share data about created Folders.
        """
        super().setUpClass()
        cls.shared_data = {}

    def test_open_existing_folder(self):
        self.driver.get('http://localhost:8000')
        sleep(0.5)
        self.driver.find_element(By.ID, '81').click()
        sleep(1)
        self.assertEqual(
            'http://localhost:8000/notes/81/',
            self.driver.current_url)

    def test_create_new_folder(self):
        self.driver.get('http://localhost:8000')
        self.driver.find_element(By.ID, 'newFolderButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'modalNewFolderButton').click()
        sleep(2)
        self.assertIn('http://localhost:8000/notes/', self.driver.current_url)
        self.shared_data['new_folder_url'] = self.driver.current_url

    def test_rename_folder(self):
        self.driver.get(self.shared_data['new_folder_url'])
        self.driver.find_element(By.ID, 'settingsButton').click()
        sleep(0.5)
        self.driver.find_element(
            By.ID, 'newFolderTitle').send_keys('New Folder')
        self.driver.find_element(By.ID, 'renameFolderButton').click()
        sleep(2)
        self.driver.get(self.shared_data['new_folder_url'])
        sleep(0.5)
        self.assertIn(
            'New Folder',
            self.driver.find_element(
                By.ID,
                'folderTitle').text)

    def test_trash_folder(self):
        """
        Makes sure that the user is able to delete a folder.
        Note: The folder that is deleted in this class is the same folder that we created
        in the previous test. This is so that we don't have a bunch of unused test folders in
        the database.
        """
        self.driver.get(self.shared_data['new_folder_url'])
        self.driver.find_element(By.ID, 'settingsButton').click()
        sleep(0.5)
        self.driver.find_element(By.ID, 'deleteFolderButton').click()
        sleep(0.5)
        self.assertEqual(
            'http://localhost:8000/notes/80/',
            self.driver.current_url)
