# Cookie base authenticate with FastAPI

### Overview

In this project i'm trying to make a pure jwt authentication in fastapi
and mongodb .

Purpose of this project is just for training and there is alot of packages
to do jwt authentication or other things i have done here

### How to Run

1. First clone the project and cd to project directory

```commandline
git clone <url of the project>
cd Password-generator
```

2. Make a python virtual env

```commandline
python3 -m venv <name of your venv>
```

3. Activate your venv

#### on linux

```commandline
source ./venv/bin/activate
```

#### on windows

```commandline
venv/bin/activate
```

4. Install the python packages

```commandline
pip install -r requirements.txt
```

5. Run the file

```commandline
uvicorn main:app --reload
```