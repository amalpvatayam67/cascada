import networkx as nx


class AttackGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, system):
        # Add nodes
        for entity in system.entities:
            self.graph.add_node(entity.id, type=entity.type)

        # Add edges
        for rel in system.relationships:
            self.graph.add_edge(
                rel.from_,   # FIXED
                rel.to,      # FIXED
                type=rel.type
            )

        return self.graph
