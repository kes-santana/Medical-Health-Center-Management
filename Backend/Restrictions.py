
from Backend.Domain import resources


class Restricctions:

    def __init__(self):
        pass

    def add_restriction(self, new_restriction: resources.Resource,
                         use_resourse_with: list[resources.Resource]=None, 
                         dont_use_resourse_with: list[resources.Resource]=None) -> None:
        
        # TODO ver si funciona con any   
        #     if not any(j.id == i.id):
        #         resource.restrictions.append(i)

        count = 0
        resource_restrictions = use_resourse_with if use_resourse_with is not None else dont_use_resourse_with
        new_list = []
        for i in resource_restrictions:
            if i.id == new_restriction.id:
                #todo mandar mensaje de que la restriccion ya existe
                return
        
            # if i.id != new_restriction.id:
            #     if count == len(resource_restrictions) - 1:
            #         new_list.append(i)
            #     else:
            #         count += 1
            #         continue

        resource_restrictions.append(i)

    def delete_restriction(self, resource_restrictions: list[resources.Resource],
                            restriction_delete : resources.Resource) -> None:
        
        for i in resource_restrictions:
            if i.id == restriction_delete.id:
                del resource_restrictions[i]
                return
        
        #todo mandar mensaje de que la restriccion no existe

    def create_restriction(self): #todo
        pass
