import os
import glob
import json
import re
import numpy as np
def parseTxt2Json(txtPath,jsonDir):
    '''
    This function is parse the txt containg start time , end time, dialog(txt) to Json format to suit topic segmentation
    Json file: dict{[start time , end time, dialog]}
    Currently, only support less than 60 minute
    :param txtPath:
    :param jsonDir:
    :return:
    '''

    if not os.path.isfile(txtPath):
        print("Error. Please check your the txt file dir and path !!!")
        return
    if not os.path.isdir(jsonDir):
        print("The outPath is not exist. Now create ...")
        os.makedir(jsonDir)
    filename = os.path.basename(txtPath)
    filename = "out" + filename[:-3]+"json"
    outfilePath = os.path.join(jsonDir, filename)
    jsonList = list()
    with open(txtPath, 'r', encoding='utf-8') as f:

            data = f.readlines()
            sentences = ""
            item = dict()
            segSequence = list()
            for line in data:

                listContainTime = re.findall("\s[0-9]+\:[0-9]+\s",line)
                if len(listContainTime)>0:

                    speaker_time = line.strip().split()
                    speaker,time = speaker_time[0],speaker_time[1]
                    m_s = time.split(":")
                    if len(m_s)>2:
                        print("This parsefile only support minute:second format. If u want to"
                              "support more format, please modify this file!!!!")
                        return
                    start_time = round(float(m_s[0])+float(m_s[1])/60,2)
                    end_time = start_time
                    if start_time==0.0:
                        item["starttime"] = start_time
                        item["speaker"] = speaker
                        sentences = ""
                    else:
                        item["endtime"] = end_time
                        if len(segSequence)>0:
                            segSequence.append(sentences)
                            pre_start_time = item["starttime"]
                            pre_end_time = item["endtime"]
                            pre_speaker = item["speaker"]

                            start_time_stamp = np.linspace(pre_start_time,pre_end_time,len(segSequence))
                            last_end_time_stamp = start_time_stamp[1:]
                            for i,(start, end) in enumerate(zip(start_time_stamp, last_end_time_stamp)):
                                item = dict()
                                item["starttime"] = round(start,2)
                                item["endtime"] = round(end,2)
                                item["text"] = segSequence[i]
                                item["speaker"] = pre_speaker
                                jsonList.append(item)
                            item = dict()
                            item["starttime"] = start_time
                            item["speaker"] = speaker
                            sentences = ""
                        else:
                            item["text"] = sentences
                            jsonList.append(item)
                            item = dict()
                            item["starttime"] = start_time
                            item["speaker"] = speaker
                            sentences = ""

                else:
                    if len(sentences)+len(line) > 512:
                        # if the len(sequence), segment the sentence
                        segSequence.append(sentences)
                        sentences = line.strip()
                    else:
                        sentences += line.strip()
                    #print(sentences)
                    #sentences = sentences
                    #sentences = re.split(r'([?？!！。])', line.strip())
                    #sentences.append("")
                    #sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]

    with open(outfilePath, 'w',encoding='utf-8') as w:
        k_str = json.dump(jsonList, w,ensure_ascii=False)
    print("Done. Json file generates success!!!")


if __name__=="__main__":
    parseTxt2Json("./mda-jewt9eimdxf1161b.mp4-文稿-转写结果.txt","./")