from Backend.Data_Access.context import Context


class ChangeUserRolEndpoint:

    def excecute(self, id, password, new_rol):
        context = Context()
        user_repo = context.get_repo_users()
        admin = user_repo.get_admin()
        if admin.password == password:
            user = user_repo.get_by_employee_id(id)
            user.change_rol(new_rol)
            context.save(user_repo)
            print(f"Se ha cambiado el rol del usuario de ID: {id} correctamente")
        
        raise Exception("La clave de acceso no es valida")
