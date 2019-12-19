# from xml.etree.ElementTree import iterparse
import os
import time
import logging
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def grep_pose_list(kml_file):
    pose = {}
    keys = []
    with open(kml_file) as f:
        soup = BeautifulSoup(f)
        for tag in soup.find_all('placemark'):
            key = int(tag.description.contents[0].split()[1])
            value = tag.coordinates.contents[0]
            pose[key] = value
            keys.append(key)
    return pose, keys


def count_distance(pose1, pose2):
    pose1 = np.array(get_frame_pose(pose1))
    pose2 = np.array(get_frame_pose(pose2))
    distance = np.sqrt(np.sum(np.square(pose1 - pose2)))
    return distance


def count_distance_xy(pose1, pose2):
    pose1 = np.array(get_frame_pose(pose1)[:-1])
    pose2 = np.array(get_frame_pose(pose2)[:-1])
    distance = np.sqrt(np.sum(np.square(pose1 - pose2)))
    return distance


def get_frame_pose(pose):
    new_pose = []
    for i in pose.split(','):
        new_pose.append(float(i))
    return new_pose


def check_skipping(frames):
    skipping_frames = []
    for i in range(frames[0], frames[-1]):
        if i not in frames:
            skipping_frames.append(i)
    return skipping_frames


def set_graph(plt, output_path, case_name):
    plt.legend()
    plt.xlabel("id")
    plt.ylabel("distance(m)")
    plt.title("kml distance of {}".format(case_name))
    plt.grid(axis='y')

    # plt.show()
    output_path = os.path.join(output_path, "compare_pose_kml")
    os.system("mkdir -p {}".format(output_path))
    plt.savefig("{}/{}_distance.png".format(output_path, case_name))
    plt.close('all')


def draw_pose_kml(branch_dir, master_dir, case_name, output_path='tmp'):
    '''
    graph path: output_path/compare_pose_kml/case_name_distance.png
    '''
    branch_kml = os.popen('ls {}'.format(os.path.join(branch_dir, '*-point.kml'))).read().split()[0]
    master_kml = os.popen('ls {}'.format(os.path.join(master_dir, '*-point.kml'))).read().split()[0]

    logging.info("case: {}".format(case_name))

    branch_pose, branch_frames = grep_pose_list(branch_kml)
    logging.info("branch pose list:\n{}".format(branch_pose))

    master_pose, master_frames = grep_pose_list(master_kml)
    logging.info("master pose list:\n{}".format(master_pose))

    if branch_pose and master_pose:
        logging.info("branch total frames: {}--{}".format(branch_frames[0], branch_frames[-1]))
        logging.info("master total frames: {}--{}".format(master_frames[0], master_frames[-1]))

        logging.info("check frame skipping of branch: {}".format(check_skipping(branch_frames)))
        logging.info("check frame skipping of master: {}".format(check_skipping(master_frames)))

        kml_info = "branch total frames: {}--{}<br />master total frames: {}--{}<br />" \
                   "check frame skipping of branch: {}<br />check frame skipping of master: {}".format(
            branch_frames[0], branch_frames[-1], master_frames[0], master_frames[-1],
            check_skipping(branch_frames), check_skipping(master_frames))

        common_frames = branch_frames
        distance_xy = []
        distance_list = []
        distance1 = {}
        distance05 = {}

        for key in branch_pose.keys():
            if key in master_pose:
                distance_xy.append(count_distance_xy(branch_pose[key], master_pose[key]))
                distance = count_distance(branch_pose[key], master_pose[key])
                distance_list.append(distance)
                if distance > 1:
                    distance1[key] = distance
                elif distance > 0.5:
                    distance05[key] = distance
                else:
                    pass
            else:
                common_frames.remove(key)

        logging.debug("distance list:\n{}".format(distance_list))
        if distance05:
            logging.debug('the distance more than 0.5: {}'.format(distance05))
        if distance1:
            logging.warning('the distance more than 1: {}'.format(distance1))

        distance_list = np.array(distance_list)
        logging.info('total frames: {}'.format(len(distance_list)))
        logging.info('max_distance: {}'.format(np.max(distance_list)))
        logging.info('ave_distance: {}'.format(np.average(distance_list)))
        logging.info('variance: {}'.format(np.var(distance_list)))

        plt.figure(figsize=(20, 8))
        plt.plot(common_frames, distance_list, color='#66BAB7', label='distance_xyz')
        plt.plot(common_frames, distance_xy, color='#FFB11B', label='distance_xy')
        set_graph(plt, output_path, case_name)

        return kml_info

    else:
        logging.warning("the point.kml is empty!")
        return "the point kml is empty!"


if __name__ == '__main__':
    logging.basicConfig(filename='tmp/compare_pose_kml.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    branch_result = "/Users/user/localization/RDB-46282/result_branch"
    master_result = "/Users/user/localization/RDB-46282/result_41"
    output_path = "/Users/user/localization/RDB-46282/tmp"

    threads = "multi_ekf"
    try:
        for areas in os.listdir(os.path.join(branch_result, threads)):
            for cases in os.listdir(os.path.join(branch_result, threads, areas)):
                branch_case_dir = os.path.join(branch_result, threads, areas, cases)
                master_case_dir = os.path.join(master_result, threads, areas, cases)
                if os.path.isdir(branch_case_dir) and os.path.isdir(master_case_dir):
                    now = int(round(time.time() * 1000))
                    now = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
                    case_name = '{}_{}_{}_{}_branch1'.format(now, threads, areas, cases)
                    draw_pose_kml(branch_case_dir, master_case_dir, case_name)
    except:
        logging.warning("open branch case dir failed!")