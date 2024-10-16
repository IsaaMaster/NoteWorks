# Noteworks 5
## About
Noteworks 5 is a personal project that I've started to gain experience with web development. It is designed to be a powerful and intuitive note-taking application designed to help you organize your thoughts, ideas, and tasks efficiently. Whether you're a student, professional, or anyone who needs to keep track of information, Noteworks 5 provides a seamless and user-friendly experience. With features like rich text formatting, folder organization, and search functionality, you can easily create, manage, and find your notes whenever you need them. Here some are key features that I'm really happy to have designed: 
- **Rich Text Formatting:** Customize your notes with bold, italic, underline, and other formatting options.
- **Folder Organization:** Organize your notes into folders for easy access and management.
- **Search Functionality:** Quickly find notes using the built-in search feature.
- **Secure and Private:** Your notes are securely stored and only accessible by you.

View the live site [here](https://noteworks5.herokuapp.com/). 

## Contributing
### Installation Instructions: 
1. Clone the repository:
   ```
   sh git clone https://github.com/IsaaMaster/NoteWorks.git
   cd NoteWorks
2. Install dependencies
   ```
   pip install -r requirements.txt
3. Apply migrations
   ```
   python manage.py migrate
4. Run the development server
   ```
   python manage.py runsever
### Running Tests: 
Please make sure you have all other dependencies installed first. 
1. Run all tests
   ```
   python manage.py test notes/tests
2. Running a single test
   ```
   python manage.py test notes.tests.test_selenium_notes
### Running Pylint
Pyling custom arguments should be modified in .pylintrc
1. Install Pylint
   ```
   pip install pytlint
2. Running Pylint
   Navigate to the project directory and run:
   ```
   pylint $(git ls-files '*.py')
3. Running Pylint for one file
   ```
   pylint notes/views.py
4. Make automatic corrections
   ```
   autopep8 --in-place --aggressive --aggressive --recursive .
   isort .
### Contact Information: 
Please reach out to isong@westmont.edu for any questions or comments. 
