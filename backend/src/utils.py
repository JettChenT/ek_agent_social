from typing import Any, List

def flatten(lst: List[List[Any]]) -> List[Any]:
    return [item for sublist in lst for item in sublist]


def spread(lst: List[Any]) -> List[Any]:
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(spread(item))
        else:
            result.append(item)
    return result