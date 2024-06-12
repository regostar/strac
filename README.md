# Assignmnet

Below is the Take Home Assignment:

Build a server-side app (preferably in Javascript/NodeJS) where you connect to One Drive and
1. list files
2. download files
4. list all users who have access to the file
5. It should also be real time where if users are added to the file, in real time, you get an event and you display the new users. Similarly, if users are removed from the file, you should be able to display the current list of users who have access to file.


Provide a README file which tells a) what does your program do and b) how to execute it. Make it extremely easy so that our engineers can understand and execute the code. If they are not able to test the code in less than 10 minutes, the assignment will get REJECTED.

Please provide loom video that a) executes all steps listed in your README, b) shows the demo of all above features, c) dives deep into the core parts of your code.
All of the above are REQUIRED features.

Please return the assignment in 24 hrs.

## Quick Install

clone repo

git clone https://github.com/regostar/strac.git

Create a virtual environment

python -m venv venv

Install requirements

cd strac_file_manager

pip install -r backend/requirements.txt

Add .env

refer

https://drive.google.com/drive/folders/1yQ6-v2uNj6NxptWOCJxt7SOOBEBLkGa3?usp=drive_link

Next run app :- 

cd backend/app

uvicorn app.main:app --host 0.0.0.0 --port 8000

## For webhook public facing we need ngrok

There are many ways to install and run this.

I have done this :- 

export NGROK_AUTHTOKEN=<shared in email>
pip install ngrok

python

>>import ngrok

>>listener = ngrok.forward(8001, authtoken_from_env=True)

>>print(f"Ingress established at {listener.url()}")

Now this url will be the webhook call back URL

add this here
https://github.com/regostar/strac/blob/731c398325e271e7eabc8857585688e9cf7f1b3d/backend/app/app/core/config.py#L213

Now if we deploy this, we don't need to do this.

Alternatively in the video I showed how we can use a webhook from Zapier and the subsequent email

## Getting Started

The commands in this documentation can be customized on the **Makefile**. It can be started with and without docker.

This project uses poetry, if you don't have it installed, you can the follow the instruction in [Poetry Documentation](https://python-poetry.org/docs/#installation).


Open [http://fastapi.localhost/docs](http://fastapi.localhost/docs) with your browser to see the result.


- Run the server without docker:

First, make sure you have all packages installed:

```bash
make install
```

```bash
make run-app
```
pip install requirements 

uvicorn app.main:app --host 0.0.0.0 --port 8001


This is a FastAPI project initialized using [`create-fastapi-project`](https://github.com/allient/create-fastapi-project), designed to provide a quick start for building APIs with [FastAPI](https://fastapi.tiangolo.com/).
Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the result.



Experimental installation :- 
- Run the server ( using docker):

```bash
# Run locally with docker in dev mode and force build
make run-dev-build
# or
# Run locally with docker in dev mode
make run-dev
# or
# Run locally with docker in prod mode (Autorelod disabled)
make run-prod
```

