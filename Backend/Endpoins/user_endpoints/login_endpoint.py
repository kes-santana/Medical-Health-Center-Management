from Backend.Data_Access.context import Context


class LoginEndpoint:
    
    def excecute(self, user_intput, password_input) -> tuple[bool, str, str]:
        
        context = Context()
        user_repo = context.get_repo_users()
        user  = user_repo.users_list.get(user_intput, None)
        if user:
            print("Comprobando datos de login")
            return user.password == password_input, user.user_name, user.rol, user.employee_key
        
        return (False, "", "", "")
