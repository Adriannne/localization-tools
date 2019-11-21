
import re

html_path = '/home/user/localization/RDB-45529/test4/testreport/RDB-45360_test_result1.html'

new_html = ""
with open(html_path, 'r') as f:
    for line in f.readlines():
        if re.search('&lt;', line):
            print("aaaaaaaaaaaaaaa")
            line = re.sub('&lt;', '<', line)
            line = re.sub('&gt;', '>', line)
            line = re.sub('&#x27;', '\"', line)
            new_html += line
        else:
            new_html += line
f.close()

with open(html_path, 'w') as f:
    f.writelines(new_html)
f.close()