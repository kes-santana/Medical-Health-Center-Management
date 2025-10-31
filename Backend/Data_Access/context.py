from Backend.Data_Access.repository import Repository


class Context:
    def __init__(self):
        pass
    
    @staticmethod # Decorador
    def get_repo(repo: str) -> Repository:
        pass