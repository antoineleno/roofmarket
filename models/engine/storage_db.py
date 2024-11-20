#!/usr/bin/python3
"""DB Storage module"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.agent import Agent
from models.user import User
from models.property import Property
from models.transaction import Transaction, Subcription
from models.whishlist import Whishlist
from models.review import Review
from models.property_image import Property_image
from models.message import Message, Room, RoomParticipants
base_dir = os.path.dirname(__file__)
parent_dir = os.path.join(base_dir, '..', '..')
sys_path = os.path.abspath(parent_dir)

sys.path.append(sys_path)


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
        url = "roofmarket_user:roofmarket_pwd@localhost/roofmarket_db"
        self.__engine = create_engine(
                    'mysql+mysqldb://' + url, pool_pre_ping=True)

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
                      "Agent": Agent,
                      "Property": Property,
                      "Transaction": Transaction,
                      "Subcription": Subcription,
                      "Whishlist": Whishlist,
                      "Review": Review,
                      "Property_image": Property_image,
                      "Message": Message,
                      "Room": Room,
                      "RoomParticipants": RoomParticipants}
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
            self.__session.commit()

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

    def get_object(self, cls, sign=None, all=None, order_by=None,
                   limit=None,
                   count=False, **kwargs):
        """
        Get all objects or only one object based on filters.
        Optionally count the results.

        Args:
            cls: The model class to query.
            sign: The comparison operator for filtering.
            all: If not None, fetches all matching objects.
            order_by: A tuple (column, direction) for sorting
                (e.g., (cls.created_at, 'desc')).
            limit: An integer specifying the maximum number
                of results to return.
            count: If True, returns the count of results based on the filters.
            **kwargs: Key-value pairs for filtering.

        Returns:
            A single object if `all` is None, otherwise a list of objects.
            If `count` is True, returns the count of objects.
        """
        if sign is None:
            sign = '=='

        query = self.__session.query(cls)

        operators = {
            '==': lambda key, value: key == value,
            '!=': lambda key, value: key != value,
            '<': lambda key, value: key < value,
            '<=': lambda key, value: key <= value,
            '>': lambda key, value: key > value,
            '>=': lambda key, value: key >= value
        }

        if kwargs:
            for key, value in kwargs.items():
                if sign in operators:
                    query = query.filter(operators[sign](getattr(cls, key),
                                                         value))
                else:
                    raise ValueError(f"Invalid comparison operator: {sign}")
        if count:
            if (
                "room_id" in kwargs and
                "user_id" in kwargs and
                "read_status" in kwargs
            ):
                query = self.__session.query(cls).filter(
                    cls.room_id == kwargs.get("room_id"),
                    cls.user_id != kwargs.get("user_id"),
                    cls.read_status == False
                )

                return query.count()
        if order_by:
            column, direction = order_by
            if direction.lower() == 'desc':
                query = query.order_by(column.desc())
            elif direction.lower() == 'asc':
                query = query.order_by(column)
            else:
                raise ValueError("Invalid direction for order_by")

        if limit is not None:
            query = query.limit(limit)
        if all is not None:
            return query.all()
        return query.first()
