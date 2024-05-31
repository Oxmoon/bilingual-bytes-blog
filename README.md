# Running the App for Development

## 1. Clone the repository

Open your terminal and run:

Recommended to use SSH

```
git clone git@github.com:Oxmoon/bilingual-bytes-blog.git
cd bilingual-bytes-blog
```

## 2. Setup the Backend

### 1. Setup Python Virtual Enviornment

Enter the backend folder

```
cd backend/
```

Create a virtual enviornemnt

```
python3 -m venv .venv
```

To activate the virtual enviornment run:

```
. .venv/bin/activate
```

Update the python libraries with:

```
pip install -r requirements.txt
```

### 2. Setup PostgreSQL

Ensure PostgreSQL is running

Create a database for the blog:

```
psql
CREATE DATABASE blog_db;
```

### 3. Setup Enviornment Variables

Return to the backend folder `cd backend/`

Create a file titled `.env` and enter the following:

You can create a secret key using `openssl rand -hex 32`

```
FLASK_APP=app/wsgi.py
FLASK_DEBUG=1
FLASK_CONFIG=development
SECRET_KEY=(put anything here)
DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/blog_db"
```

Future enviornment variables including API keys will be saved here. Will not be saved in the repository

## 3. Running the Backend

Ensure the virtual enviornment is running:

```
. .venv/bin/activate
```

Start the flask app with:

```
flask run
```

