import json
from pathlib import Path
from jsonschema import validate


with open("RGF.json") as f:
    schema = json.load(f)


class interaction:
    def __init__(self, name, type, source, target):
        self.name = name
        self.type = type
        self.source = source
        self.target = target

class node:
    def __init__(self,id):
        self.id: int = id


class Nucleotide_node(node):
    def __init__(self, type, id):
        super().__init__(id)
        self.type = type
        self.connections: list[interaction] = []

class motif(node):
    def __init__(self,name,id,index):
        super().__init__(id)
        self.name = name
        self.children = self.index_children(index)
    
    def index_children(index) -> dict[Nucleotide_node]:
        pass

class graph:
    def __init__(self):
        self.nodes: dict[int, Nucleotide_node] = {}
    def add_node(self,index):
        pass
    def remove_node(self,id):
        pass

class state_diff:
    def __init__(id,diff_list):
        self.id:int = id
        self.diff_list:list[Nucleotide_node] = diff_list


class Strand_graph(graph):
    def __init__(self,states):
        super().__init__()
        self.states = states

    def add_diff(self,diff:state_diff):
        pass

    def remove_diff(self,index):
        pass


class motif_graph:
    def __init__(id):
        super().__init__(id)



class RGF:
    def __init__(self,file):
        with open(file) as f:
            data = json.load(f)
        validate(data,schema)
        self.file = file
        self.meta_data = data["Metadata"]
        self.design = data["Design"]
        self.derived = data.get("Derived Data")
        self.attached = data.get("attached data")
    def to_dict(self):
        self_dict = {
            "Metadata":self.meta_data,
            "Design": self.design,
        }

        if self.derived is not None:
            self_dict["Derived data"] = self.derived
        if self.attached is not None:
            self_dict["attached data"] = self.attached

        return self_dict


    def save_to_json(self,file_name = None):
        if file_name is None:
            file_name = self.file
        data = self.to_dict()
        validate(data,schema)
        with open(file_name, "w") as f:
            json.dump(data,f,indent=4)




