from typing import List
import networkx as nx


class RiskScorer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def score_path(self, path: List[str]) -> dict:
        score = 0
        reasons = []

        # 1. Path length (shorter = higher risk)
        length_penalty = max(0, 10 - len(path))
        score += length_penalty
        reasons.append(f"Path length = {len(path)}")

        # 2. Privilege escalation detection
        for node in path:
            node_type = self.graph.nodes[node].get("type")
            if node_type == "role":
                score += 30
                reasons.append("Privilege escalation via role access")
                break

        # 3. Sensitive target reached
        final_node = path[-1]
        final_type = self.graph.nodes[final_node].get("type")
        if final_type == "data":
            score += 40
            reasons.append("Sensitive data asset reached")

        # 4. External entry point
        entry_type = self.graph.nodes[path[0]].get("type")
        if entry_type == "external":
            score += 20
            reasons.append("Externally reachable entry point")

        return {
            "path": path,
            "risk_score": score,
            "reasons": reasons
        }
