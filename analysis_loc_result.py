import os
from draw_memory import draw_compare_memory
from compare_kml import compare_kml
import compare_posreport_kml
import tmp-offline
# import subprocess
import logging
import time


def compare_two_results(branch_result, master_result, output_path='tmp'):
    logging.basicConfig(filename='{}/analysis.log'.format(output_path), level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    threads, areas = 'multi_ekf', 'honda'
    for cases in os.listdir(os.path.join(branch_result, threads, areas)):
        branch_case_dir = os.path.join(branch_result, threads, areas, cases)
        master_case_dir = os.path.join(master_result, threads, areas, cases)
        if os.path.isdir(master_case_dir):
            now = int(round(time.time()*1000))
            now = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
            case_name = '{}_{}_{}_{}_branch1'.format(now, threads, areas, cases)

            # print('draw_compare_memory(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir, case_name, output_path))
            # draw_compare_memory(branch_case_dir, master_case_dir, case_name, output_path)
            #
            # print('compare_kml(\'{}\', \'{}\', \'{}\', \'{}\')'.format(branch_case_dir, master_case_dir, case_name, output_path))
            # compare_kml(branch_case_dir, master_case_dir, case_name, output_path)

            print('compare_kml(\'{}\', \'{}\', \'{}\')'.format(branch_case_dir, case_name, output_path))
            compare_posreport_kml.compare_kml(branch_case_dir, case_name, output_path)

        else:
            print("error! case {} don't exist in master_result!".format(cases))


if __name__ == '__main__':
    master_result = '/home/user/localization/RDB-45658/result_branch'
    branch_result = '/home/user/localization/RDB-46012/result_branch'
    output_path = '/home/user/localization/RDB-46012/output'
    html_name = 'RDB-46012_vehicledb_rdb40_test_result_honda.html'

    os.system('mkdir -p {}'.format(output_path))
    compare_two_results(branch_result, master_result, output_path)
    print('finished')