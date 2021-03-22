import heapq as hp
from _collections import deque


f = open("input.txt", "r")
fr = f.readlines()
y = [x.strip().split() for x in fr]
search_type = y[0][0]
wid = int(y[1][0])
hght = int(y[1][1])

inl_yl= (int(y[2][0]), int(y[2][1]), int(y[2][2]))

tgt_yl = (int(y[3][0]), int(y[3][1]), int(y[3][2]))

configuration_num = int(y[4][0])

cfg = {}

for i in range(configuration_num):
    if int(y[5+i][0]) == int(y[5+i][3]):
        continue;
    a, b, c, d = int(y[5+i][0]),int(y[5+i][1]), int(y[5+i][2]), int(y[5+i][3])
    if (a,b,c) not in cfg:
        cfg[(a,b,c)]={d}
    else:
        cfg[(a,b,c)].add(d)

    if (d,b,c) not in cfg:
        cfg[(d, b, c)] = {a}
    else:
        cfg[(d, b, c)].add(a)

def bfs(inl_yl: str, tgt_yl: str, cfg: dict, wid: int, hght: int):
    queue = deque()
    visited = set()

    queue.append(inl_yl)

    total_cost = 0
    step = 0
    map_s = {}
    flg = 0
    nb_lst = [-1, 0, 1]
    map_s[inl_yl] = [inl_yl, 0]

    while queue:
        frt_q = queue.popleft()
        if frt_q == tgt_yl:
            flg = 1
            break
        for i in nb_lst:
            if frt_q[1] + i > wid - 1 or frt_q[1] + i < 0:
                continue
            else:
                for j in nb_lst:
                    if i == j == 0 or frt_q[2] + j > hght - 1 or frt_q[2] + j < 0:
                        continue
                    else:
                        neighbour = (frt_q[0], frt_q[1] + i, frt_q[2] + j)
                        if neighbour not in visited:
                            visited.add(neighbour)
                            queue.append(neighbour)
                            map_s[neighbour] = [frt_q, 1]
        if frt_q in cfg:
            for element in cfg[frt_q]:
                tc_yl = (element, frt_q[1], frt_q[2])
                if tc_yl not in visited:
                    visited.add(tc_yl)
                    queue.append(tc_yl)
                    map_s[tc_yl] = [frt_q, 1]

    fw = open("output.txt", "w")
    if flg == 0:
        fw.write("FAIL")
    else:
        key_yl = tgt_yl
        out_steps = []
        total_cost = 0
        while key_yl != inl_yl:
            total_cost += map_s[key_yl][1]
            out_steps.append([key_yl, map_s[key_yl][1]])
            step += 1
            key_yl = map_s[key_yl][0]

        out_steps.append([inl_yl,0])
        step += 1
        fw.write("%s\n" % total_cost)
        fw.write("%s\n" % step)
        for out in reversed(out_steps):
            for x in out[0]:
                fw.write("%s " % x)
            fw.write("%s\n" % out[1])

def ucs(inl_yl: str, tgt_yl: str, cfg: dict, wid: int, hght: int):
    visited = set()
    dst_queue = [(0, inl_yl, inl_yl, 0, 0)]

    total_cost = 0
    step = 0
    flg = 0

    map_s = {}
    nb_lst = [-1, 0, 1]
    map_s[inl_yl] = [inl_yl, 0]

    while dst_queue:
        queue = hp.heappop(dst_queue)
        frt_q = queue[1]

        if frt_q in visited:
            continue
        else:
            map_s[frt_q] = [queue[2], queue[4]]
            dst_s = queue[3]
            visited.add(frt_q)

        if frt_q == tgt_yl:
            flg = 1
            break

        for i in nb_lst:
            if frt_q[1] + i > wid - 1 or frt_q[1] + i < 0:
                continue
            else:
                for j in nb_lst:
                    if i == j == 0 or frt_q[2] + j > hght - 1 or frt_q[2] + j < 0:
                        continue
                    else:
                        neighbour = (frt_q[0], frt_q[1] + i, frt_q[2] + j)
                        if neighbour not in visited:
                            if i != 0 and j != 0:
                                cost = 14
                            else:
                                cost = 10
                            dst_nb = dst_s + cost
                            hp.heappush(dst_queue, (dst_nb, neighbour, frt_q, dst_nb, cost))

        if frt_q in cfg:
            for element in cfg[frt_q]:
                tc_yl = (element, frt_q[1], frt_q[2])
                if tc_yl not in visited:
                    cost = abs(element - frt_q[0])
                    dst_tc = dst_s + cost
                    hp.heappush(dst_queue, (dst_tc, tc_yl, frt_q, dst_tc, cost))

    fw = open("output.txt", "w")
    if flg == 0:
        fw.write("FAIL")
    else:
        key_yl = tgt_yl
        out_steps = []

        while key_yl != inl_yl:
            out_steps.append([key_yl, map_s[key_yl][1]])
            step += 1
            total_cost += map_s[key_yl][1]
            key_yl = map_s[key_yl][0]

        out_steps.append(map_s[key_yl])
        step += 1

        fw.write("%s\n" % total_cost)
        fw.write("%s\n" % step)
        for out in reversed(out_steps):
            for x in out[0]:
                fw.write("%s " % x)
            fw.write("%s\n" % out[1])

def a_star(inl_yl: str, tgt_yl: str, cfg: dict, wid: int, hght: int):

    visited = set()
    dst_queue = [(0, inl_yl, inl_yl, 0, 0)]

    total_cost = 0
    step = 0
    flg = 0

    map_s = {}
    nb_lst = [-1, 0, 1]
    map_s[inl_yl] = [inl_yl, 0]

    # def dst_h(str1: tuple, str2: tuple):
    #     sum = (str1[0] - str2[0]) ** 2 + 100 * (str1[1] - str2[1]) ** 2 + 100 * (str1[2] - str2[2]) ** 2
    #     h = sum ** (1 / 2.0)
    #     return h

    def dst_h(a: tuple, b: tuple):
        year_distance = abs(a[0] - b[0])
        length = abs(a[1] - b[1])
        height = abs(a[2] - b[2])
        rest = abs(length - height)
        diag_step = min(length, height)
        return year_distance + diag_step * 14 + rest * 10

    while dst_queue:
        queue = hp.heappop(dst_queue)
        frt_q = queue[1]
        if frt_q in visited:
            continue
        else:
            map_s[frt_q] = [queue[2], queue[4]]
            dst_s = queue[3] + queue[4]
            visited.add(frt_q)
        if frt_q == tgt_yl:
            flg = 1
            break
        for i in nb_lst:
            if frt_q[1] + i > wid - 1 or frt_q[1] + i < 0:
                continue
            else:
                for j in nb_lst:
                    if i == j == 0 or frt_q[2] + j > hght - 1 or frt_q[2] + j < 0:
                        continue
                    else:
                        neighbour = (frt_q[0], frt_q[1] + i, frt_q[2] + j)
                        if neighbour not in visited:
                            if i != 0 and j != 0:
                                cost = 14
                            else:
                                cost = 10
                            dst_nb = dst_s + cost + dst_h(neighbour, tgt_yl)
                            hp.heappush(dst_queue, (dst_nb, neighbour, frt_q, dst_s, cost))

        if frt_q in cfg:
            for element in cfg[frt_q]:
                tc_yl = (element, frt_q[1], frt_q[2])
                if tc_yl not in visited:
                    cost = abs(element - frt_q[0])
                    dst_tc = dst_s + cost + dst_h(tc_yl, tgt_yl)
                    hp.heappush(dst_queue, (dst_tc, tc_yl, frt_q, dst_s, cost))

    fw = open("output.txt", "w")
    if flg == 0:
        fw.write("FAIL")
    else:
        key_yl = tgt_yl
        out_steps = []

        while key_yl != inl_yl:
            out_steps.append([key_yl, map_s[key_yl][1]])
            step += 1
            total_cost += map_s[key_yl][1]
            key_yl = map_s[key_yl][0]

        out_steps.append(map_s[key_yl])
        step += 1

        fw.write("%s\n" % total_cost)
        fw.write("%s\n" % step)
        for out in reversed(out_steps):
            for x in out[0]:
                fw.write("%s " % x)
            fw.write("%s\n" % out[1])

if search_type == "BFS":
    bfs(inl_yl, tgt_yl, cfg, wid, hght)
elif search_type == "UCS":
    ucs(inl_yl, tgt_yl, cfg, wid, hght)
elif search_type == "A*":
    a_star(inl_yl, tgt_yl, cfg, wid, hght)
