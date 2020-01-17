import os
import json
path = "/opt/ygomi/roadDB/work_path/WorkflowManager/RefGenerator/refGeneratorInput"
count = 0
for files in os.listdir(path):
    files = os.path.join(path, files)
    print(files)
    with open(files, 'r') as f:
        json_file = json.load(f)
        f.close()
    print(json_file["ReportData"])
    count = count + len(json_file["ReportData"])

print(count)