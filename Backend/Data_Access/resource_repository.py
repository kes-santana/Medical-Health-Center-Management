class ResourceRepository:
    def __init__(self, items: list):
        self.items : list = items
        self.count: int = len(items)

    def get_all(self):
        # Devuelve, una lista, con todos los elementos de la Base de Datos
        pass

    def get_by_id(self, id: int):
        # Esta claro lo que hace
        pass

    def save(self, item):
        # Escribe en Base de Datos
        pass

    def change_state(self, id: int, state: str):
        pass