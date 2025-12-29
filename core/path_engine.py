from typing import List
import networkx as nx


class PathEngine:
    def __init__(self, graph: nx.DiGraph, max_depth: int = 6):
        self.graph = graph
        self.max_depth = max_depth

    def find_paths(self, entry_points: List[str], targets: List[str]) -> List[List[str]]:
        results = []

        for entry in entry_points:
            self._dfs(
                current=entry,
                targets=set(targets),
                path=[entry],
                visited={entry},
                results=results
            )

        return results

    def _dfs(self, current, targets, path, visited, results):
        if len(path) > self.max_depth:
            return

        if current in targets:
            results.append(list(path))
            return

        for neighbor in self.graph.successors(current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            path.append(neighbor)

            self._dfs(neighbor, targets, path, visited, results)

            path.pop()
            visited.remove(neighbor)
