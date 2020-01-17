import subprocess

def print_db2kml_log():
    for dbkml in ['bekml', 'vekml', 'lgkml', 'vlgkml']:
        print('************************{}************************'.format(dbkml))
        for i in range(5):
            p = subprocess.Popen('tail /Users/user/deployment/RDB-46641/{}/type{}/log*'.format(dbkml, i), shell=True, stdout=subprocess.PIPE)
            ret = p.stdout.readlines()
            for lines in ret:
                print(lines)
            print('\n')

def print_db2kml_cmd():
    result_path = '/opt/shiyu/RDB-46641'
    vehicledb_path = '/opt/largeScaleTest/backup/20191231105625_4.2.1.3_largescale_Detroit/Process/vehicleDB/'
    logicdb_path = '/opt/largeScaleTest/backup/20191231105625_4.2.1.3_largescale_Detroit/Process/logicDB/'

    for i in range(5):
        print('mkdir -p {}/bekml/type{}'.format(result_path, i))
    for i in range(4):
        print('mkdir -p {}/vekml/type{}'.format(result_path, i))
        print('mkdir -p {}/lgkml/type{}'.format(result_path, i))
        print('mkdir -p {}/vlgkml/type{}'.format(result_path, i))
    for i in range(5):
        print('/opt/ygomi/roadDB/tool/DB2KML RESTBE --domain http://127.0.0.1:8080 --typeOrg {} --oPath {}/bekml/type{} --ol {}/bekml/type{}/log'.format(i,result_path, i,result_path, i))
    for i in range(4):
        print('/opt/ygomi/roadDB/tool/DB2KML FILVHL --idb {}  --typeOrg {} --oPath {}/vekml/type{} --ol {}/vekml/type{}/log'.format(vehicledb_path, i,result_path, i,result_path, i))
    for i in range(4):
        print('/opt/ygomi/roadDB/tool/DB2KML RESTLG --domain http://127.0.0.1:8080 --typeOrg {} --oPath {}/lgkml/type{} --ol {}/lgkml/type{}/log'.format(i,result_path, i,result_path, i))
    for i in range(4):
        print('/opt/ygomi/roadDB/tool/DB2KML FILLG --idb {} --typeOrg {} --oPath {}/vlgkml/type{} --ol {}/vlgkml/type{}/log'.format(logicdb_path, i,result_path, i,result_path, i))

if __name__ == '__main__':
    print_db2kml_cmd()
    # print_db2kml_log()
