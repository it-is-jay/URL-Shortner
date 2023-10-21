# URL-Shortner
A simple web page that gets URL and returns a shortened URL

# Python venv
I have created new python virtual environment which includes all flask and required dependencies.
venv folder contains dependencies.

# steps to compile.
1. Clone the repo
2. Create a new venv using python or feel free to use the venv I have attached with the repo. Below are CMD steps on how to get configured. (Delete venv folder if you are creating new python environment)
   -  python -m venv venv
   -  .\venv\Scripts\activate
   -  (if required) python -m pip install --upgrade pip
   -  python -m pip install flask
3. Run application
   - python -m flask --app .\app.py run
