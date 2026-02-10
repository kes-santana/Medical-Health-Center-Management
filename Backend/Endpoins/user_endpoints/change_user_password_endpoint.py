from Backend.Data_Access.context import Context


class ChangeUserPasswordEndpoint:

    def excecute(self, id, password, new_password, new_password_copy):
        if new_password == "":
            raise Exception("Debe introducir su nueva password")
        if not new_password == new_password_copy:
            raise Exception("Verifique la nueva password y la confirmacion sean iguales.")
        
        context = Context()
        user_repo = context.get_repo_users()
        user = user_repo.get_employee_by_id(id)
        user.change_password(password, new_password)
        context.save(user_repo)
        print(f"Se ha cambiado el password del usuario de ID: {id} correctamente")
