# coding: utf-8

__author__ = "Claus Conrad <webmaster@clausconrad.com>"

class RtmList(object):
    def __init__(self, data):
        self.archived = bool(int(data["archived"]))
        self.deleted = bool(int(data["deleted"]))
        self.id = int(data["id"])
        self.locked = bool(int(data["locked"]))
        self.name = data["name"].decode("utf-8")
        self.position = int(data["position"])
        self.smart = bool(int(data["smart"]))
        self.sort_order = int(data["sort_order"])
