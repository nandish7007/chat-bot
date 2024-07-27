# Chat-bot
Its an Chat-bot app build with python fast-api.

### Instructions
Follow step by step instructions given below to setup the Chat-bot fast-api application in local (linux based OS).

### Prerequisites

- Python 3.8

### Recommended tools

Creating a virtual python environment dedicated for this application is strongly recommended to prevent your local system from breaking unexpectedly.

- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

        $ python3.8 -m virtualenv venv

- [PyCharm](https://www.jetbrains.com/pycharm/)

### Setting up project

1. Clone this repository and confirm if virtual env is activated.

        $ git clone https://github.com/nandish7007/test-bot.git
        $ cd chat-bot
        $ python --version
        Python 3.8

2. Run `pip install -r requirements.txt`

3. Run the following command to start the **server**.

        $ uvicorn main:app --reload 

4. Run the following command to run the **test cases**.

        $ pytest test_main.py

### Thanks !!
