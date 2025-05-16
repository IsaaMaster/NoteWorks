# Noteworks

## Overview

**Noteworks 5** is a web-based note-taking application I developed to strengthen my skills in full-stack web development and user-centered design. The app provides a clean, intuitive interface for organizing ideas, tasks, and study material—ideal for students, professionals, or anyone looking to manage information effectively.

Designed with simplicity and usability in mind, Noteworks 5 includes essential note-taking features such as rich text formatting, folder organization, user authentication, note collaboration, and search. It also introduces smart AI productivity tools that distinguish it from typical note apps:

### ✨ Key Features

- **Smart Search**  
  Forget exact keywords—describe the content of a note in your own words, and Smart Search will intelligently surface relevant results.

- **Snap Summary**  
  Instantly generate concise summaries of your notes using AI, helping you review key ideas quickly.

- **Recall Boost (Coming Soon)**  
  Transform your notes into#study-ready formats designed to reinforce memory and retention.

### 🚀 Live Demo

👉 [View the live application](https://noteworks5.herokuapp.com/)

## 🛠️ Technical Specifications

### 📦 Tech Stack

- **Frontend:**
  - HTML5, CSS3, JavaScript (ES6+)
  - Bootstrap 5 for responsive design
  - Libraries & Tools:
    - **Quill.js** – Rich text editing
    - **Masonry** – Dynamic grid-based note layout
    - **jsPDF** – Export notes as downloadable PDFs
  - AJAX with jQuery for asynchronous HTTP requests and dynamic page updates without full DOM reloads

- **Backend:**
  - Django (Python) for request handling, routing, and business logic
  - Django REST Framework (DRF) for API endpoints supporting third-party integration and future mobile development
  - Cohere API integration for AI-powered features like Smart Search and Snap Summary

- **Database:**
  - PostgreSQL, hosted on Microsoft Azure (Flexible Server)
  - Relational schema supporting users, notes, folders, sharing permissions, and metadata

- **Authentication:**
  - Secure session-based authentication via Django
  - Google OAuth for optional single sign-on
  - Role-based access control for shared note permissions

- **AI/ML Features:**
  - **Smart Search** – Uses Cohere reranking to match user queries with relevant notes, even when phrased imprecisely
  - **Snap Summary** – Leverages Cohere’s summarization endpoint to quickly distill note content

---

### 🚀 Deployment & Hosting

- **Hosting:**  
  - Full-stack deployment on [Heroku](https://noteworks5.herokuapp.com/)
  - Environment variables securely managed via Heroku Config Vars
  - HTTPS secured via automatic SSL certificates from Heroku

- **Database Hosting:**  
  - Azure PostgreSQL Flexible Server with daily backups and managed scaling

---

### 🔍 Testing & Code Quality

- **Linting:**
  - `HTMLHint` for HTML
  - `ESLint` for JavaScript
  - `Pylint` for Python (Django backend)

- **Automated Testing:**
  - **Unit Tests:** PyUnit for backend logic and utility functions
  - **End-to-End Testing:** Selenium (headless) for major user flows

- **CI/CD Pipeline:**
  - GitHub Actions:
    - Runs linting and test suites on every push and pull request
    - Auto-deploys to Heroku on successful pushes to `main`

---

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
   python manage.py runserver
### Running Tests: 
Please make sure you have all other dependencies installed first. 
1. Run all tests
   ```
   python manage.py test notes/tests
2. Running a single test
   ```
   python manage.py test notes.tests.test_selenium_notes
### Running Pylint
Pylint custom arguments should be modified in .pylintrc
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

### Running HTMLHint
HTMLHint custom arguments should be modified in .htmlhintrc (not yet created)
1. Install HTMLHint
   ```
   npm install -g htmlhint
2. Running HTMLHint
   ```
    htmlhint "**/*.html"
   
## License
This software is licensed under the GNU General Public License. 

## Contact Information: 
Please reach out to isong@westmont.edu for any questions or comments. 
