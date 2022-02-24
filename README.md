# IDATT2900-072

to run the tests:
python -m pytest tests

## To download the project and install all the requirements
# git clone with ssh:
git@gitlab.stud.idi.ntnu.no:mattiaae/idatt2900-072.git
cd idatt2900-072

# git clone with https:
git clone https://gitlab.stud.idi.ntnu.no/mattiaae/idatt2900-072.git
cd idatt2900-072

# Install the virtual environement inside the project folder
python -m venv ./venv
source ./venv/bin/activate

# Install all the requirements
python -m pip install -r requirements.txt

# To chech that it is successfully installed, check the version 
python -m bbcli --version

# Run the tests
python -m pytest test