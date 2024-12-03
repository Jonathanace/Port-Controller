import re
from typing import TYPE_CHECKING, TypedDict

class Item(TypedDict):
    company: str
    location: tuple[int, int]
    weight: int


def parse_manifest(manifest: str) -> list["Item"]:
    """Parses the manifest

    Parameters
    ----------
    manifest : str
        The manifest data as str

    Returns
    -------
    list[Item]
        The list of dict containt the item's location, weight, and company
    """

    items: list["Item"] = []
    for match in re.finditer(
        r"\[(?P<LocationX>\d\d),(?P<LocationY>\d\d)\], {(?P<Weight>\d\d\d\d\d)}, (?P<Company>[\S ]+)",
        manifest,
    ):
        data = match.groupdict()
        x = int(data["LocationX"])
        y = int(data["LocationY"])
        weight = int(data["Weight"])
        company = data["Company"]

        items.append({"location": (x, y), "weight": weight, "company": company})

    return items


if __name__ == "__main__":
    from pprint import pprint

    # i = 2
    # with open(f"Shipcase{i}.txt") as f:
    #     pprint(parse_manifest(f.read()))

    with open(f"SilverQueen.txt") as f:
        pprint(parse_manifest(f.read()))
