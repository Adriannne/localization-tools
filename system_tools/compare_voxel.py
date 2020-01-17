import os
import json




if __name__ == '__main__':
    data_path = "/Users/user/deployment/RDB-47497/points_version1"
    voxelInfo_path = os.path.join(data_path, 'voxelInfo.json')
    with open(voxelInfo_path, 'r') as f:
        voxelInfo_json = json.load(f)
        f.close()
    # print(voxelInfo_json)
    # print(voxelInfo_json['semantic']['2']['subSematic'])
    # if '100663296' not in voxelInfo_json['semantic']['2']['subSematic'].keys():
    #     print('100663296')
    # else:
    #     print('true')

    # {'nID': 18, 'points': ['-83.216110514302,42.608678518633,263.55059814453', '-83.216113701004,42.608678569182,263.54748535156', '-83.216116990347,42.608678621929,263.54437255859', '-83.216118674624,42.608678648302,263.5426940918', '-83.216120386793,42.6086786755,263.54104614258', '-83.21612212611,42.608678703522,263.53936767578', '-83.216124166283,42.60868170102,263.5205078125', '-83.21612752145,42.608682076566,263.51544189453', '-83.216129360805,42.60868208783,263.51040649414', '-83.216131188259,42.608682215027,263.50805664062', '-83.216133046207,42.608682345245,263.50570678711', '-83.216136777352,42.608682680956,263.50054931641', '-83.216138649061,42.608682887822,263.49768066406', '-83.216140551636,42.60868309826,263.49478149414', '-83.216142488797,42.608683313093,263.49185180664', '-83.21614444009,42.608687302341,263.46743774414', '-83.216147622329,42.608686618831,263.46850585938', '-83.216148875217,42.608685600159,263.47323608398', '-83.2161556603,42.608680157354,263.50180053711', '-83.216157939969,42.608680279605,263.49911499023'], 'semanticType': 0, 'subSemantic': 83951872}

    for files in os.listdir(data_path):
        if files != 'voxelInfo.json':
            file_path = os.path.join(data_path, files)
            print(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                points_json = json.load(f)
                f.close()
            # print(points_json)
            for refs in points_json:
                if refs['points']:
                    # print(refs['semanticType'], refs['subSemantic'])
                    try:
                        if refs['subSemantic'] == 0:
                            pass
                        elif str(refs['subSemantic']) in voxelInfo_json['semantic'][str(refs['semanticType'])]['subSematic'].keys():
                            pass
                        else:
                            print(refs['nID'], refs['semanticType'], refs['subSemantic'])
                            # print('true')
                    except:
                        # pass

                        print('error! {} did not exist subSematic, the refID is {}'.format(refs['semanticType'], refs['nID']))