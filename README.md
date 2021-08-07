# E-shhnli
ecommerce webesite
the first project i have finished for a client.
this website let customers to purchase from a wide range of US stores and websites and Delivering products at their hands

## Setup
The first thing to do is to clone the repository:
```
> $ git clone https://github.com/EslamRM/E-shhnli.git
> $ cd E-shhnli
```
Create a virtual environment to install dependencies in and activate it:
```
> $ virtualenv2 --no-site-packages env
> $ source env/bin/activate
```
Then install the dependencies:
```
> (env)$ pip install -r requirements.txt
```
Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once pip has finished downloading the dependencies:
```
> (env)$ cd project
> (env)$ python manage.py runserver
```
