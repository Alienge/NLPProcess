import os
import glob
import re
def simpleSegText(textPathFile,outPath):
    '''
    Target: This function segment the text using the following rules.
    Rules: We delete ":" rows, split "!",".","?",and to generate the pre-process dataset
    :param textPathFile: input text file path
    :param outPath: output text path dir
    :return: None
    '''
    if not os.path.isfile(textPathFile):
        print("Error. Please check your the file dir and path !!!")
        return
    if not os.path.isdir(outPath):
        print("The outPath is not exist. Now create ...")
        os.makedir(outPath)
    filename = os.path.basename(textPathFile)
    filename = "out"+filename
    outfilePath = os.path.join(outPath,filename)

    with open(textPathFile, 'r', encoding='utf-8') as f:
        with open(outfilePath, 'w', encoding='utf-8') as g:
            data = f.readlines()
            for line in data:
                listContainTime = re.findall("\s[0-9]+\:[0-9]+\s",line)
                if len(listContainTime)>0:
                    print(line)
                    pass
                else:
                    sentences = re.split(r'([?？!！。])', line.strip())
                    #sentences.append("")
                    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
                    for sentence in sentences:
                        g.writelines(sentence)
                        g.write("\n")

if __name__=="__main__":
    textPathFile = "./joined_all.mp4-文稿-转写结果.txt"
    outPath = "./"
    simpleSegText(textPathFile,outPath)









