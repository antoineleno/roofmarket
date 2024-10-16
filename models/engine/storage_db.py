#!/usr/bin/python3
"""DB Storage module"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.agent import Agent
from models.user import User
from models.property import Property
from models.transaction import Transaction
from models.whishlist import Whishlist
from models.review import Review
from models.property_image import Property_image
from models.visit_schedule import Visit_schedule
from models.message import Message
from models.payement import Payment


class DBStorage:
    """DBStorage
    Class to manage objects storage to DB
    """
    __engine = None
    __session = None

    def __init__(self):
        """Contructor method
        """
        env = os.getenv("env")

        self.__engine = create_engine(
                    'mysql+mysqldb://roofmarket_user:roofmarket_pwd@localhost/roofmarket_db')

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all to retrieve all records from DB

        Args:
            cls (string, optional): Object to return. Defaults to None.

        Returns:
            Dict: All records from a database
        """
        allclasses = {"User": User,
                      "State": Agent,
                      "City": Property,
                      "Amenity": Transaction,
                      "Place": Whishlist,
                      "Review": Review,
                      "Property_image": Property_image,
                      "Visit_schedule": Visit_schedule,
                      "Message": Message,
                      "Payment": Payment}
        obj_result = {}
        cls = cls if not isinstance(cls, str) else allclasses.get(cls)
        if cls is None:
            for cls in allclasses:
                objs = self.__session.query(cls).all()
                for o in objs:
                    obj_result["{}.{}".format(o.name, o.id)] = o
        else:
            objs = self.__session.query(cls).all()
            for o in objs:
                obj_result["{}.{}".format(o.__table__, o.id)] = o
        return obj_result

    def new(self, obj):
        """new : to add an an obj to a session

        Args:
            obj (instance): Obj created to be added
        """
        self.__session.add(obj)

    def save(self):
        """save: method to commit changes to the db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete an obj from the db

        Args:
            obj (string): name of the obj. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)()

    def close(self):
        """close session
        """
        self.__session.close()
