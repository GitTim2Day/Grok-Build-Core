# Escalator. His word, 2026-09-24.
# When the stopping blocks pile up, vibrate until they sort
# into groups by a measure they already carry: size, or density.
# No new cutoff. An item with no measure is held, not forced.

def escalate(items, key):
    held = []
    moving = []
    for item in items:
        if item.get(key) is None:
            held.append(item["name"])
        else:
            moving.append(item)

    passes = 0
    if len(moving) > 1:
        start = 0
        end = len(moving) - 1
        swapped = True
        while swapped:
            swapped = False
            passes += 1
            for i in range(start, end):
                if moving[i][key] > moving[i + 1][key]:
                    moving[i], moving[i + 1] = moving[i + 1], moving[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end, start, -1):
                if moving[i - 1][key] > moving[i][key]:
                    moving[i - 1], moving[i] = moving[i], moving[i - 1]
                    swapped = True
            start += 1

    groups = []
    for item in moving:
        if not groups or groups[-1][0] != item[key]:
            groups.append([item[key], [item["name"]]])
        else:
            groups[-1][1].append(item["name"])
    return {"key": key, "passes": passes, "groups": groups, "held": held}


def pan(items):
    # A little water is truth/logic. One wash. Not a flood.
    # The densest group stays. That flash is the scintillation.
    # Lighter groups are carried off. No measure stays held.
    shaken = escalate(items, "density")
    if not shaken["groups"]:
        return {"gold": None, "wash": [], "held": shaken["held"], "flash": False}
    gold = shaken["groups"][-1]
    wash = shaken["groups"][:-1]
    return {"gold": gold, "wash": wash, "held": shaken["held"], "flash": True}


def second_cut(items, key_a, key_b):
    # Axis one keeps every band. Axis two recuts each band.
    # Nothing is poured out. A close pair splits only on the second key.
    first = escalate(items, key_a)
    by_name = {item["name"]: item for item in items}
    bands = []
    for value, names in first["groups"]:
        members = [by_name[name] for name in names]
        second = escalate(members, key_b)
        bands.append({"on": key_a, "value": value, "by": key_b, "groups": second["groups"], "held": second["held"]})
    return {"bands": bands, "held": first["held"]}


if __name__ == "__main__":
    # Demo labels only. Not measured densities.
    blocks = [
        {"name": "leaf", "size": 2, "density": 1},
        {"name": "root", "size": 5, "density": 4},
        {"name": "capillary", "size": 2, "density": 2},
        {"name": "branch", "size": 3, "density": 2},
        {"name": "fruit", "size": 3, "density": 3},
        {"name": "mesentery", "size": None, "density": None},
    ]
    by_size = escalate(blocks, "size")
    by_density = escalate(blocks, "density")
    assert by_size["held"] == ["mesentery"]
    assert by_density["held"] == ["mesentery"]
    assert by_size["groups"][0][1] == ["leaf", "capillary"]
    assert by_density["groups"][1][1] == ["capillary", "branch"]
    panned = pan(blocks)
    assert panned["flash"] is True
    assert panned["gold"][1] == ["root"]
    assert panned["held"] == ["mesentery"]
    assert [name for group in panned["wash"] for name in group[1]] == [
        "leaf",
        "capillary",
        "branch",
        "fruit",
    ]
    print("SIZE", by_size)
    print("DENSITY", by_density)
    print("PAN", panned)
    cut = second_cut(blocks, "size", "density")
    size_two = [band for band in cut["bands"] if band["value"] == 2][0]
    assert [group[1] for group in size_two["groups"]] == [["leaf"], ["capillary"]]
    assert cut["held"] == ["mesentery"]
    print("SECOND", cut)
    print("ALL_GREEN")
