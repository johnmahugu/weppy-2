import pymongo
from weppy.extension import Extension

class MongoDBExtension(Extension):
    """
    Sets a connection to a MongoDB database in the app object.
    """

    def __init__(self, host, port, db_name, username=None, password=None,
                 attr_name='mongodb'):
        """
        host -- str that specifies the hostname or IP address of the server.
        port -- int that specifies the port number on which to connect.
        db_name -- str that specifies the database name.
        username -- str that specifies the username. None by default.
        password --  str that specifies the password. None by default.
        attr_name -- str that specifies the name of the attribute of the app
                     object in which the connection is set. 'mongo' by default.
        """
        self.attr_name = attr_name
        client = pymongo.MongoClient(host, port)
        self.db = getattr(client, db_name)
        if username and password:
            self.db.authenticate(username, password)

    def __call__(self, app):
        """
        Sets the connection to the database in the app object.

        app -- WSGIApplication instance.
        """
        setattr(app, self.attr_name, self.db)
