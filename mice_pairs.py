#!/usr/bin/env python
# encoding: utf-8

from load_data import data, mice, phases
from datetime import datetime
import csv

# create header for table
rooms = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
FILE_NAME = 'mice_pairs.csv'
header=["Pair of mice:"]
for phase in phases.sections():
    for room in rooms:
        header.append(phase+" in Room: "+str(room))
file = open(FILE_NAME, mode='w')
writer = csv.writer(file, dialect='excel')
writer.writerow(header)


def presences_of_A_and_B(mouse_A, mouse_B, phase):
    data.unmask_data()
    data.mask_data(*phases.gettime(phase))
    start_times_A = data.getstarttimes(mouse_A)
    end_times_A = data.getendtimes(mouse_A)
    room_numbers_A = data.getaddresses(mouse_A)
    start_times_B = data.getstarttimes(mouse_B)
    end_times_B = data.getendtimes(mouse_B)
    room_numbers_B = data.getaddresses(mouse_B)
    presences_list = {1: [[0, 0]], 2: [[0, 0]], 3: [[0, 0]], 4: [[0, 0]]}
    # "presences_list" is dictionary of lists of lists
    # e.g. presences_list = { 1:[[101, 105], [102, 122], [112, 118], ...], 2:[[   e.c.t.
    #       ...where: 1,2... are room numbers; 101 is start o 1st presence; 105 is end of 1st presence;
    #       ...102 is start of 2nd presence; 122 is end of 2nd presence...
    for a in range(0, len(room_numbers_A)):
        room = room_numbers_A[a]
        if room in presences_list:
            presences_list[room].append([start_times_A[a], end_times_A[a]])
        else:
            presences_list[room] = [[start_times_A[a], end_times_A[a]]]
    for b in range(0, len(room_numbers_B)):
        room = room_numbers_B[b]
        if room in presences_list:
            presences_list[room].append([start_times_B[b], end_times_B[b]])
        else:
            presences_list[room] = [[start_times_B[b], end_times_B[b]]]
    for presences in presences_list:
        presences_list[presences].sort()
    return presences_list


def time_together(presences_list):
    time_together = {}
    for room in presences_list:
        # "presences_list" is dictionary of lists of lists
        # e.g. presences_list = { 1:[[101, 105], [102, 122], [112, 118], ...], 2:[[   e.c.t.
        #       ...where: 1,2... are room numbers; 101 is start o 1st presence; 105 is end of 1st presence;
        #       ...102 is start of 2nd presence; 122 is end of 2nd presence...
        start = 0
        end = 1
        time_together[room] = 0
        i = 1
        j = 0
        while i < len(presences_list[room]):
            if presences_list[room][i][start] < presences_list[room][j][end]:
                # presences of mouse_A and mouse_B are overlapping
                if presences_list[room][i][end] < presences_list[room][j][end]:
                    time_together[room] += presences_list[room][i][end] - presences_list[room][i][start]
                    i += 1
                else:
                    time_together[room] += presences_list[room][j][end] - presences_list[room][i][start]
                    j = i
                    i += 1
            else:
                j = i
                i += 1
    return time_together


pair = 0
for i in range(0, len(mice)):
    mouse_A = list(mice)[i]
    for j in range(i+1, len(mice)):
        mouse_B = list(mice)[j]
        pair += 1
        row = ["Pair " + str(pair) + ": " + mouse_A + " and " + mouse_B]
        for phase in phases.sections():
            tt = time_together(presences_of_A_and_B(mouse_A, mouse_B, phase))
            for room in tt:
                tt[room] = datetime.utcfromtimestamp(tt[room]).strftime('%Hh %Mmin %Ss')
                row.append(tt[room])
        writer.writerow(row)
file.close()