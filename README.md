Certainly! Here's a complete `README.md` file you can use for your project. It includes all the necessary steps for setting up the environment, running the app, and using version control. Feel free to modify any details to better fit your project.

---

# Book Search App

A Flask application that allows users to search for books via the [Open Library API](https://openlibrary.org/), with a frontend served from a static HTML page.

## Table of Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
   - [Clone the Repository](#clone-the-repository)
   - [Create a Virtual Environment](#create-a-virtual-environment)
   - [Activate the Virtual Environment](#activate-the-virtual-environment)
   - [Install Dependencies](#install-dependencies)
3. [Running the Application](#running-the-application)
4. [Testing the Application](#testing-the-application)
5. [Deactivating the Virtual Environment](#deactivating-the-virtual-environment)
6. [Contributing](#contributing)

---

## Introduction

This project is a simple book search web application built with Flask. The user can search for books by title, author, or subject, and the app fetches results from the Open Library API.

The frontend consists of a single `index.html` page, served from the `frontend` folder. The backend is a Flask application that communicates with the Open Library API and serves the data to the frontend.

---

## Setup

Follow these steps to set up the project on your local machine.

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/book_search_app.git
cd book_search_app
```

### Create a Virtual Environment

Once inside the project directory, create a virtual environment. If you're using Python 3.3 or later, use the `venv` module:

```bash
python3 -m venv venv
```

This will create a directory named `venv` which contains the isolated Python environment for your project.

### Activate the Virtual Environment

After creating the virtual environment, activate it.

#### On macOS or Linux:

```bash
source venv/bin/activate
```

#### On Windows (I do not own a windows to test this):

```bash
venv\Scripts\activate
```

Once activated, you should see the virtual environment's name (`venv`) appear in your terminal prompt.

### Install Dependencies

With the virtual environment activated, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

This will install all necessary packages such as Flask, requests, and other dependencies defined in the `requirements.txt` file.

---

## Running the Application

After setting up the environment, you can run the Flask application. The backend will run on port `5001`.

To start the Flask app, run:

```bash
python src/backend/app.py
```

Once the server is running, you can access the application in your web browser at:

```
http://localhost:5001
```

---

## Testing the Application

This project includes unit tests to ensure that the functionality is working as expected.

Our goal is to have 95% or better. 

To run the tests with code coverage, use the following command:

```bash
PYTHONPATH=src coverage run -m unittest discover -s test/backend
```

This will run all the tests located in the `test/backend` directory. You can view the coverage report with:

```bash
coverage report
```

For a more detailed HTML report, you can use:

```bash
coverage html
```

The report will be saved in the `htmlcov` directory, and you can open it in a web browser.
