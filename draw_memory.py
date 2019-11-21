import matplotlib.pyplot as plt
import logging
import os
import time

def draw_memory(branch_dir, graph_name, output_path="tmp"):
    topfile = os.path.join(branch_dir, 'loctopinfo.log')

    memory = grep_memory(topfile)
    logging.info("memory list: {}".format(memory))

    x = []
    for i in range(len(memory)):
        x.append(i)

    plt.figure(figsize=(20,8))
    plt.plot(x, memory, color='#F05E1C', label='branch')

    plt.legend()
    plt.xlabel("id")
    plt.ylabel("memory(g)")
    plt.title("memory of {}".format(graph_name))
    plt.grid(axis='y')

    # plt.show()
    plt.savefig("{}/{}_memory.png".format(output_path, graph_name))
    plt.close('all')


def draw_compare_memory(branch_dir, master_dir, graph_name, output_path="tmp"):
    topfile_branch = os.path.join(branch_dir, 'loctopinfo.log')
    topfile_master = os.path.join(master_dir, 'loctopinfo.log')

    memory_branch = grep_memory(topfile_branch)
    logging.info("branch memory list: {}".format(memory_branch))
    memory_master = grep_memory(topfile_master)
    logging.info("master memory list: {}".format(memory_master))

    length = min(len(memory_branch), len(memory_master))

    x = []
    for i in range(length):
        x.append(i)

    plt.figure(figsize=(20,8))
    plt.plot(x, memory_branch[:length], color='#F75C2F', label='branch')
    plt.plot(x, memory_master[:length], color='#86C166', label='master')

    plt.legend()
    plt.xlabel("id")
    plt.ylabel("memory(g)")
    plt.title("memory of {}".format(graph_name))
    plt.grid(axis='y')

    # plt.show()
    output_path = os.path.join(output_path, "compare_memory")
    os.system("mkdir -p {}".format(output_path))
    plt.savefig("{}/{}_memory.png".format(output_path, graph_name))


def grep_memory(file_path):
    # grep memory of MultiThreadsLoc.
    memory = []
    with open(file_path) as f:
        for line in f.readlines():
            if "MultiThreadsLoc" in line:
                # print(line)
                res = line.split()[5]
                shr = line.split()[6]
                memory.append(convert_memory(res) - convert_memory(shr))
    f.close()
    # print(memory)
    return memory

    # # grep memory of total used.
    # memory = []
    # with open(file_path) as f:
    #     for line in f.readlines():
    #         if "KiB Mem" in line:
    #             used = line.split()[7]
    #             memory.append(convert_memory(used))
    # f.close()
    # return memory


def convert_memory(value):
    if value[-1] == 'g':
        return float(value[:-1])
    elif value[-1] == 'm':
        return float(value[:-1])/1024
    elif value[-1] == 't':
        return float(value[:-1]) * 1024
    else:
        return float(value)/1048576


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    draw_compare_memory('/home/user/localization/RDB-45658/result_branch/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img',
                        '/home/user/localization/RDB-45529/test4/result_master/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img',
                        '20191029160500_multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img_branch1')


    # branch_result = "/home/user/localization/RDB-45529/test4/result_branch1"
    # master_result = "/home/user/localization/RDB-45529/test4/result_master"
    # output_path = "/home/user/localization/RDB-45529/test4/output/honda1"
    #
    # threads, areas = "multi", "honda"
    # for cases in os.listdir(os.path.join(branch_result, threads, areas)):
    #     branch_case_dir = os.path.join(branch_result, threads, areas, cases)
    #     master_case_dir = os.path.join(master_result, threads, areas, cases)
    #     if os.path.isdir(master_case_dir):
    #         now = int(round(time.time()*1000))
    #         now = time.strftime('%Y%m%d%H%M%S', time.localtime(now / 1000))
    #         case_name = '{}_{}_{}_{}_branch1'.format(now, threads, areas, cases)