# Cascada

**Cascada** is a **design-time attack path reasoning engine** that helps
security engineers, architects, and defenders understand how _access,
trust, and privilege relationships_ can cascade into critical impact ---
**before any vulnerability is exploited**.

Cascada is **offline, agentless, deterministic, and explainable**,
making it suitable for regulated, defense, and high‑assurance
environments.

---

## Why Cascada Exists

Most security tools answer: \> _"What vulnerabilities exist right now?"_

Cascada answers a different and earlier question: \> **"If something
goes wrong, how bad can it get --- and why?"**

It focuses on **blast radius**, **privilege escalation**, and **trust
abuse** at the _architecture level_.

---

## What Cascada Does

- Models systems as **entities and relationships**
- Builds a directed **attack graph**
- Discovers feasible **attack paths**
- Scores risk using **explainable rules**
- Explains _why_ a path is dangerous
- Works fully **offline**
- Requires **no credentials, agents, or cloud access**

---

## What Cascada Does NOT Do

Cascada is intentionally scoped.

- ❌ No vulnerability scanning
- ❌ No exploitation or payloads
- ❌ No live system interaction
- ❌ No cloud API access
- ❌ No AI guesswork or attacker simulation

This restraint is a **feature**, not a limitation.

---

## Typical Use Cases

- Security architecture reviews
- Cloud & IAM blast-radius analysis
- Zero-trust design validation
- Pre-deployment threat modeling
- Regulated or defense environments
- Security consulting demonstrations

---

## Architecture Overview

    System Model (JSON)
            ↓
       Validation Layer
            ↓
       Attack Graph Builder
            ↓
       Path Discovery Engine
            ↓
       Risk Scoring Engine
            ↓
     Explainable Results (Text / JSON / UI)

All reasoning is **deterministic and auditable**.

---

## Installation

```bash
git clone <repo-url>
cd cascada
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Quick Start

```bash
python cli.py -i inputs/realistic_system.json
```

---

## Advanced Usage

```bash
python cli.py -i inputs/realistic_system.json \
  --path-mode full \
  --profile cloud \
  --max-depth 8 \
  --max-paths 100 \
  --explain
```

---

## CLI Options

| Option           | Argument                     | Default        | Description                                |
| ---------------- | ---------------------------- | -------------- | ------------------------------------------ |
| `-i`, `--input`  | `<file>`                     | **required**   | Path to system model JSON file             |
| `--path-mode`    | `first_impact \| full`       | `first_impact` | Attack path discovery mode                 |
| `--max-depth`    | `<int>`                      | `6`            | Maximum length of an attack path           |
| `--max-paths`    | `<int>`                      | `50`           | Maximum number of attack paths to discover |
| `--profile`      | `default \| cloud \| onprem` | `default`      | Risk scoring rule profile                  |
| `-f`, `--format` | `text \| json`               | `text`         | Output format                              |
| `--explain`      | _(flag)_                     | —              | Explain engine configuration used          |
| `--version`      | _(flag)_                     | —              | Show tool version and exit                 |

---

## Path Mode Explained

| Mode           | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `first_impact` | Stops analysis when the first critical target is reached (default, faster) |
| `full`         | Explores all reachable attack paths up to configured limits                |

---

## Output

- **Terminal output** (human‑readable)
- **JSON output** (`outputs/latest.json`)
- **Optional local UI** for visualization

---

## Design Philosophy

Cascada prioritizes:

- Correctness over completeness
- Explainability over opacity
- Design-time insight over runtime noise
- Safety over exploitation
- Trust over automation hype

---

## Disclaimer

Cascada is a **design-time analysis tool**.

It does not guarantee security and does not replace professional
security assessments. All results depend on the accuracy of the input
model.

---

## License

Copyright (c) 2025 Amal P

All rights reserved.

This project is currently not licensed.

<!-- No permission is granted to use, copy, modify, or distribute this software
without explicit written permission from the author. -->

---

## Status

**Stable -- v0.1.0**\
Actively maintained and intentionally scoped.
