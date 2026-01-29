class User:
    def __init__(self, id: int, user_name: str, employee_key: str, password: str, rol: str):
        self.id = id
        self.user_name: str = user_name
        self.employee_key: str = employee_key
        self.password: str = password
        self.rol: str = rol

    def change_user_name(self, new_user_name, password):
        if self.password == password:
            self.user_name = new_user_name
            return
        raise Exception("Password no valida")
    
    def change_password(self, password, new_password):
        if self.password == password:
            self.password = new_password
            return
        raise Exception("Password no valida")
        
    def change_rol(self, new_rol):
        self.rol = new_rol

    def to_dict(self) -> dict:
        """Convierte el usuario a un diccionario"""

        return {
            "id": self.id,
            "user_name": self.user_name,
            "employee_key": self.employee_key,
            "password": self.password,
            "rol": self.rol
            }
    
    @staticmethod
    def from_dict(data:dict) -> "User":
        id = data["id"]
        user_name = data["user_name"]
        employee_key = data["employee_key"]
        password = data["password"]
        rol = data["rol"]

        return User(id, user_name, employee_key, password, rol)