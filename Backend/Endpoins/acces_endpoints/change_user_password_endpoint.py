from Backend.Data_Access.context import Context


class ChangeUserPasswordEndpoint:

    def excecute(self, id, password, new_password):
        context = Context()
        user_repo = context.get_repo_users()
        user = user_repo.get_by_employee_id(id)
        user.change_password(password, new_password)
        context.save(user_repo)
        print(f"Se ha cambiado el password del usuario de ID: {id} correctamente")
