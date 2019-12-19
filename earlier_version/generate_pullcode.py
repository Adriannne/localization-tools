#!/usr/bin/env python
# coding=utf-8

def generate_branch_name(repo):
    print('{}Branch=$branch'.format(repo))


def generate_pullcode_module(repo):
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

    print(r'''
    echo -e "\n-------------------------checkout {}-------------------------!\n"
    cd "$rootDir"/{} && git fetch --all && git reset --hard && git checkout ${}Branch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout {} failed!\n"
        exit 1
    fi'''.format(repo, repo_dir, repo, repo))


def generate_buildcode_module(repo):
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
    for repo in ['3rdparty', 'common', 'rdb-device-common', 'road_in_vehicle_common_api', 'algorithm_common',
                 'data-receiver', 'algorithm_vehicle_localization', 'rdb-loc-visualization']:
        # generate_branch_name(repo)
        # generate_pullcode_module(repo)
        generate_buildcode_module(repo)