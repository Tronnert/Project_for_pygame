from settings import DETECT_RAD
import copy
import pprint

def get_path(x1, y1, x2, y2, lab):
    lab = [[e if e == -1 else 0 for e in j] for j in lab]
    # print()
    # print(*["\t".join(map(str, e)) for e in lab], sep="\n")
    # print()
    n, m = len(lab[0]), len(lab)
    lab[y1][x1] = -2
    lab = voln(x1, y1, n, m, lab)
    # print()
    # print(*["\t".join(map(str, e)) for e in lab], sep="\n")
    # print()
    i, j = y2, x2
    k = lab[i][j]
    the_path = []
    while k > 1:
        if i > 0 and lab[i - 1][j] == k - 1:
            i, j = i - 1, j
            the_path.append((j, i))
            k -= 1
        elif j > 0 and lab[i][j - 1] == k - 1:
            i, j = i, j - 1
            the_path.append((j, i))
            k -= 1
        elif i < len(lab) - 1 and lab[i + 1][j] == k - 1:
            i, j = i + 1, j
            the_path.append((j, i))
            k -= 1
        elif j < len(lab[i]) - 1 and lab[i][j + 1] == k - 1:
            i, j = i, j + 1
            the_path.append((j, i))
            k -= 1
    if the_path:
        the_path = [(x2, y2)] + the_path
        the_path.reverse()
        #the_path = [(x1, y1)] + the_path
    return the_path


def voln(x, y, n, m, lab):
    for e in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= x + e[0] < n and 0 <= y + e[1] < m:
            if lab[y + e[1]][x + e[0]] not in [-1, -2] and (lab[y + e[1]][x + e[0]] > lab[y][x] or lab[y + e[1]][x + e[0]] == 0) and lab[y][x] <= DETECT_RAD:
                # print(*["\t".join(map(str, e)) for e in lab], sep="\n")
                # print()
                # print(x + e[0], y + e[1])
                # print()
                lab[y + e[1]][x + e[0]] = lab[y][x] + 1 if lab[y][x] > 0 else 1
                voln(x + e[0], y + e[1], n, m, lab)
    return lab