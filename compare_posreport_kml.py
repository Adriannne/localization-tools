# from xml.etree.ElementTree import iterparse
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

def grep_pose_list(kml_file):
    pose = []
    with open(kml_file) as f:
        soup = BeautifulSoup(f)
        for tag in soup.find_all('placemark'):
            all_pose = tag.coordinates.contents[0]
            for i in all_pose.split():
                pose.append(i)
    return pose


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


def compare_kml(case_dir, case_name, output_path='tmp'):
    '''
    compare posreport kml and pose kml of the same case.
    only when report way is image.
    '''
    logging.info("case: {}".format(case_name))

    pose_kml = os.popen('ls {}'.format(os.path.join(case_dir, '*-LocPosN-S_0.kml'))).read().split()[0]
    posreport_kml = os.popen('ls {}'.format(os.path.join(case_dir, '*-LocPosReport_0.kml'))).read().split()[0]

    posreport_list = grep_pose_list(posreport_kml)
    logging.debug("posreport list:\n{}".format(posreport_list))

    pose_list = grep_pose_list(pose_kml)
    logging.debug("pose list:\n{}".format(pose_list))

    distance_list = []
    distance1 = []
    distance05 = []

    if len(pose_list) >= len(posreport_list):
        logging.info("the length of two kml is different. pose kml: {}, posreport kml: {}".format(len(pose_list), len(posreport_list)))

        # gap = len(posreport_list) - len(pose_list)
        # for i in range(len(pose_list)):
        gap = 1
        for i in range(len(posreport_list)):
            distance = count_distance(posreport_list[i], pose_list[i+gap])
            distance_list.append(distance)
            if distance > 1:
                distance1.append((i,distance, posreport_list[i], pose_list[i+gap]))
            elif distance > 0.5:
                distance05.append((i,distance, posreport_list[i], pose_list[i+gap]))
            else:
                pass
        logging.debug("distance list:\n{}".format(distance_list))
        if distance05:
            logging.debug('the distance more than 0.5:')
            for item in distance05:
                logging.debug('index:%d, distance:%f, poseReport:%s, optimizePos:%s'%(item[0], item[1], item[2], item[3]))
        if distance1:
            logging.warning('the distance more than 1:')
            for item in distance1:
                logging.warning('index:%d, distance:%f, poseReport:%s, optimizePos:%s'%(item[0], item[1], item[2], item[3]))


        distance_list = np.array(distance_list)
        logging.info('total frames: {}'.format(len(distance_list)))
        logging.info('max_distance: {}'.format(np.max(distance_list)))
        logging.info('ave_distance: {}'.format(np.average(distance_list)))
        logging.info('variance: {}'.format(np.var(distance_list)))

        plt.figure(figsize=(20, 8))
        plt.plot(distance_list, color='#66BAB7')
        plt.title("kml distance of {}".format(case_name))
        plt.xlabel("id")
        plt.ylabel("distance(m)")
        plt.grid(axis='y')

        # plt.show()
        output_path = os.path.join(output_path, "compare_posreport")
        os.system("mkdir -p {}".format(output_path))
        plt.savefig("{}/{}_prepose.png".format(output_path, case_name))
        plt.close('all')
    else:
        logging.info("the length of two kml is different. pose kml: {}, posreport kml: {}".format(len(pose_list), len(posreport_list)))


if __name__ == '__main__':
    logging.basicConfig(filename='tmp/compare_kml1.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # case_name = '2017-01-01_T_01-39-10.093_UTC.img'
    # case_dir = os.path.join('/home/user/localization/RDB-45360/result_jlr/multi_ekf/JLR', case_name)
    #
    # compare_kml(case_dir, case_name)

    compare_kml('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
    # compare_kml('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_22-30-29.443_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_22-30-29.443_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
    # compare_kml('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-05_T_18-24-04.387_UTC.img', '20191111144607_multi_ekf_honda_2019-09-05_T_18-24-04.387_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
    # compare_kml('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_23-29-46.484_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_23-29-46.484_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
    # compare_kml('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_22-00-29.443_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_22-00-29.443_UTC.img_branch1', '/home/user/localization/RDB-46012/output')

