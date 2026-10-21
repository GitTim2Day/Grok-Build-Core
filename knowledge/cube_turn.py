# Cube turn. One model. GOSUB style.
# U white, D yellow, F green, B blue, L orange, R red.
# A half turn is its own inverse. A bad token stops. It is not skipped.

FACES = "UDFBLR"
COLOR = {"U": "W", "D": "Y", "F": "G", "B": "B", "L": "O", "R": "R"}


def new_cube():
    return {face: [[COLOR[face]] * 3 for _ in range(3)] for face in FACES}


def rotate_cw(face):
    return [list(row) for row in zip(*face[::-1])]


def turn_u(cube):
    cube["U"] = rotate_cw(cube["U"])
    temp = cube["F"][0][:]
    cube["F"][0] = cube["L"][0][:]
    cube["L"][0] = cube["B"][0][:]
    cube["B"][0] = cube["R"][0][:]
    cube["R"][0] = temp


def turn_d(cube):
    cube["D"] = rotate_cw(cube["D"])
    temp = cube["F"][2][:]
    cube["F"][2] = cube["R"][2][:]
    cube["R"][2] = cube["B"][2][:]
    cube["B"][2] = cube["L"][2][:]
    cube["L"][2] = temp


def turn_f(cube):
    # Copy the four edges first. Writing in place reversed them by the fourth turn.
    cube["F"] = rotate_cw(cube["F"])
    u = cube["U"][2][:]
    r = [cube["R"][i][0] for i in range(3)]
    d = cube["D"][0][:]
    l = [cube["L"][i][2] for i in range(3)]
    for i in range(3):
        cube["U"][2][i] = l[2 - i]
        cube["L"][2 - i][2] = d[i]
        cube["D"][0][i] = r[2 - i]
        cube["R"][i][0] = u[2 - i]


def turn_b(cube):
    cube["B"] = rotate_cw(cube["B"])
    temp = cube["U"][0][:]
    for i in range(3):
        cube["U"][0][i] = cube["R"][i][2]
        cube["R"][i][2] = cube["D"][2][2 - i]
        cube["D"][2][2 - i] = cube["L"][2 - i][0]
        cube["L"][2 - i][0] = temp[i]


def turn_l(cube):
    cube["L"] = rotate_cw(cube["L"])
    temp = [cube["U"][i][0] for i in range(3)]
    for i in range(3):
        cube["U"][i][0] = cube["B"][2 - i][2]
        cube["B"][2 - i][2] = cube["D"][i][0]
        cube["D"][i][0] = cube["F"][i][0]
        cube["F"][i][0] = temp[i]


def turn_r(cube):
    cube["R"] = rotate_cw(cube["R"])
    temp = [cube["U"][i][2] for i in range(3)]
    for i in range(3):
        cube["U"][i][2] = cube["F"][i][2]
        cube["F"][i][2] = cube["D"][i][2]
        cube["D"][i][2] = cube["B"][2 - i][0]
        cube["B"][2 - i][0] = temp[i]


TURN = {"U": turn_u, "D": turn_d, "F": turn_f, "B": turn_b, "L": turn_l, "R": turn_r}


def gosub_parse(token):
    # Same IF as the BASIC lines. A 2 wins over a prime. R2' is two turns.
    if not token:
        return None
    face = token[0]
    if face not in FACES:
        return None
    rest = token[1:]
    if rest not in ("", "'", "2", "2'"):
        return None
    if "2" in token:
        return face, 2
    if "'" in token:
        return face, 3
    return face, 1


def gosub_turn(cube, face, times):
    for _ in range(times):
        TURN[face](cube)


def apply_move(cube, token):
    parsed = gosub_parse(token)
    if parsed is None:
        return False
    face, times = parsed
    gosub_turn(cube, face, times)
    return True


def apply_sequence(cube, sequence):
    for token in sequence.split():
        if not apply_move(cube, token):
            return False
    return True


def gosub_inverse(sequence):
    out = []
    for token in reversed(sequence.split()):
        parsed = gosub_parse(token)
        if parsed is None:
            return None
        face, times = parsed
        if times == 2:
            out.append(face + "2")
        elif times == 3:
            out.append(face)
        else:
            out.append(face + "'")
    return " ".join(out)


def is_solved(cube):
    return all(
        cell == cube[face][1][1]
        for face in FACES
        for row in cube[face]
        for cell in row
    )


def counts(cube):
    found = {}
    for face in FACES:
        for row in cube[face]:
            for cell in row:
                found[cell] = found.get(cell, 0) + 1
    return found


def centers(cube):
    return {face: cube[face][1][1] for face in FACES}
