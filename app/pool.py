from dataclasses import dataclass
import json

@dataclass
class Pool:
    def __init__(self, name, count, mode, type, os_type, vm_size):
        self.name = name
        self.count = count
        self.mode = mode
        self.type = type
        self.os_type = os_type
        self.vm_size = vm_size

    def to_dict(self):
        return {
            "name": self.name,
            "count": self.count,
            "mode": self.mode,
            "type": self.type,
            "os_type": self.os_type,
            "vm_size": self.vm_size
        }

    def toJSON(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return f"Pool - Name: {self.name}, Count: {self.count}, Mode: {self.mode}, Type: {self.type}, OS: {self.os_type}, VM Size: {self.vm_size}"
    
class PoolEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pool):
            return {
                "name": obj.name,
                "count": obj.count,
                "mode": obj.mode,
                "type": obj.type,
                "os_type": obj.os_type,
                "vm_size": obj.vm_size
            }
        return super().default(obj)
