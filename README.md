[Twitter App](https://github.com/GonEbal/twitter)

# Introduction

The goal of this project was to create copy of twitter written on Django.

![preview](_screenshots/preview.gif?raw=true "Title")

### Main features

* Separated dev and production settings

* Example app with custom user model

* User registration and logging in

* SQLite by default if no env variable is set


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/GonEbal/twitter.git
    $ cd twitter
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
