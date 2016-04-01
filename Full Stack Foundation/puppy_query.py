from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppy.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#  1. Query all of the puppies and return the results in ascending alphabetical order
def get_all_puppies():
    """
    :return: Prints name of all puppies in ascending order
    """
    all_puppies = session.query(Puppy).order_by(Puppy.name.asc()).all()
    for puppy in all_puppies:
        print(puppy.name)


def age_in_months(date1, date2):
    """
    :returns: A helper function which return age in months
    """
    delta = date1 - date2
    return delta.days / 30


#  2. Query all of the puppies that are less than 6 months old organized by the youngest first
def get_young_puppies():
    """
    :return: Prints name of all puppies less than 6 months old youngest first
    """
    today = datetime.date.today()
    all_puppies = session.query(Puppy).order_by(Puppy.dob.desc()).all()

    for puppy in all_puppies:
        puppy_age_months = age_in_months(today, puppy.dob)
        if puppy_age_months < 6:
            print "{name}: {months}".format(name=puppy.name, months=puppy_age_months)


#  3. Query all puppies by ascending weight
def get_light_puppies():
    """
    :return: Prints name of all puppies by ascending weight
    """
    all_puppies = session.query(Puppy).order_by(Puppy.weight.asc()).all()
    for puppy in all_puppies:
        print "{name}: {weight}".format(name=puppy.name, weight=round(puppy.weight, 2))


#  4. Query all puppies grouped by the shelter in which they are staying
def puppies_with_shelter():
    """
    :return: Prints puppies grouped by the shelter in which they are staying
    """
    all_shelter = session.query(Shelter).all()
    for shelter in all_shelter:
        print "The puppies in shelter {name} are".format(name=shelter.name)
        all_in_puppies_shelters = session.query(Puppy).filter_by(shelter=shelter)
        for puppy in all_in_puppies_shelters:
            print(puppy.name)




def main():
    """
    main subroutine
    """
    get_all_puppies()
    get_young_puppies()
    get_light_puppies()
    puppies_with_shelter()

if __name__ == '__main__':
    main()