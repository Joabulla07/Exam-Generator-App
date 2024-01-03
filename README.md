# Exam Date Generator App ![Status badge](https://img.shields.io/badge/status-in%20progress-yellow) ![Python 3.6](https://img.shields.io/badge/python-3.12-blue.svg)
A university in Resistencia-Chaco requires a system to create examination schedules for its students. So this app was created to satisfies that necessity.
This app was created using PyQt.

![image](https://github.com/Joabulla07/Exam-Generator-App/assets/40646853/1c4563af-0112-4b03-bd36-4ab4f2d91cd7)



## 🚀 Installation

To install and run the app locally, follow these steps:
1. Clone the repository
2. Install the required dependencies with `python -m pip install -r requirements.txt`


## ⚠️ Dependencies - coming soon
A pre-commit dependency is required for code formatting and performing local validations before pushing to a remote branch. To install:

1. Confirm the pre-commit module is installed with pre-commit --version.
2. Install the pre-commit hook in your local repository with pre-commit install.
3. The pre-commit run with pre-commit run

A pre-commit hook will now be installed in your local repository, which will run checks before allowing commits. If any checks fail, please review your staging area for any necessary fixes.

## 💊 Test App
Execute tests with coverage using
- `pytest --cov-config=.coveragerc --cov=. --cov-fail-under=5 tests/unit`


## 📋  Instructions for users

1. Excel columns must have the names:
   1. "grado", "materia" , "dia" and "segundo dia"
   2. "dia" are for preference day of the week. and "segundo dia" is for the second preference day.
2. The subject must have numbers instead of roman numbers.
   1. Example: "Tècnica 1", "Tècnica 2".
3. Dates must have "dd/mm/yy" format. Ex: "02/02/24".
4. You need to add the career name at first field.

## Extra documentation
1. Jira: https://joannabbado4748.atlassian.net/jira/software/projects/EDG/boards/1
2. wiki: https://joannabbado4748.atlassian.net/wiki/home


## Liscense
Joanna Bulla
