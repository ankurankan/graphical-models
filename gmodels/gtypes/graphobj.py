"""
object contained in a graph
"""

from gmodels.gtypes.abstractobj import AbstractGraphObj


class GraphObject(AbstractGraphObj):
    "object contained in a graph"

    def __init__(self, oid: str, odata={}):
        """!
        """
        self.object_id = oid
        self.object_data = odata

    def data(self):
        """!
        """
        return self.object_data

    def id(self):
        """!
        """
        return self.object_id

    def clear_data(self):
        """!
        """
        self.object_data.clear()

    def update_data(self, ndata: dict):
        """!
        """
        self.object_data.update(ndata)
