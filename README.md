# IDATT2900-072

to run the tests:
`python -m pytest tests`

## To download the project and install all the requirements

### 1. git clone project:

**With SSH:**

`git clone git@gitlab.stud.idi.ntnu.no:mattiaae/idatt2900-072.git`

`cd idatt2900-072`

**With HTTPS:**

`git clone https://gitlab.stud.idi.ntnu.no/mattiaae/idatt2900-072.git`

`cd idatt2900-072`

### 2. Install the virtual environement inside the project folder

`python -m venv ./venv` **OR** `python3 -m venv ./venv`

**On mac/linux:** `source ./venv/bin/activate`
**On Windows:** `.\venv\Scripts\activate`

### 3. Install all the requirements

`python -m pip install -r requirements.txt`

### 4. To chech that it is successfully installed, check the version

`python -m bbcli --version`

### 5. Run the tests

`python -m pytest test`

### 6. Setup the bbcli script inside the root of the project

`pip install --editable .` **OR** `pip3 install --editable .`

[image](/uploads/8780c8ce8ccb66bfe0bad77eb9410769/image.png)
