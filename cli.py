import json
import argparse
from pathlib import Path

from core.models import SystemModel
from core.graph_builder import AttackGraph
from core.path_engine import PathEngine
from core.scorer import RiskScorer


BASE_DIR = Path(__file__).resolve().parent
RULES_FILE = BASE_DIR / "core" / "rules.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cascada – Cascading Attack Path Analysis Engine"
    )

    # Input / Output
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to system description JSON"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    # Engine configuration
    parser.add_argument(
        "--path-mode",
        choices=["first_impact", "full"],
        default="first_impact",
        help="Attack path exploration mode (default: first_impact)"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=6,
        help="Maximum depth of attack paths (default: 6)"
    )
    parser.add_argument(
        "--max-paths",
        type=int,
        default=50,
        help="Maximum number of attack paths to discover (default: 50)"
    )

    args = parser.parse_args()

    # Validation guards
    if args.max_depth < 1 or args.max_depth > 20:
        parser.error("--max-depth must be between 1 and 20")

    if args.max_paths < 1 or args.max_paths > 500:
        parser.error("--max-paths must be between 1 and 500")

    return args


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

    # Load system
    system = load_system(input_path)

    # Build attack graph
    graph = AttackGraph().build(system)

    # Configure path engine from CLI
    engine = PathEngine(
        graph,
        max_depth=args.max_depth,
        max_paths=args.max_paths,
        path_mode=args.path_mode
    )

    paths = engine.find_paths(system.entry_points, system.targets)

    # Score paths
    scorer = RiskScorer(graph, RULES_FILE)
    scored_paths = [scorer.score_path(p) for p in paths]
    scored_paths.sort(key=lambda x: x["risk_score"], reverse=True)

    # Always persist latest result for UI
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "latest.json", "w") as f:
        json.dump(output_json(scored_paths), f, indent=2)

    # Terminal output control
    if args.format == "json":
        print(json.dumps(output_json(scored_paths), indent=2))
    else:
        output_text(scored_paths)
