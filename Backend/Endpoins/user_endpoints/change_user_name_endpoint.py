from Backend.Data_Access.context import Context


class ChangeUserNameEndpoint:

    def excecute(self, id: int, password: str, new_user_name: str):
        if new_user_name == "":
            raise Exception("Debe introducir su nuevo nombre")
        context = Context()
        user_repo = context.get_repo_users()
        user = user_repo.get_employee_by_id(id)
        user.change_user_name(new_user_name, password)
        context.save(user_repo)
        print(f"Se ha cambiado el user name del usuario de ID: {id} correctamente")
