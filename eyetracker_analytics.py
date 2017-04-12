#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import math
import matplotlib.pyplot as plt
import numpy

_MONITOR_SIZE_ROW = 2
_POSITION_DATA_ROW = 5

def _get_norm_from_points(point_a, point_b):
    return math.sqrt(pow(point_a[0] - point_b[0], 2) + pow(point_a[1] - point_b[1], 2))

def _get_average_from_points(points):
    length = len(points)
    ave_x = 0
    ave_y = 0
    for point in points:
        ave_x += point[1]
        ave_y += point[2]
    ave_x /= length
    ave_y /= length
    return [int(ave_x), int(ave_y)]

def get_average_and_variance_per_unit_time(csv_file_name, unit_time = None, trigger_word = None):
    if csv_file_name is None:
        return []
    # unit_time: ms単位
    current_dir_path = os.getcwd()

    row_num = 0
    csv_file = open(current_dir_path + '/' + csv_file_name, 'rb')
    csv_reader = csv.reader(csv_file)
    points = []
    data_list = []
    max_threshold_norm = 0
    for row in csv_reader:
        if row_num == _MONITOR_SIZE_ROW - 1:
            max_threshold_norm = math.sqrt(pow(int(row[1]), 2) + pow(int(row[3]), 2))
        if row_num > _POSITION_DATA_ROW:
            if len(row) < 4:
                continue
            now_point = [float(row[0]), float(row[1]), float(row[2])]
            points.append(now_point)

            if len(points) <= 1:
                continue

            # 最低限指定時間分の時系列データを格納したpointsでなければならない
            if points[-1][0] - points[0][0] < unit_time:
                continue

            # 指定時間を超えた時系列データを格納している場合、
            # 指定時間内に収まるまで古いデータを削除する
            while points[-1][0] - points[0][0] > unit_time:
                del points[0]

            pre_point = None
            ave_norm = 0
            norms = []

            # 平均値
            for point in points:
                if pre_point is None:
                    pre_point = point
                    continue
                norm = _get_norm_from_points([now_point[1], now_point[2]], [pre_point[1], pre_point[2]])
                norms.append(norm)
                ave_norm += norm
                pre_point = point
            ave_norm /= (len(points) - 1)

            # 分散値
            dev_norm = 0
            for norm in norms:
                dev_norm = pow(norm - ave_norm, 2)
            dev_norm /= len(norms)
            if ave_norm < max_threshold_norm:
                data_list.append([row[0], round(ave_norm, 2), round(dev_norm, 2)])
            else:
                data_list.append([row[0], 0, 0])
        row_num += 1
    csv_file.close()
    return data_list

def create_graph(data_lists):
    if len(data_lists) > 5:
        return False
    count = 0
    color_list = ["r", "b", "g", "c", "m"]
    for data_list in data_lists:
        if len(data_list) == 0:
            continue
        plt.plot(numpy.array(data_list[0]), numpy.array(data_list[1]), color_list[count])
        count += 1
    plt.show()

def fft(data_list):
    if len(data_list) == 0:
        return []
    time = []
    averages = []
    divs = []
    for data in data_list:
        time.append(data[0])
        averages.append(data[1])
        divs.append(data[2])
    unit_time = (float(time[-1]) - float(time[0])) / len(time)
    spectrum = numpy.fft.fft(averages)
    half_spectrum = spectrum[0:len(spectrum) / 2 + 1]
    frq_list = numpy.fft.fftfreq(len(averages), unit_time / 1000)
    half_frq = []
    for frq in frq_list:
        if frq >= 0:
            half_frq.append(frq)
    half_frq = half_frq[2:len(half_frq)]
    half_spectrum = half_spectrum[2:len(half_spectrum)]
    return [half_frq, half_spectrum]
