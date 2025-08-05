from pydantic import BaseModel, ValidationError, constr, conint

class MachineModel(BaseModel):
    name: constr(min_length=1, max_length=12)
    os: str
    cpu: conint(gt=0)
    ram: conint(gt=0)

class Machine:
    supported_os = ["linux", "windows", "macos", "mac", "win", "unix"]

    def __init__(self, name: str, os: str, cpu: int, ram: int):
        self.model = MachineModel(name=name, os=os.lower(), cpu=cpu, ram=ram)

    @property
    def as_dict(self):
        return self.model.model_dump()

    def __str__(self):
        return f"{self.model.name} | OS: {self.model.os} | CPU: {self.model.cpu} | RAM: {self.model.ram}GB"
