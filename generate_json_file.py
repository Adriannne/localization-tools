#!/usr/bin/env python
# coding=utf-8

import os
# import schedule
# import time

def print_json():
    # rtv_path = '/home/roaddb/others/shiyu/GM_data/RTV_undistorted'
    rtv_path = '.'

    # for cases in os.listdir(rtv_path):
    #     print('{')
    #     print('     "FileType": "rtvgroup",')
    #     print('     "RtvRosbag": "rtv/one/{}.rtv"'.format(cases,
    #                                                                                                           cases))
    #     print('},')

    for cases in os.listdir(rtv_path):
        if ".rtv" in cases:
            print('{')
            print('     "FileType": "rtvgroup",')
            print('     "RtvRosbag": "rtv/one/{}.rtv"'.format(cases,
                                                              cases))
            print('},')

if __name__ == "__main__":
    print_json()
    # schedule.every().day.at("20:10").do(print_json)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
