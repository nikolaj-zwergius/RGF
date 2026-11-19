import json
from pathlib import Path
from jsonschema import validate


with open("RGF.json") as f:
    schema = json.load(f)


class interaction:
    def __init__(self, source_edge,target_edge,target):
        self.interaction_type = self.compute_type(source_edge,target_edge)
        self.target = target
        self.target_edge = target_edge

    def compute_type(self,source_edge,target_edge):
        pass
    
    def to_dict(self):
        pass

    def __repr__(self):
        return f"{self.target_edge} of {self.target} as {self.interaction_type}"

class node:
    def __init__(self,id:int):
        self.id: int = id




interactions_faces = ["5p","3p","Watson","Hoogsteen","Sugar","5p-stack","3p-stack"]


class Nucleotide_node(node):
    def __init__(self, id, base):
        super().__init__(id)
        
        self.connections: dict[str,interaction|None] = {}
        for face in interactions_faces:
            self.connections[face] = None
        self.base = base
        self.next_chain = None
    
    @classmethod
    def dict_to_node(self,line:dict):
        _node = Nucleotide_node(line["id"],line["base"])
        
        for face in interactions_faces:
            face_interaction = line["connections"].get(face)
            if face_interaction is not None:
                _node.add_interaction(face,interaction(face,face_interaction["target_edge"],face_interaction["target_id"]))
        _node.next_chain = line.get("next chain")
        
        return _node



    def to_dict(self):
        output = {"id":self.id,"base":self.base,"connections":{}}
        for connection in self.connections:
            if self.connections[connection] is not None:
                output["connections"][connection] = {"target_id":self.connections[connection].target,"target_edge":self.connections[connection].target_edge}
        return output


    def add_interaction(self,face,interaction):
        if self.connections[face] is not None:
            raise KeyError("connection already connected to a partner")
        self.connections[face] = interaction
        pass

    def __repr__(self):
        return f"{self.base}"

class motif(node):
    def __init__(self,name,id):
        super().__init__(id)
        self.name = name
        self.children = []
    
    def add_children(self,children:list):
        pass
    
    @classmethod
    def dict_to_node(self,line:dict):
        pass

class graph:
    def __init__(self):
        self.nodes: dict[int, Nucleotide_node] = {}
        self.first = None
        self.last = None

    def add_node(self,node):
        if self.first is None:
            self.first = node
        self.nodes[node.id] = node


    def remove_node(self,id):
        pass

class state_diff:
    def __init__(id,diff_list):
        self.id:int = id
        self.diff_list:list[Nucleotide_node] = diff_list


class Strand_graph(graph):
    def __init__(self,states = None):
        super().__init__()
        self.states = states

    def to_dict(self):
        output= []
        node = self.first
        while node.connections["3p"] is not None:
            output.append(node.to_dict())
            node = self.nodes[node.connections["3p"].target]
            if node.connections["3p"] is not None:
                continue
            if node.next_chain is None:
                continue
            raise NotImplementedError("Next chain logic is not implmented yet")

        return output

    def states_to_dict():
        pass

    def add_diff(self,diff:state_diff):
        pass

    def remove_diff(self,index):
        pass


class motif_graph:
    def __init__(self):
        super().__init__()
    


class RGF:
    def __init__(self,file=None):
        self.file = None
        self.meta_data = {}
        self.design = {}
        self.derived = {}
        self.attached = {}
        self.current_max_node_index = 0
        self.current_max_motif_index = 0
        self.strand_graph = Strand_graph()
        self.motif_graph = motif_graph()
    
    @classmethod
    def load(self,file):
        rgf = RGF()
        with open(file) as f:
            data = json.load(f)
        validate(data,schema)
        rgf.file = file
        rgf.meta_data = data["Metadata"]
        rgf.design = data["Design"]
        rgf.derived = data.get("Derived Data")
        rgf.attached = data.get("attached data")

        rgf.current_max_node_index = int(rgf.meta_data.get("CurrentMaxNodeIndex"))
        rgf.current_max_Motif_index = int(rgf.meta_data.get("CurrentMaxMotifIndex"))

        for i in rgf.design["Strand Graph"]:
            rgf.strand_graph.add_node(Nucleotide_node.dict_to_node(i))
        for i in rgf.design.get("Motif Graph",[]):
            rgf.strand_graph.add_node(motif.dict_to_node(i))
        return rgf
    
    def to_dict(self):
        self_dict = {
            "Metadata":self.meta_data,
            "Design":self.design
        }

        self.design["Strand Graph"] = self.strand_graph.to_dict()

        if self.derived is not None:
            self_dict["Derived data"] = self.derived
        if self.attached is not None:
            self_dict["attached data"] = self.attached

        return self_dict


    def save_to_json(self,file_name = None):
        if file_name is None:
            file_name = self.file
        data = self.to_dict()
        self.meta_data["CurrentMaxNodeIndex"] = self.current_max_node_index
        self.meta_data["CurrentMaxMotifIndex"] = self.current_max_Motif_index
        validate(data,schema)
        with open(file_name, "w") as f:
            json.dump(data,f,indent=4)

    def prepend_to(self,target:RGF):
        pass

    def append_to(self,target:RGF):
        pass

    def compact_ids(self):
        pass
    
    def json_formatter(self,dump:str) -> str:
        pass



