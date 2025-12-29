import networkx as nx
from core.models import SystemModel


class AttackGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, system: SystemModel) -> nx.DiGraph:
        # Add entities as nodes
        for entity in system.entities:
            self.graph.add_node(
                entity.id,
                type=entity.type
            )

        # Add relationships as edges
        for rel in system.relationships:
            self.graph.add_edge(
                rel.source,
                rel.target,
                type=rel.type
            )

        return self.graph
