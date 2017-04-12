#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import eyetracker_analytics

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print u"引数を以下のように定義してください"
        print u"1: アイトラッカーで計測した時系列データ"
        exit()
    recording_csv_path_a = str(args[1])
    recording_csv_path_b = str(args[2])
    data_list_a = eyetracker_analytics.get_average_and_variance_per_unit_time(
        csv_file_name = recording_csv_path_a,
        unit_time = 1000,
        trigger_word = 'T'
    )

    data_list_b = eyetracker_analytics.get_average_and_variance_per_unit_time(
        csv_file_name = recording_csv_path_b,
        unit_time = 1000,
        trigger_word = 'T'
    )
    data_list_a = eyetracker_analytics.fft(data_list_a)
    data_list_b = eyetracker_analytics.fft(data_list_b)
    eyetracker_analytics.create_graph([data_list_a, data_list_b])
