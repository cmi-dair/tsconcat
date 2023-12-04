"""Print a tree from a list of paths."""

import pathlib as pl
from typing import Dict, List, Optional, Sequence, Union

from rich.console import Console

console = Console(highlight=False)


def tree_from_paths(paths: Sequence[Union[str, pl.Path]]) -> dict:
    """Build a tree from a list of paths."""
    tree: Dict[str, dict] = {}
    for p in (pl.Path(p) for p in paths):
        parts = list(p.parts)

        node = tree
        while True:
            if len(parts) == 0:
                break
            segment = parts.pop(0)

            child = node.get(segment, None)

            if child is None:
                child = {}
                node[segment] = child

            node = child
    return tree


def tree_collapse(tree: dict) -> dict:
    """Collapse a tree by merging single-child nodes."""
    stack = [tree]
    while True:
        if len(stack) == 0:
            break
        node = stack.pop(0)

        updated_node = False

        for node_name, child in node.items():
            if len(child) == 1:
                child_name, childchild = tuple(child.items())[0]
                del node[node_name]
                node[str(pl.Path(node_name) / child_name)] = childchild
                updated_node = True
                break

        if updated_node:
            stack.insert(0, node)
        else:
            for child in node.values():
                stack.append(child)

    return tree


INDENT_T = "├── "
INDENT_L = "└── "
INDENT_O = "    "
INDENT_I = "│   "
RAINBOW_COLORS = ["red", "green", "blue", "magenta", "cyan"]


def tree_print(tree: dict, indents: Optional[List[bool]] = None) -> None:
    """Print a tree."""
    indents = [] if indents is None else indents

    for i, (k, v) in enumerate(tree.items()):
        is_last_child = i == len(tree) - 1

        indent_list = [
            ((INDENT_L if is_last_child else INDENT_T) if level == len(indents) else INDENT_I) if ind else INDENT_O
            for level, ind in enumerate(indents + [True])
            if level > 0
        ]

        indent_list = [
            f"[{RAINBOW_COLORS[level % len(RAINBOW_COLORS)]}]{ind}[/]" for level, ind in enumerate(indent_list)
        ]

        total_indent = "".join(indent_list)
        console.print(f"{total_indent}{k}")
        tree_print(v, indents + [not is_last_child])


def pretreeprint(paths: Sequence[Union[str, pl.Path]]) -> None:
    """Print a tree from a list of paths."""
    tree_print(tree_collapse(tree_from_paths(paths)))


if __name__ == "__main__":
    from glob import glob

    pretreeprint(list(glob("../../**", recursive=True)))
