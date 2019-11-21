from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging


def grep_pose_list(kml_file):
    pose = pd.Series()
    with open(kml_file) as f:
        soup = BeautifulSoup(f)
        try:
            for tag in soup.find_all('placemark'):
                key = tag.description.contents[0].split()[1]
                value = tag.coordinates.contents[0]
                pose[key] = value
        except:
            logging.warning("the point.kml is empty!")
    return pose


def count_distance(pose1, pose2):
    pose1 = np.array(str_to_float(pose1))
    pose2 = np.array(str_to_float(pose2))
    distance = np.sqrt(np.sum(np.square(pose1 - pose2)))
    return distance


def str_to_float(pose):
    new_pose = []
    for i in pose.split(','):
        new_pose.append(float(i))
    return new_pose


def check_skipping(frames):
    skipping_frames = []
    for i in range(int(frames[0]), int(frames[-1])):
        if str(i) not in frames:
            skipping_frames.append(i)
    return skipping_frames


def compare_kml(branch_kml, master_kml, case_name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("case: {}".format(case_name))

    branch_pose = grep_pose_list(branch_kml)
    branch_pose['4396'] = '-122.0527503,37.38971697,17.0493'
    logging.info("branch pose list:\n{}".format(branch_pose))

    master_pose = grep_pose_list(master_kml)
    logging.info("master pose list:\n{}".format(master_pose))

    common_index = branch_pose.index.intersection(master_pose.index)

    distance = pd.Series()
    distance05 = pd.Series()
    distance1 = pd.Series()
    for i in common_index:
        dis = count_distance(branch_pose[i], master_pose[i])
        distance[i] = dis
        if dis > 1:
            distance05[i] = dis
        elif dis > 0.5:
            distance1[i] = dis
        else:
            pass
    logging.info("distance list:\n{}".format(distance))
    logging.info("distance that more than 0.5 m:\n{}".format(distance05))
    logging.info("distance that more than 1 m:\n{}".format(distance1))
    logging.info("distance describe:\n{}".format(distance.describe()))

    logging.info("check frame skipping of branch: {}".format(check_skipping(branch_pose.index)))
    logging.info("check frame skipping of master: {}".format(check_skipping(master_pose.index)))

    plt.figure(figsize=(20, 8))
    x = []
    for i in distance.index:
        x.append(int(i))
    plt.plot(x, distance.values, color='#66BAB7')
    plt.title("kml distance of {}".format(case_name))
    plt.xlabel("frame_id")
    plt.ylabel("distance(m)")
    plt.grid(axis='y')

    # plt.show()
    plt.savefig("{}_distance.png".format(case_name))



if __name__ == '__main__':
    # compare_kml(
    #     '/home/user/localization/RDB-45435/result_branch/multi_ekf/honda/2019-09-11_T_23-00-29.443_UTC.img/20191010211751-EKFM-2019-09-11_T_23-00-29.443_UTC.img-LocPosN-S-point.kml',
    #     '/home/user/localization/RDB-45435/result_master/multi_ekf/honda/2019-09-11_T_23-00-29.443_UTC.img/20191011001651-EKFM-2019-09-11_T_23-00-29.443_UTC.img-LocPosN-S-point.kml',
    #     'multi_ekf_honda_2019-09-11_T_23-00-29.443_UTC.img')
    #
    # compare_kml(
    #     '/home/user/localization/RDB-45435/result_branch/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191010212025-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
    #     '/home/user/localization/RDB-45435/result_master/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191011001926-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
    #     'tmp/multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img')

    compare_kml(
        '/home/user/localization/RDB-45529/result_branch0/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191014204932-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
        '/home/user/localization/RDB-45529/result_master/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191014143052-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
        'branch0_multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img')

