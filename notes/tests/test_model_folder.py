from django.test import TestCase
from notes.models import Folder
from django.contrib.auth.models import User

import unittest


class FolderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpassword")
        Folder.objects.create(title="test folder", home=True, parent = None, owner = user)


    def test_folder_creation(self):
        folder = Folder.objects.get(title="test folder")
        self.assertEqual(folder.title, "test folder")
    
    def test_folder_str(self):
        folder = Folder.objects.get(title="test folder")
        self.assertEqual(str(folder), "test folder")
    
    def test_folder_delete(self):
        folder = Folder.objects.get(title="test folder")
        folder.delete()
        self.assertEqual(str(Folder.objects.all()), '<QuerySet []>')
    
    def test_folder_update(self):
        folder = Folder.objects.get(title="test folder")
        folder.title = "new title"
        folder.save()
        self.assertEqual(folder.title, "new title")
    
if __name__ == '__main__':
    unittest.main()

    
