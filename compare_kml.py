# from xml.etree.ElementTree import iterparse
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

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


def compare_kml(branch_dir, master_dir, case_name, output_path='tmp'):
    branch_kml = os.popen('ls {}'.format(os.path.join(branch_dir, '*-point.kml'))).read().split()[0]
    master_kml = os.popen('ls {}'.format(os.path.join(master_dir, '*-point.kml'))).read().split()[0]

    logging.info("case: {}".format(case_name))

    branch_pose, branch_frames = grep_pose_list(branch_kml)
    # branch_pose[4396] = '-122.0527503,37.38971697,17.0493'
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
        # plt.plot(common_frames, distance_list, color='#66BAB7', label='distance_xyz')
        plt.plot(common_frames, distance_xy, color='#FFB11B', label='distance_xy')
        plt.title("kml distance of {}".format(case_name))

        plt.legend()
        plt.xlabel("id")
        plt.ylabel("distance(m)")
        plt.grid(axis='y')

        # plt.show()
        output_path = os.path.join(output_path, "compare_kml")
        os.system("mkdir -p {}".format(output_path))
        plt.savefig("{}/{}_distance.png".format(output_path, case_name))
        plt.close('all')

        return kml_info

    else:
        logging.warning("the point.kml is empty!")
        return "the point kml is empty!"


if __name__ == '__main__':
    logging.basicConfig(filename='tmp/compare_kml.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # pass
    # branch_kml = '/home/user/localization/RDB-45435/result_branch/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191010212025-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml'
    # master_kml = '/home/user/localization/RDB-45435/result_master/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191011001926-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml'
    # case_name = 'multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img'
    # compare_kml(branch_kml, master_kml, case_name)

    # compare_kml(
    #     '/home/user/localization/RDB-45529/test1/result_branch1/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191014234833-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
    #     '/home/user/localization/RDB-45529/test1/result_master/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img/20191014143052-EKFM-2019-09-11_T_23-59-46.484_UTC.img-LocPosN-S-point.kml',
    #     'branch1_multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img')

    # compare_kml('/home/user/localization/RDB-45658/change_undistort_config/0',
    #             '/home/user/localization/RDB-45658/change_undistort_config/1',
    #             'compare_kml_of_changed_undistort_config_2019-09-05_T_18-24-04.387_UTC.img')

    # compare_kml(
    #     '/home/user/localization/RDB-45664/result_release_withsingle/multi_ekf/GM/2019-08-20_T_22-56-20.940_UTC.img',
    #     '/home/user/localization/RDB-45664/result_release_vehicledb0919/multi_ekf/GM/2019-08-20_T_22-56-20.940_UTC.img',
    #     '20191030105023_multi_ekf_GM_2019-08-20_T_22-56-20.940_UTC.img_branch1',
    #     '/home/user/localization/RDB-45664/output')

    compare_kml(
        '/home/user/localization/RDB-46015/master_result/multi_ekf/JLR_cam65_shortSection/2019-02-16_T_14-34-41.165_GMT.rtv',
        '/home/user/localization/RDB-46015/master_result/multi_ekf/JLR_cam65_shortSection/2019-02-16_T_14-34-41.165_GMT.rtv',
        '20191114100114_multi_ekf_JLR_cam65_shortSection_2019-02-16_T_14-34-41.165_GMT.rtv_branch1',
        '/home/user/localization/RDB-46015/output')