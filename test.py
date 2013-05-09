import os
f = os.popen('autojump --completion sae')
result = f.read()
for line in result.split('\n'):
    if len(line) > 0:
        print line[line.find('/'):len(line)]



# print result
