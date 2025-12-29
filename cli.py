import json
from core.models import SystemModel
from core.graph_builder import AttackGraph
from core.path_engine import PathEngine
from core.scorer import RiskScorer


def load_system(path: str) -> SystemModel:
    with open(path, "r") as f:
        data = json.load(f)
    return SystemModel(**data)


if __name__ == "__main__":
    system = load_system("inputs/sample_system.json")

    graph = AttackGraph().build(system)

    engine = PathEngine(graph, max_depth=6)
    paths = engine.find_paths(system.entry_points, system.targets)

    scorer = RiskScorer(graph)
scored_paths = [scorer.score_path(p) for p in paths]

# Sort by risk score (descending)
scored_paths.sort(key=lambda x: x["risk_score"], reverse=True)

print("\nDiscovered & Scored Attack Paths:\n")
for idx, item in enumerate(scored_paths, 1):
    print(f"{idx}. {' -> '.join(item['path'])}")
    print(f"   Risk Score: {item['risk_score']}")
    for reason in item["reasons"]:
        print(f"   - {reason}")
    print()
