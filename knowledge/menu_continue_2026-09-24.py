# Console menu. Disk work. Y stays. N or D returns.
# Other keys are ignored. Empty is not a choice.

def run(keys):
    place = "MENU"
    log = []
    for key in keys:
        k = key.upper()
        if place == "MENU":
            if k == "1":
                place = "DISK"
                log.append("CHAIN WORK")
            continue
        if k == "Y":
            log.append("STAY")
            continue
        if k in ("N", "D"):
            place = "MENU"
            log.append("CHAIN MENU")
            continue
    return place, log


if __name__ == "__main__":
    place, log = run(["1", "Y", "Y", "X", "N", "Q", "1", "D"])
    assert place == "MENU"
    assert log == ["CHAIN WORK", "STAY", "STAY", "CHAIN MENU", "CHAIN WORK", "CHAIN MENU"]
    place, log = run(["Y", "N"])
    assert place == "MENU"
    assert log == []
    print("ALL_GREEN")
