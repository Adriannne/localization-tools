branch=master
branch1=feature/RDB-46282-integrate-coordinate-main

3rdpartyBranch=$branch
commonBranch=$branch
rdb-device-commonBranch=$branch
road_in_vehicle_common_apiBranch=$branch
algorithm_commonBranch=$branch
data-receiverBranch=$branch
algorithm_vehicle_localizationBranch=$branch
rdb-loc-visualizationBranch=$branch

new_repo=1
compile_all=1
code_dir=/home/roaddb/others/shiyu/code_branch

#===================================================#
#Do not modify the content below
#===================================================#

if [ ${new_repo} -eq 1 ]; then
    echo "--------------------get new repo--------------------"
    mkdir -p ${code_dir}/core
    mkdir -p ${code_dir}/framework/device
    rm -rf ${code_dir}/*
    cd ${code_dir}

    git clone ssh://git@stash.ygomi.com:7999/as/3rdparty.git ${code_dir}/3rdparty
    git clone ssh://git@stash.ygomi.com:7999/as/common.git ${code_dir}/common

    git clone ssh://git@stash.ygomi.com:7999/as/rdb-device-common.git ${code_dir}/framework/device/rdb-device-common
    git clone ssh://git@stash.ygomi.com:7999/as/road_in_vehicle_common_api.git ${code_dir}/framework/device/road_in_vehicle_common_api
    git clone ssh://git@stash.ygomi.com:7999/as/data-receiver.git ${code_dir}/framework/device/data-receiver
    git clone ssh://git@stash.ygomi.com:7999/as/rdb-tools-debug-tools.git ${code_dir}/framework/device/rdb-tools-debug-tools

    git clone ssh://git@stash.ygomi.com:7999/rdbcore/algorithm_common.git ${code_dir}/core/algorithm_common
    git clone ssh://git@stash.ygomi.com:7999/rdbcore/algorithm_vehicle_localization.git ${code_dir}/core/algorithm_vehicle_localization
    git clone ssh://git@stash.ygomi.com:7999/rdbcore/rdb-loc-visualization.git ${code_dir}/core/rdb-loc-visualization
fi

if [ ${compile_all} -eq 1 ]; then
    cd ${code_dir}
    rootDir=${code_dir}

    echo -e "\n-------------------------checkout 3rdparty-------------------------!\n"
    cd "$rootDir"/3rdparty && git fetch --all && git reset --hard && git checkout $3rdpartyBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout 3rdparty failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout common-------------------------!\n"
    cd "$rootDir"/common && git fetch --all && git reset --hard && git checkout $commonBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout common failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout rdb-device-common-------------------------!\n"
    cd "$rootDir"/framework/device/rdb-device-common && git fetch --all && git reset --hard && git checkout $rdb-device-commonBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout rdb-device-common failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout road_in_vehicle_common_api-------------------------!\n"
    cd "$rootDir"/framework/device/road_in_vehicle_common_api && git fetch --all && git reset --hard && git checkout $road_in_vehicle_common_apiBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout road_in_vehicle_common_api failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout algorithm_common-------------------------!\n"
    cd "$rootDir"/core/algorithm_common && git fetch --all && git reset --hard && git checkout $algorithm_commonBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout algorithm_common failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout data-receiver-------------------------!\n"
    cd "$rootDir"/framework/device/data-receiver && git fetch --all && git reset --hard && git checkout $data-receiverBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout data-receiver failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout algorithm_vehicle_localization-------------------------!\n"
    cd "$rootDir"/core/algorithm_vehicle_localization && git fetch --all && git reset --hard && git checkout $algorithm_vehicle_localizationBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout algorithm_vehicle_localization failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------checkout rdb-loc-visualization-------------------------!\n"
    cd "$rootDir"/core/rdb-loc-visualization && git fetch --all && git reset --hard && git checkout $rdb-loc-visualizationBranch && git pull
    if [ $? -ne 0 ];then
        echo -e "\ncheckout rdb-loc-visualization failed!\n"
        exit 1
    fi
fi