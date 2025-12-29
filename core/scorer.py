import json
from typing import List
import networkx as nx
from pathlib import Path


class RiskScorer:
    def __init__(self, graph: nx.DiGraph, rules_path: Path):
        self.graph = graph
        with open(rules_path, "r") as f:
            self.rules = json.load(f)

    def score_path(self, path: List[str]) -> dict:
        score = 0
        reasons = []

        # Path length rule
        if self.rules["path_length"]["enabled"]:
            base = self.rules["path_length"]["base"]
            length_score = max(0, base - len(path))
            score += length_score
            reasons.append(f"Path length = {len(path)}")

        # External entry rule
        if self.rules["external_entry"]["enabled"]:
            entry_type = self.graph.nodes[path[0]].get("type")
            if entry_type == "external":
                score += self.rules["external_entry"]["score"]
                reasons.append("Externally reachable entry point")

        # Privilege escalation rule
        if self.rules["privilege_escalation"]["enabled"]:
            for node in path:
                if self.graph.nodes[node].get("type") == "role":
                    score += self.rules["privilege_escalation"]["score"]
                    reasons.append("Privilege escalation via role access")
                    break

        # Sensitive target rule
        if self.rules["sensitive_target"]["enabled"]:
            final_type = self.graph.nodes[path[-1]].get("type")
            if final_type == "data":
                score += self.rules["sensitive_target"]["score"]
                reasons.append("Sensitive data asset reached")

        return {
            "path": path,
            "risk_score": score,
            "reasons": reasons
        }
