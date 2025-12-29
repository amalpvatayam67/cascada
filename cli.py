import json
import argparse
from pathlib import Path

from core.models import SystemModel
from core.graph_builder import AttackGraph
from core.path_engine import PathEngine
from core.scorer import RiskScorer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cascada – Cascading Attack Path Analysis Engine"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to system description JSON"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    return parser.parse_args()


def load_system(path: Path) -> SystemModel:
    with open(path, "r") as f:
        data = json.load(f)
    return SystemModel(**data)


def output_text(scored_paths):
    print("\nDiscovered & Scored Attack Paths:\n")
    for idx, item in enumerate(scored_paths, 1):
        print(f"{idx}. {' -> '.join(item['path'])}")
        print(f"   Risk Score: {item['risk_score']}")
        for reason in item["reasons"]:
            print(f"   - {reason}")
        print()


def output_json(scored_paths):
    return {
        "metadata": {
            "tool": "cascada",
            "version": "0.1",
            "paths_analyzed": len(scored_paths)
        },
        "results": scored_paths
    }


if __name__ == "__main__":
    args = parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        exit(1)

    system = load_system(input_path)

    graph = AttackGraph().build(system)
    engine = PathEngine(graph, max_depth=6)
    paths = engine.find_paths(system.entry_points, system.targets)

    scorer = RiskScorer(graph)
    scored_paths = [scorer.score_path(p) for p in paths]
    scored_paths.sort(key=lambda x: x["risk_score"], reverse=True)

    if args.format == "json":
        print(json.dumps(output_json(scored_paths), indent=2))
    else:
        output_text(scored_paths)
