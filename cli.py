import json
import argparse
from pathlib import Path

from core.models import SystemModel
from core.graph_builder import AttackGraph
from core.path_engine import PathEngine
from core.scorer import RiskScorer


BASE_DIR = Path(__file__).resolve().parent
RULES_DIR = BASE_DIR / "core" / "rules"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cascada – Cascading Attack Path Analysis Engine"
    )

    # -----------------------------
    # Input / Output
    # -----------------------------
    parser.add_argument(
        "-i", "--input",
        help="Path to system description JSON"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    # -----------------------------
    # Engine configuration
    # -----------------------------
    parser.add_argument(
        "--path-mode",
        choices=["first_impact", "full"],
        default="first_impact",
        help="Attack path exploration mode"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=6,
        help="Maximum depth of attack paths"
    )
    parser.add_argument(
        "--max-paths",
        type=int,
        default=50,
        help="Maximum number of attack paths"
    )
    parser.add_argument(
        "--profile",
        choices=["default", "cloud", "onprem"],
        default="default",
        help="Risk scoring profile"
    )

    # -----------------------------
    # Meta / UX
    # -----------------------------
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Explain engine configuration used for this run"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show Cascada version and exit"
    )

    args = parser.parse_args()

    # -----------------------------
    # Early exit: version
    # -----------------------------
    if args.version:
        print("Cascada v0.1.0")
        print("Attack Path Reasoning Engine (Design-time)")
        exit(0)

    # -----------------------------
    # Validation guards
    # -----------------------------
    if not args.input:
        parser.error("the following arguments are required: -i/--input")

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
            "version": "0.1.0",
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

    # -----------------------------
    # Explain configuration (optional)
    # -----------------------------
    if args.explain:
        print("\n[Engine Configuration]")
        print(f"Path mode   : {args.path_mode}")
        print(f"Max depth   : {args.max_depth}")
        print(f"Max paths   : {args.max_paths}")
        print(f"Risk profile: {args.profile}\n")

    # -----------------------------
    # Load & build system
    # -----------------------------
    system = load_system(input_path)
    graph = AttackGraph().build(system)

    engine = PathEngine(
        graph,
        max_depth=args.max_depth,
        max_paths=args.max_paths,
        path_mode=args.path_mode
    )

    paths = engine.find_paths(system.entry_points, system.targets)

    # -----------------------------
    # Score paths
    # -----------------------------
    rules_file = RULES_DIR / f"{args.profile}.json"
    scorer = RiskScorer(graph, rules_file)

    scored_paths = [scorer.score_path(p) for p in paths]
    scored_paths.sort(key=lambda x: x["risk_score"], reverse=True)

    # -----------------------------
    # Persist output for UI
    # -----------------------------
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "latest.json", "w") as f:
        json.dump(output_json(scored_paths), f, indent=2)

    # -----------------------------
    # Terminal output
    # -----------------------------
    if args.format == "json":
        print(json.dumps(output_json(scored_paths), indent=2))
    else:
        output_text(scored_paths)
