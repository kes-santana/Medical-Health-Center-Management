
from backend.domain.user import User


class UsersRepository:
    def __init__(self, users_list: dict[str, User]={}):
        self.users_list: dict[str, User] = users_list

    def add_user(self, user: User):
        self.users_list[user.user_name] = user
        
    def get_admins(self, admin_id: int) -> User:
        user = self.get_employee_by_id(admin_id)
        if user.rol == "admin":
            return user
        raise Exception("El ID del usuario que ejecuta la accion no es el ID de un administrador")
            
    def get_employee_by_id(self, id: int) -> User:
        for user in self.users_list.values():
            user_id = int(user.employee_key.split(" ")[0])
            if user_id == id:
                return user
        
        raise Exception(f"El usuario de ID: {id} no se encuentra en la base de datos")

    def to_dict(self) -> dict:
        data = {}
        for user in self.users_list.values():
            data[user.user_name] = user.to_dict()
        return data

    @staticmethod
    def from_dict(data: dict) -> "UsersRepository":
        user_list = {}
        for key, u in data.items():
            user_list[key] = User.from_dict(u)
        
        return UsersRepository(user_list)