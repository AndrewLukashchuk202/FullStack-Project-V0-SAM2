from typing import TypedDict


class Coordinates(TypedDict):
    """
        A typed dictionary representing coordinates for mask generation.

        Attributes:
            included (list[tuple[int, int]]): A list of coordinate tuples to be included in the mask.
            excluded (list[tuple[int, int]]): A list of coordinate tuples to be excluded from the mask.
    """
    included: list[tuple[int, int]]
    excluded: list[tuple[int, int]]
