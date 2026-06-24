from backend.domain.resources import Resource


class ResourceDto:
    def __init__(self):
        self.id: int
        self.name: str
        self.use_state: str
        self.count: int
        self.is_espendable: bool
        self.use_with: list[str]
        self.dont_use_with: list[str]

    @staticmethod
    def to_resource_dto(resource: Resource) -> "ResourceDto":
        dto = ResourceDto()
        dto.id = resource.id
        dto.name = resource.name
        dto.use_state = resource.use_state
        dto.count = resource.count
        dto.is_espendable = resource.is_espendable
        dto.use_with = [r for r in resource.use_with]
        dto.dont_use_with = [r for r in resource.dont_use_with]
        return dto
    
    def __str__(self):
        return f"Resource: \n \
            Name: {self.name} \n \
            Use State: {self.use_state} \n \
            Count: {self.count} \n \
            Is Espendable: {self.is_espendable} \n"