# delete last line of one file
fileName = 'pull_pullx.xvg'
with open(fileName,'r') as f:
    lines = f.readlines()
newlines = lines[:-1]
with open(fileName,'w') as f:
    f.writelines(newlines)
