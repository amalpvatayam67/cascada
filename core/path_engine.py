from typing import List, Set
import networkx as nx


class PathEngine:
    def __init__(
        self,
        graph: nx.DiGraph,
        max_depth: int = 6,
        max_paths: int = 50
    ):
        self.graph = graph
        self.max_depth = max_depth
        self.max_paths = max_paths

    def find_paths(
        self,
        entry_points: List[str],
        targets: List[str]
    ) -> List[List[str]]:
        results: List[List[str]] = []
        target_set: Set[str] = set(targets)

        for entry in entry_points:
            if len(results) >= self.max_paths:
                break

            self._dfs(
                current=entry,
                targets=target_set,
                path=[entry],
                visited={entry},
                results=results
            )

        return results

    def _dfs(
        self,
        current: str,
        targets: Set[str],
        path: List[str],
        visited: Set[str],
        results: List[List[str]]
    ):
        # Global path limit guard
        if len(results) >= self.max_paths:
            return

        # Depth guard
        if len(path) > self.max_depth:
            return

        # Target reached
        if current in targets:
            results.append(list(path))
            return

        # Traverse neighbors
        for neighbor in self.graph.successors(current):
            if neighbor in visited:
                continue  # cycle protection

            visited.add(neighbor)
            path.append(neighbor)

            self._dfs(
                current=neighbor,
                targets=targets,
                path=path,
                visited=visited,
                results=results
            )

            # Backtrack
            path.pop()
            visited.remove(neighbor)
