from backend.data_access.context import Context


class ChangeUserRolEndpoint:

    def excecute(self, admin_id, id, password, new_rol):
        context = Context()
        user_repo = context.get_repo_users()
        admin = user_repo.get_admins(admin_id)
        if admin.password == password:
            user = user_repo.get_employee_by_id(id)
            user.change_rol(new_rol)
            context.save(user_repo)
            print(f"Se ha cambiado el rol del usuario de ID: {id} correctamente")
            return
        
        raise Exception("La clave de acceso no es valida")
