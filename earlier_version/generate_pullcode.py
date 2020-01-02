#!/usr/bin/env python
# coding=utf-8

def get_repo_dir(repo):
    if repo in ['3rdparty', 'common']:
        repo_dir = repo
    elif repo in ['road_in_vehicle_common_api', 'data-receiver', 'rdb-tools-debug-tools', 'rdb-device-common']:
        repo_dir = 'framework/device/{}'.format(repo)
    elif repo in ['algorithm_common', 'algorithm_vehicle_localization', 'rdb-loc-visualization']:
        repo_dir = 'core/{}'.format(repo)
    else:
        repo_dir = repo
        print('repo is not required for localization!')
        exit(1)
    return repo_dir


def generate_branch_name(repo_branch_name):
    print('{}Branch=$branch'.format(repo_branch_name))


def generate_pullcode_module(repo, repo_branch_name):
    repo_dir = get_repo_dir(repo)

    print(r'''
    echo -e "\n-------------------------checkout {}-------------------------!\n"
    cd "$rootDir"/{} && git fetch --all && git reset --hard && git checkout ${}Branch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout {} failed!\n"
        exit 1
    fi'''.format(repo, repo_dir, repo_branch_name, repo))


def generate_buildcode_module(repo):
    repo_dir = get_repo_dir(repo)

    if repo == 'data-receiver':
        build_command = '-vr'
    elif repo == 'rdb-loc-visualization':
        build_command = '-e'
    else:
        build_command = '-r'

    print(r'''
    echo -e "\n-------------------------build {}-------------------------!\n"
    cd "$rootDir"/{} && ./build.sh {}
    if [ $? -ne 0 ];then
        echo -e "\nbuild {} failed!\n"
        exit 1
    fi'''.format(repo, repo_dir, build_command, repo, repo))


if __name__ == '__main__':
    repo_list = ['3rdparty', 'common', 'rdb-device-common', 'road_in_vehicle_common_api', 'algorithm_common',
                 'data-receiver', 'algorithm_vehicle_localization', 'rdb-loc-visualization']
    repo_branch_name_list = ['thirdparty', 'common', 'rdbDeviceCommon', 'roadInVehicleCommonApi', 'algorithmCommon',
                 'dataReceiver', 'localization', 'visualization']
    for i in range(len(repo_list)):
        repo = repo_list[i]
        repo_branch_name = repo_branch_name_list[i]
        # generate_branch_name(repo_branch_name)
        # generate_pullcode_module(repo, repo_branch_name)
        generate_buildcode_module(repo)