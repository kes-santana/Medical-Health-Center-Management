from Backend.Data_Access import context
from constants import Events


contexto = context.Context()
repo = contexto.get_repo(Events)
