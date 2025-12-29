import json
from pathlib import Path


class RiskScorer:
    def __init__(self, graph, rules_file: Path):
        self.graph = graph

        with open(rules_file, "r") as f:
            rules = json.load(f)

        self.weights = rules["weights"]

    def score_path(self, path):
        score = 0
        reasons = []

        # Path length
        path_len = len(path)
        score += path_len * self.weights["path_length"]
        reasons.append(f"Path length = {path_len}")

        # External entry
        if path[0] == "internet":
            score += self.weights["external_entry"]
            reasons.append("Externally reachable entry point")

        # Privilege escalation
        if any("role" in node for node in path):
            score += self.weights["privilege_escalation"]
            reasons.append("Privilege escalation via role access")

        # Sensitive asset
        if "db" in path:
            score += self.weights["sensitive_asset"]
            reasons.append("Sensitive data asset reached")

        return {
            "path": path,
            "risk_score": score,
            "reasons": reasons
        }
