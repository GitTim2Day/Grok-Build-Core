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
    print("SIZE", by_size)
    print("DENSITY", by_density)
    print("ALL_GREEN")
