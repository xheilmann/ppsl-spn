class IDChip:
    def __init__(self, id, ip4, port, name) -> None:
        assert id is not None
        assert ip4 is not None
        assert port is not None

        self.__id = id
        self.__ip4 = ip4
        self.__port = port

        if name is not None:
            self.__name = name
        else:
            self.__name = f"{id}_{ip4}_{port}"

    @property
    def id(self):
        return self.__id

    @property
    def ip4(self):
        return self.__ip4

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name
