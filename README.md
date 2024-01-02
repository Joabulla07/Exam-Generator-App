# Exam Date Generator App ![Status badge](https://img.shields.io/badge/status-in%20progress-yellow) ![Python 3.6](https://img.shields.io/badge/python-3.12-blue.svg)
A university in Resistencia-Chaco requires a system to create examination schedules for its students. So this app was created to satisfies that necessity.
This app was created using PyQt.




## 🚀 Installation

To install and run the app locally, follow these steps:
1. Clone the repository
2. Install the required dependencies with `python -m pip install -r requirements.txt`


## ⚠️ Dependencies - coming soon


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
