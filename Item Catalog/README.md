# Item Catalog

    * This is the third project for the fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

    * This is an application that provides a list of items within a variety of categories as well as
    provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own categories and items.

    * Used technologies: Flask, SQLAlchemy, Google+ Authentication, Bootstrap for CSS


# How to run the application
-----------------------
1. Navigate to project folder:

`cd /vagrant`

2. Create your own virtual environment and install dependencies from requirements.txt

```
virtualenv catalog-project
pip install -r requirements.txt
source catalog-project/bin/activate
```

3. Run database_setup.py in order to set database:

`python database_setup.py`

4. Populate database

`python catalog_populator.py`

5. Run app

`python webserver.py`

6. Go to: http://localhost:8080

7. Api endpoint are:
	7.1 http://localhost:8080/all/JSON => For listing all categories
	7.2 http://localhost:8080/1/JSON => For getting all items of category with categoryid as 1
	7.3 http://localhost:8080/1/item/2/JSON  => For getting details of item with itemid as 2
