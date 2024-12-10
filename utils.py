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


def _format_item(item: "Item") -> str:
    """Formats an item for the outbound manifest

    Parameters
    ----------
    item : Item
        The item to format

    Returns
    -------
    str
        The formatted item
    """
    location = item["location"]

    x = str(location[0]).zfill(2)
    y = str(location[1]).zfill(2)
    weight = str(item["weight"]).zfill(5)
    company = item["company"]

    item_str = f"[{x},{y}], " + "{" + weight + "}, " + company
    return item_str


def save_modified_manifest(modified_manifest: list["Item"], file_name: str):
    """Saves the modified manifest

    Parameters
    ----------
    modified_manifest : list[Item]
        The modified manifest in json format
    """
    manifest_lst_str = [_format_item(item) for item in modified_manifest]

    manifest = "\n".join(manifest_lst_str)
    with open(f"{file_name}Outbound.txt", "w") as f:
        f.write(manifest)

def get_crate_names(parsed_manifest):
    for item in parsed_manifest:
        if item['company'] != 'UNUSED' and item['company'] != 'NAN':
            print(item['company'])

if __name__ == "__main__":
    from pprint import pprint

    i = 2
    # with open(f"Shipcase{i}.txt") as f:
    #     pprint(parse_manifest(f.read()))

    # with open(f"SilverQueen.txt") as f:
    #     pprint(parse_manifest(f.read()))

    # copy the json version of shipcase 2
    manifest_test = [
        {"company": "NAN", "location": (1, 1), "weight": 0},
        {"company": "NAN", "location": (1, 2), "weight": 0},
        {"company": "NAN", "location": (1, 3), "weight": 0},
        {"company": "Ram", "location": (1, 4), "weight": 120},
        {"company": "UNUSED", "location": (1, 5), "weight": 0},
        {"company": "UNUSED", "location": (1, 6), "weight": 0},
        {"company": "UNUSED", "location": (1, 7), "weight": 0},
        {"company": "UNUSED", "location": (1, 8), "weight": 0},
        {"company": "Owl", "location": (1, 9), "weight": 35},
        {"company": "NAN", "location": (1, 10), "weight": 0},
        {"company": "NAN", "location": (1, 11), "weight": 0},
        {"company": "NAN", "location": (1, 12), "weight": 0},
        {"company": "NAN", "location": (2, 1), "weight": 0},
        {"company": "Dog", "location": (2, 2), "weight": 50},
        {"company": "UNUSED", "location": (2, 3), "weight": 0},
        {"company": "UNUSED", "location": (2, 4), "weight": 0},
        {"company": "UNUSED", "location": (2, 5), "weight": 0},
        {"company": "UNUSED", "location": (2, 6), "weight": 0},
        {"company": "UNUSED", "location": (2, 7), "weight": 0},
        {"company": "UNUSED", "location": (2, 8), "weight": 0},
        {"company": "UNUSED", "location": (2, 9), "weight": 0},
        {"company": "UNUSED", "location": (2, 10), "weight": 0},
        {"company": "UNUSED", "location": (2, 11), "weight": 0},
        {"company": "NAN", "location": (2, 12), "weight": 0},
        {"company": "Cat", "location": (3, 1), "weight": 40},
        {"company": "UNUSED", "location": (3, 2), "weight": 0},
        {"company": "UNUSED", "location": (3, 3), "weight": 0},
        {"company": "UNUSED", "location": (3, 4), "weight": 0},
        {"company": "UNUSED", "location": (3, 5), "weight": 0},
        {"company": "UNUSED", "location": (3, 6), "weight": 0},
        {"company": "UNUSED", "location": (3, 7), "weight": 0},
        {"company": "UNUSED", "location": (3, 8), "weight": 0},
        {"company": "UNUSED", "location": (3, 9), "weight": 0},
        {"company": "UNUSED", "location": (3, 10), "weight": 0},
        {"company": "UNUSED", "location": (3, 11), "weight": 0},
        {"company": "UNUSED", "location": (3, 12), "weight": 0},
        {"company": "UNUSED", "location": (4, 1), "weight": 0},
        {"company": "UNUSED", "location": (4, 2), "weight": 0},
        {"company": "UNUSED", "location": (4, 3), "weight": 0},
        {"company": "UNUSED", "location": (4, 4), "weight": 0},
        {"company": "UNUSED", "location": (4, 5), "weight": 0},
        {"company": "UNUSED", "location": (4, 6), "weight": 0},
        {"company": "UNUSED", "location": (4, 7), "weight": 0},
        {"company": "UNUSED", "location": (4, 8), "weight": 0},
        {"company": "UNUSED", "location": (4, 9), "weight": 0},
        {"company": "UNUSED", "location": (4, 10), "weight": 0},
        {"company": "UNUSED", "location": (4, 11), "weight": 0},
        {"company": "UNUSED", "location": (4, 12), "weight": 0},
        {"company": "UNUSED", "location": (5, 1), "weight": 0},
        {"company": "UNUSED", "location": (5, 2), "weight": 0},
        {"company": "UNUSED", "location": (5, 3), "weight": 0},
        {"company": "UNUSED", "location": (5, 4), "weight": 0},
        {"company": "UNUSED", "location": (5, 5), "weight": 0},
        {"company": "UNUSED", "location": (5, 6), "weight": 0},
        {"company": "UNUSED", "location": (5, 7), "weight": 0},
        {"company": "UNUSED", "location": (5, 8), "weight": 0},
        {"company": "UNUSED", "location": (5, 9), "weight": 0},
        {"company": "UNUSED", "location": (5, 10), "weight": 0},
        {"company": "UNUSED", "location": (5, 11), "weight": 0},
        {"company": "UNUSED", "location": (5, 12), "weight": 0},
        {"company": "UNUSED", "location": (6, 1), "weight": 0},
        {"company": "UNUSED", "location": (6, 2), "weight": 0},
        {"company": "UNUSED", "location": (6, 3), "weight": 0},
        {"company": "UNUSED", "location": (6, 4), "weight": 0},
        {"company": "UNUSED", "location": (6, 5), "weight": 0},
        {"company": "UNUSED", "location": (6, 6), "weight": 0},
        {"company": "UNUSED", "location": (6, 7), "weight": 0},
        {"company": "UNUSED", "location": (6, 8), "weight": 0},
        {"company": "UNUSED", "location": (6, 9), "weight": 0},
        {"company": "UNUSED", "location": (6, 10), "weight": 0},
        {"company": "UNUSED", "location": (6, 11), "weight": 0},
        {"company": "UNUSED", "location": (6, 12), "weight": 0},
        {"company": "UNUSED", "location": (7, 1), "weight": 0},
        {"company": "UNUSED", "location": (7, 2), "weight": 0},
        {"company": "UNUSED", "location": (7, 3), "weight": 0},
        {"company": "UNUSED", "location": (7, 4), "weight": 0},
        {"company": "UNUSED", "location": (7, 5), "weight": 0},
        {"company": "UNUSED", "location": (7, 6), "weight": 0},
        {"company": "UNUSED", "location": (7, 7), "weight": 0},
        {"company": "UNUSED", "location": (7, 8), "weight": 0},
        {"company": "UNUSED", "location": (7, 9), "weight": 0},
        {"company": "UNUSED", "location": (7, 10), "weight": 0},
        {"company": "UNUSED", "location": (7, 11), "weight": 0},
        {"company": "UNUSED", "location": (7, 12), "weight": 0},
        {"company": "UNUSED", "location": (8, 1), "weight": 0},
        {"company": "UNUSED", "location": (8, 2), "weight": 0},
        {"company": "UNUSED", "location": (8, 3), "weight": 0},
        {"company": "UNUSED", "location": (8, 4), "weight": 0},
        {"company": "UNUSED", "location": (8, 5), "weight": 0},
        {"company": "UNUSED", "location": (8, 6), "weight": 0},
        {"company": "UNUSED", "location": (8, 7), "weight": 0},
        {"company": "UNUSED", "location": (8, 8), "weight": 0},
        {"company": "UNUSED", "location": (8, 9), "weight": 0},
        {"company": "UNUSED", "location": (8, 10), "weight": 0},
        {"company": "UNUSED", "location": (8, 11), "weight": 0},
        {"company": "UNUSED", "location": (8, 12), "weight": 0},
    ]
    save_modified_manifest(manifest_test, f"Shipcase{i}")
    import filecmp

    print(filecmp.cmp(f"Shipcase{i}.txt", f"Shipcase{i}Outbound.txt"))
