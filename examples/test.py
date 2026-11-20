import sys
from pathlib import Path


sys.path.insert(
0,
str(Path(__file__).parent.parent)
)


from pyRGF.RGF import RGF, Nucleotide_node
rgf =  RGF.load("examples/test.json")

rgf.strand_graph.add_node(Nucleotide_node(10,"C"))

rgf.save_to_json("examples/test2.json")