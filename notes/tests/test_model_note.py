from django.test import TestCase
from notes.models import Note, Folder
from django.contrib.auth.models import User

import unittest

class NoteTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpassword")
        folder = Folder.objects.create(title="test folder", home=True, parent = None, owner = user)
        Note.objects.create(title="test note", text="this is a test note", folder = folder, owner = user)
  

    def test_note_creation(self):
        note = Note.objects.get(title="test note")
        self.assertEqual(note.title, "test note")
        self.assertEqual(note.text, "this is a test note")
        self.assertEqual(note.displayText, "")
    
    def test_note_str(self):
        note = Note.objects.get(title="test note")
        self.assertEqual(str(note), "test note")
    
    def test_note_delete(self):
        note = Note.objects.get(title="test note")
        note.delete()
        self.assertEqual(str(Note.objects.all()), '<QuerySet []>')
    
    def test_note_update(self):
        note = Note.objects.get(title="test note")
        note.title = "new title"
        note.text = "new text"
        note.displayText = "new display text"
        note.save()
        self.assertEqual(note.title, "new title")
        self.assertEqual(note.text, "new text")
        self.assertEqual(str(note.folder), "test folder" )
        self.assertEqual(note.displayText, "new display text")
    
    def test_note_last_accessed(self):
        note = Note.objects.get(title="test note")
        note.lastAccessed = "2021-06-01 12:00:00"
        self.assertEqual(note.lastAccessed, "2021-06-01 12:00:00")

if __name__ == '__main__':
    unittest.main()
    
