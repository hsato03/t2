import pickle
from abc import ABC


class GenericDAO(ABC):
    def __init__(self, datasource=""):
        self.__datasource = datasource
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, "wb"))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, "rb"))

    def insert(self, key, obj):
        self.__cache[key] = obj
        self.__dump()

    def find_by_id(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            pass

    def update(self, old_key, new_key, obj):
        self.remove(old_key)
        self.__cache[new_key] = obj
        self.__dump()

        return obj

    def remove(self, key):
        try:
            obj = self.__cache.pop(key)
            self.__dump()
            return obj
        except KeyError:
            pass

    def find_all(self):
        return list(self.__cache.values())