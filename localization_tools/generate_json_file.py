#!/usr/bin/env python
# coding=utf-8

'''
{
    "Area": "honda",
    "CameraParameter": "CameraParameter/calibration-Honda_Acura.json",
    "DBPath": "database/vehicleDB_20190911",
    "DBType": "product",
    "LogicDbPath":"database/LogicDB_4.1",
    "Cases":
    [
        {
            "FileType": "rtvgroup",
            "RtvRosbag": "case/2019-09-05_T_18-24-04.387_UTC/2019-09-05_T_18-24-04.387_UTC.img",
            "Frames": 54044
        },
        {
            "FileType": "rtvgroup",
            "RtvRosbag": "case/2019-09-11_T_22-00-29.443_UTC/2019-09-11_T_22-00-29.443_UTC.img"
        }
    ]
}
'''

import os
import json

def print_rtv_group():
    rtv_dir = "/home/roaddb/others/shiyu/for_xianlong/RTV"
    # rtv_dir = "/Users/user/deployment/test_data"

    for root, dirs, files in os.walk(rtv_dir):
        for name in files:
            # if ".rtv" in name or ".img" in name:
            if os.path.splitext(name)[1] == ".rtv" or os.path.splitext(name)[1] == ".img":
                print('{')
                print('     "FileType": "rtvgroup",')
                print('     "RtvRosbag": "{}"'.format(os.path.join(root, name)))
                print('},')


def generate_json_file():
    area = "USi94"
    rtv_dir = "/home/roaddb/others/shiyu/for_xianlong/RTV"
    # rtv_dir = "/Users/user/deployment/test_data"
    camera_config = "/home/roaddb/others/shiyu/for_xianlong/camera_sensing_JXA61701.json"
    db_path = "/home/roaddb/others/shiyu/20191204123028_20191204.46751_GM_USi94_forLoc/vehicleDB"
    db_type = "product"

    # json_path = "/home/roaddb/others/shiyu/case-usi94-productdb.json"
    json_path = 'tmp/tmp.json'

    json_dict = {
        "Area": area,
        "CameraParameter": camera_config,
        "DBPath": db_path,
        "DBType": db_type,
        "Cases":[]
    }
    print(json_dict)
    i = 0

    for root, dirs, files in os.walk(rtv_dir):
        for name in files:
            if os.path.splitext(name)[1] == ".rtv" or os.path.splitext(name)[1] == ".img":
                json_dict["Cases"].append(dict({"FileType": "rtvgroup", "RtvRosbag": os.path.join(root, name)}))
                i = i + 1

    with open(json_path, 'w') as f:
        json.dump(json_dict, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    print_rtv_group()
    generate_json_file()