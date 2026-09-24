# One pass. Context, Content, Data, Time.
# A watched STT word is checked against the four. It is not searched one by one.

WATCH = {
    "green yard": {
        "meaning": "Grignard",
        "spelled": "G-R-I-G-N-A-R-D",
        "does_not_comply_when": "organic chemistry",
    }
}


def check(heard, context, content, data, time):
    word = heard.strip().lower()
    row = WATCH.get(word)
    if row is None:
        return {"complies": True, "use": heard, "time": time}
    if context == row["does_not_comply_when"]:
        return {
            "complies": False,
            "use": row["meaning"],
            "spelled": row["spelled"],
            "content": content,
            "data": data,
            "time": time,
        }
    return {"complies": True, "use": heard, "time": time}


if __name__ == "__main__":
    hit = check(
        "green yard",
        context="organic chemistry",
        content="polymerization",
        data="clean vessel",
        time="2026-09-24T14:09:00-04:00",
    )
    assert hit["complies"] is False
    assert hit["use"] == "Grignard"
    assert hit["spelled"] == "G-R-I-G-N-A-R-D"
    plain = check("menu", "console", "RUN", "one choice", "2026-09-24T14:09:00-04:00")
    assert plain["complies"] is True
    assert plain["use"] == "menu"
    print("ALL_GREEN")
