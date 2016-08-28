"""
Run this script only for once
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


users = [{'email': 'umangshucool@gmail.com', 'username': 'mascot6699'},
         {'email': 'pranays94@gmail.com', 'username': 'pranays94'}]

for user in users:
    user_obj = User(email=user['email'], name=user['username'])
    session.add(user_obj)
    session.commit()
user_id_1 = user_obj.id

category1 = Category(
    name='Full Stack Web Developer Nanodegree',
    user_id=user_id_1)
session.add(category1)
session.commit()

item1 = Item(
    name='Programming Foundations with Python',
    user_id=user_id_1,
    category=category1,
    description="Introductory programming class to learn Object-Oriented Programming, a must-have technique to reuse and share code easily. Learn by making projects that spread happiness!")
session.add(item1)
session.commit()

item2 = Item(
    name='Intro to Relational Databases',
    user_id=user_id_1,
    category=category1,
    description="Relational databases are a powerful tool used throughout the industry. Learn the basics of SQL and how to connect your Python code to a relational database.")
session.add(item2)
session.commit()

item3 = Item(
    name='Full Stack Foundations',
    user_id=user_id_1,
    category=category1,
    description="Learn the fundamentals of back-end web development by creating your own web application from the ground up using the iterative development process.")
session.add(item3)
session.commit()

item4 = Item(
    name='Authentication & Authorization: OAuth',
    user_id=user_id_1,
    category=category1,
    description="Learn to implement the OAuth 2.0 framework to allow users to securely and easily login to your web applications.")
session.add(item4)
session.commit()


category2 = Category(name='Data Analyst Nanodegree', user_id=user_id_1)
session.add(category2)
session.commit()

item1 = Item(
    name='Data Visualization and D3.js',
    user_id=user_id_1,
    category=category2,
    description="Learn the fundamentals of data visualization and apply design and narrative concepts to create your own visualization.")
session.add(item1)
session.commit()

item2 = Item(
    name='Intro to Hadoop and MapReduce',
    user_id=user_id_1,
    category=category2,
    description="In this short course, learn the fundamentals of MapReduce and Apache Hadoop to start making sense of Big Data in the real world!")
session.add(item2)
session.commit()


item3 = Item(
    name='Intro to Data Analysis',
    user_id=user_id_1,
    category=category2,
    description="Explore a variety of datasets, posing and answering your own questions about each. You'll be using the Python libraries NumPy, Pandas, and Matplotlib.")
session.add(item3)
session.commit()

category3 = Category(name='Android Basics Nanodegree', user_id=user_id_1)
session.add(category3)
session.commit()

item1 = Item(
    name='Android Basics: Multi-screen Apps',
    user_id=user_id_1,
    category=category3,
    description="Learn to build multiscreen apps using the foundation of Android for Beginners!")
session.add(item1)
session.commit()

item2 = Item(
    name='Android Basics: Networking',
    user_id=user_id_1,
    category=category3,
    description="This class teaches the basics of networking using Android, and is a part of the Android Basics Nanodegree by Google.")
session.add(item2)
session.commit()

item3 = Item(
    name='Android Basics: Data Storage',
    user_id=user_id_1,
    category=category3,
    description="In this course, you'll learn the basics of data storage in Andriod, building your first database and an app that could be used for any small business!")
session.add(item3)
session.commit()

for i in session.query(Item).all():
    i.price = "Free"
    session.add(i)
    session.commit()
