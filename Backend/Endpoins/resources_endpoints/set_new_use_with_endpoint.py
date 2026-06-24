
from backend.data_access.context import Context
from backend.domain.resources import Resource



class SetNewUseWithEndpoint:
    def excecute(self,resource_id: int, restricted_resource_id: int) -> None:
        
        context = Context()
        resources_repo = context.get_repo_resource()
        resource_id: Resource = resources_repo.get_by_id(resource_id)

        if restricted_resource_id in resource_id.use_with:
            raise Exception("El recurso ya estaba agregado")
        
        resource_id.use_with.append(restricted_resource_id)
        resource_id.verificar_dependencias(resources_repo)
        resource_id.revisar_codependencias(resources_repo)
        resources_repo.to_dict()
        context.save(resources_repo)
        print(f"Ahora es necesario usar el recurso {resource_id.name} junto al recurso de ID: {restricted_resource_id}")
