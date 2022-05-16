import os

oldFile = open("memo/list.md", "r", encoding="utf-8")
oldText = oldFile.read()
oldFile.close()

markPos = oldText.find("<!--MARKFORBOT-->")

newText = oldText[0:markPos] + "<!--MARKFORBOT-->"

def addLine(name, level, isDir):
    global newText
    pre = "\n"+ "    " * level + "- "
    middle = "`" + name + "`" if isDir else name
    newText += pre + middle

def readFolder(loc, level):
    files = []
    dirs = []
    for file in os.listdir(loc):
        if(file[0] == "."):
            continue
        if os.path.isfile(os.path.join(loc, file)):
            if file.endswith(".md"):
                files.append(file)
        else:
            dirs.append(file)
    for file in files:
        addLine(file, level, False)
    for dir in dirs:
        addLine(dir, level, True)
        readFolder(loc + "/" + dir, level + 1)

readFolder(".", 0)

print(newText)

oldFile = open("memo/list.md", "w", encoding="utf-8")
oldFile.write(newText)
oldFile.close()
