branch=master
branch1=feature/RDB-45529-integrate-new-dr-code-to-master-branch

thirdPartyBranch=$branch
globalCommonBranch=$branch
coreCommonBranch=$branch

rdbDeviceCommonBranch=$branch
rdbBaseRuleBranch=$branch
vehicleCommonApiBranch=$branch
dataReceiverBranch=$branch

algoCommonBranch=$branch
algoVehicleLocBranch=$branch1

locVisualBranch=$branch
debugToolsBranch=$branch

new_repo=1 #Use repo to clone the whole code
compile_all=1 #Compile all the code except the algorithm_localization 

taskspace=/home/user/localization
taskspace_code=${taskspace}/code_45529

#===================================================#
#Do not modify the content below
#===================================================#

if ! [ -d ${taskspace} ]; then
    mkdir ${taskspace}
fi
if ! [ -d ${taskspace_code} ]; then
    mkdir ${taskspace_code}
fi

if [ ${new_repo} -eq 1 ]; then
    echo "get new repo"
    rm -rf ${taskspace_code}
    mkdir ${taskspace_code}
    cd ${taskspace_code}
    git clone ssh://git@stash.ygomi.com:7999/as/3rdparty
    git clone ssh://git@stash.ygomi.com:7999/as/common
    mkdir core
    cd ${taskspace_code}/core
    git clone ssh://git@stash.ygomi.com:7999/rdbcore/algorithm_common.git
    git clone ssh://git@stash.ygomi.com:7999/rdbcore/algorithm_vehicle_localization.git
    git clone ssh://git@stash.ygomi.com:7999/rdbcore/rdb-loc-visualization.git
    cd ${taskspace_code}
    mkdir -p ${taskspace_code}/framework/device
    cd ${taskspace_code}/framework/device
    git clone ssh://git@stash.ygomi.com:7999/as/rdb-device-common.git
    git clone ssh://git@stash.ygomi.com:7999/as/rdb-device-base-rules
    git clone ssh://git@stash.ygomi.com:7999/as/road_in_vehicle_common_api
    git clone ssh://git@stash.ygomi.com:7999/as/data-receiver.git
    git clone ssh://git@stash.ygomi.com:7999/as/rdb-tools-debug-tools.git
fi

if [ ${compile_all} -eq 1 ]; then
    cd ${taskspace_code}
    rootDir=${taskspace_code}

    echo -e "\n--------------------checkout 3rd party-------------------------!\n"
    cd "$rootDir"/3rdparty && git fetch --all && git reset --hard &&  git checkout ${thirdPartyBranch} && git pull 
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout 3rd party failed!\n"
       exit 1
    fi
    echo -e "\n--------------------checkout global common-------------------------!\n"
    cd "$rootDir"/common/ && git fetch --all && git reset --hard && git checkout $globalCommonBranch && git pull  
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout global common failed!\n"
       exit 1
    fi
       
    echo -e "\n------------------checkout rdb-device-common------------------!\n"
    cd "$rootDir"/framework/device/rdb-device-common && git fetch --all && git reset --hard &&  git checkout $rdbDeviceCommonBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout rdb-device-common failed!\n"
       exit 1
    fi
    echo -e "\n------------------checkout rdb-device-base-rules------------------!\n"
    cd "$rootDir"/framework/device/data-receiver && git fetch --all && git reset --hard &&  git checkout $rdbBaseRuleBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout rdb-device-base-rules failed!\n"
       exit 1
    fi
    echo -e "\n--------------------checkout road_in_vehicle_common_api-------------------------!\n"
    cd "$rootDir"/framework/device/road_in_vehicle_common_api/ &&  git fetch --all && git reset --hard &&  git checkout $vehicleCommonApiBranch && git pull 
    if [ $? -ne 0 ];then 
       echo -e "\nbuild road_in_vehicle_common_api failed!\n"
       exit 1
    fi
    echo -e "\n------------------checkout data receiver------------------!\n"
    cd "$rootDir"/framework/device/data-receiver && git fetch --all && git reset --hard &&  git checkout $dataReceiverBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout data receiver failed!\n"
       exit 1
    fi
    
    echo -e "\n--------------------checkout algorithm_common-------------------------!\n"
    cd "$rootDir"/core/algorithm_common/ && git fetch --all && git reset --hard &&  git checkout $algoCommonBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout algorithm_common failed!\n"
       exit 1
    fi
    echo -e "\n------------------checkout algorithm_vehicle_localization------------------!\n"
    cd "$rootDir"/core/algorithm_vehicle_localization/ && git fetch --all && git reset --hard &&  git checkout $algoVehicleLocBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout algorithm_vehicle_localization failed!\n"
       exit 1
    fi
    echo -e "\n------------------checkout rdb-loc-visualization------------------!\n"
    cd "$rootDir"/core/rdb-loc-visualization/ && git fetch --all && git reset --hard &&  git checkout $locVisualBranch && git pull
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout rdb-loc-visualization failed!\n"
       exit 1
    fi

    echo -e "\n--------------------checkout rdb-tools-debug-tools-------------------------!\n"
    cd "$rootDir"/framework/device/rdb-tools-debug-tools/ &&  git fetch --all && git reset --hard &&  git checkout $debugToolsBranch && git pull  
    if [ $? -ne 0 ];then 
       echo -e "\ncheckout rdb-tools-debug-tools failed!\n"
       exit 1
    fi
fi
