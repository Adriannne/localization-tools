import os
import json

output_dir = "/opt/ygomi/roadDB/work_path/WorkflowManager/RefRegistration/refRegistrationResult"

for files in os.listdir(output_dir):
    files = os.path.join(output_dir, files)
    print(files)
    with open(files, 'r') as f:
        fjson = json.loads(f.read())
        f.close()
    print(fjson)
    print(fjson[u'reference_status'])
    if fjson[u'reference_status']:
        for ref in fjson[u'reference_status']:
            if ref[u'delete'] == u'1':
                print(ref[u'referenceid'])