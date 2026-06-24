from backend.data_access.context import Context
from backend.domain.employee import Employee
from backend.domain.user import User


class CreateUserEndpoint:

    def excecute(self, employee: Employee):
        context = Context()
        user_repo = context.get_repo_users()
        user_name = f"nuevo_empleado_{employee.name.lower().replace(" ", "_")}"
        password = ""
        for i in range(10):
            password += f"{i}"
        user = User(len(user_repo.users_list), user_name, employee.key, password, "doctor")
        user_repo.add_user(user)
        context.save(user_repo)
        print("Se creo el nuevo usuario con exito")