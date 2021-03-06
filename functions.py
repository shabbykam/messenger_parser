import datetime
import os
import random
import pyhtml as ph
import re
import xml
import functions
from os.path import isfile, join
import xmltodict
import json
import ftfy
from datetime import datetime
import unidecode
import time
import logging

FOLDER_GEN_HTML = "generated_html"
FOLDER_TXTS_FROM_JSON_OR_XML = "txtsFromJsonOrXml"
FOLDER_ABC = "ABC_NAME_TO_DATE"
FOLDER_PER_NAME_STATS = "perNameStats"
FOLDER_JSON = "c:\\Users\\abasc\\Documents\\_csaba\\my_fb_data_20200823\\messages\\inbox"   # dell
FOLDER_BIG_FILES = "BIG_HTML_FILES"
FOLDER_LOG = "log"
FILE_DONEFILE = "doneFile.txt"
XMLS_TO_TXT = "_txt_from_XML"
initFoldersList = [FOLDER_JSON, FOLDER_GEN_HTML, FOLDER_ABC, FOLDER_LOG, FOLDER_TXTS_FROM_JSON_OR_XML]
STRING_VIDA_CSABA = 'Vida Csaba'
doneFiles = []
VISITED_JSON = "visited.json"
ABOUT_YOU = "about_you"
dirsToProcessInJsonFolder = os.listdir(FOLDER_JSON)

#==================== <DONT TOUCH - ITS STABLE> =========================================

# Generating the folders that are needed for further processings
def initFolders(initFoldersList):
    for foldername in initFoldersList:
        if not os.path.exists(foldername):
            os.mkdir(foldername)
            logging.info("Creating folder ( initFolder()) : " + foldername)
        else:
            logging.info("Creating folder ( initFolder()) : " + foldername + " not neccessary. It already exists.")

#==================== </DONT TOUCH - ITS STABLE - THE END> =========================================

def showFilesInFolders(pathToGenerated):
    count = 0
    dayToCountDict = {}
    for x in os.walk(pathToGenerated):
        #print(x[0])
        if not(x[1]):
            day = x[0]
            count += 1
            sumOfAllLines = 0
            for chat in x[2]:
                #print(chat)
                #print(sumOfAllLines)
                try:
                    numOfLines = int((chat.split("_")[1]).split(".")[0])
                    sumOfAllLines = numOfLines + sumOfAllLines
                except IndexError:
                    print("Oops!  That was no valid number.  Try again..." + chat)

                #print(numOfLines)


            #print("sum of all: " + str(sumOfAllLines))
            if len(day.split("\\")) == 4:
                month = day.split("\\")[2]
                thatDay = day.split("\\")[3]
                date = day.split("\\")[1] + "-" + month + "-" + thatDay
                dayToCountDict[date] = sumOfAllLines
            #print(day)
            #print(str(x))
            #print(len(x[2]))
            #print(count)
    #print(count)
    dictionary_items = dayToCountDict.items()
    sorted_items = sorted(dictionary_items)
    #print(sorted_items)
    #print(type(sorted_items))

    return dayToCountDict

def analyzeByYearAll(dayToCount):
    #print(dayToCount)
    yearToCount = {}
    for date, val in dayToCount.items():
        #print(date + " " + str(val))
        year = date.split("-")[0]
        if year in yearToCount:
            yearToCount[year] = yearToCount[year] + val
        else:
            yearToCount[year] = val
    print(yearToCount)

def getListOfAllPersonsInDayFiles(pathToGenerated):
    persons = []
    for x in os.walk(pathToGenerated):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            persons.append(name)
    return sorted(list(set(persons)))

def getLabels(labels):
    if labels:
        return labels
    else:
        return """'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July'"""

# TOPLIST - MOST CHATTED WITHIN A DAY - who is the one you talked the most within a day
def getTopMessagesWithinDAy():
    max = 0
    person = ""
    day = ""
    for x in os.walk(FOLDER_GEN_HTML):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            count = int((file.split("_")[1]).split(".")[0])
            if count > max:
                max = count
                day = x[0]
                person = name
    print("The person you chatted the most within a day was " + person + " , and you changed " + str(max) + " messages on " + str(day))

def getListOfAllPersonsInDayFilesWithLimit(limit):
    persons = []
    for x in os.walk(FOLDER_GEN_HTML):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            count = int((file.split("_")[1]).split(".")[0])
            if count > limit:
                persons.append(name)
                print(x)
                print(file)
    return sorted(list(set(persons)))



def analyzeByMonthsAll(dayToCount):
    #print(dayToCount)
    yearMonthToCount = {}
    for date, val in dayToCount.items():
        #print(date + " " + str(val))
        year = date.split("-")[0]
        month = date.split("-")[1]
        yearMonth = year + "-" + month
        if yearMonth in yearMonthToCount:
            yearMonthToCount[yearMonth] = yearMonthToCount[yearMonth] + val
        else:
            yearMonthToCount[yearMonth] = val
    print(yearMonthToCount)
    return yearMonthToCount

def createTxtFilesFromFolders(dirsToProcessInJsonFolder):
    for folderPath in dirsToProcessInJsonFolder:
        print(folderPath)
        filesOrFoldersInFolder = os.listdir(folderPath)
        print(filesOrFoldersInFolder)
        exit()
        jsonFiles = list(filter(lambda x: (str(x).endswith('.json')), filesOrFoldersInFolder))
        xmlFiles = list(filter(lambda x: (str(x).endswith('.xml')), filesOrFoldersInFolder))
        logging.info("List of json files " + str(jsonFiles))
        logging.info("List of xml files " + str(xmlFiles))
        print("List of json files " + str(jsonFiles))
        print("List of xml files " + str(xmlFiles))
        counter = 0
        if jsonFiles != []:
            logging.info("Json files : " + str(jsonFiles))
            for file in jsonFiles:
                file = folderPath + '/' + file
                # volt: counter = counter +
                functions.processJson(file)
        pass

def correctFolderDates():
    count = 0
    datesArray = os.walk(FOLDER_GEN_HTML)
    for d in datesArray:
        if (not (d[2])):  # correcting the one numbered months
            if len(d[0].split("\\")) == 2:
                months = d[1]
                for month in months:
                    recentPath = os.getcwd()
                    if len(month) == 1:
                        oldPath = d[0]
                        os.chdir(oldPath)
                        os.rename(month, "0" + month)
                        os.chdir(recentPath)

            if len(d[0].split("\\")) == 3:
                days = d[1]
                for day in days:
                    recentPath = os.getcwd()
                    if len(day) == 1:
                        oldPath = d[0]
                        os.chdir(oldPath)
                        os.rename(day, "0" + day)
                        os.chdir(recentPath)

        # days
    for folder in os.walk(FOLDER_GEN_HTML):
        if ((not (folder[1])) or (not (folder[2]))):
            if len(folder[0].split("\\")) == 2:
                #print(folder)
                oldPath = folder[0]
                os.chdir(oldPath)
                months = folder[1]
                #print(months)


# deletes all the empty folders, that have been generated
def deleteEmptyFolders(pathToGenerated):
    yearDirs = os.listdir(pathToGenerated)
    yearDirs = os.walk(pathToGenerated)
    for x in os.walk(pathToGenerated):
        if not(x[1])  and not(x[2]):
            print(str(x))
            #os.remove(x[0])
            #print(x[0] + " removed.")

def processJsonToTxt(dirsToProcessInJsonFolder):
    for folder in dirsToProcessInJsonFolder:
        logging.info("Start processing folder \"" + folder + "\"")
        print("Start processing folder \"" + folder + "\"")
        # exit()
        folderPath = FOLDER_JSON + '/' + folder
        logging.info("Relative path to folder " + folderPath)
        filesInFolder = os.listdir(folderPath)
        logging.info("Files in: " + folderPath)
        print("Files in: " + folderPath)
        logging.info(filesInFolder)
        # print("filesInFolder: ")
        # print(filesInFolder)
        countOfProcessedTxt = functions.createTxtFromJsonOrXml(folderPath)
        # print("szar2")
        logging.info("Number of files processed to TXT file : " + str(countOfProcessedTxt))
        # exit()


def processAllData(all_data):
    counter = 0
    dirs = os.walk(all_data)
    for folder in dirs:
        counter += 1
        if counter > 60:
            exit()
        else:
            #print(counter)
            #print(folder)

            if (folder[1] == []) & (folder[2] == []):
                print("Should be deleted: " + str(folder))
            if folder[0] == all_data + "\\"  + ABOUT_YOU:
                print("Start aboutyou")
                processAboutYou(folder[0])
                exit()
    exit()

def processVisited(pathToFile):
    #print(pathToFile + " szar")
    menuElements = []
    with open(pathToFile) as json_file:
        data = json.load(json_file)
        for key in data["visited_things"]:
            name = functions.encodeText(str(key['name']))
            print(name)
            print(str(key))
            menuElements.append((name, name))

    def f_links(ctx):
        for title, page in menuElements:
            yield ph.li(ph.a(href=page)(title))
    t = ph.html(
        ph.head(
            ph.title('visited_things'),
            ph.script(src="http://path.to/script.js")
        ),
        ph.body(
            ph.header(
                ph.img(src='/path/to/logo.png'),
                ph.nav(
                    ph.ul(f_links(menuElements))
                )
            ),
            ph.div(
                lambda ctx: "Hello %s" % ctx.get('user', 'Guest'),
                'Content here'
            ),
            ph.footer(
                ph.hr,
                'Copyright 2013'
            )
        )
    )
    resultFile = FOLDER_GEN_HTML + "\\" + "sample.html"
    with open(resultFile, "w", encoding="utf-8") as newFile:
        newFile.write(t.render(user='Csaba'))
    newFile.close()

    print(str(menuElements))

    exit()

def processAboutYou(path):
    print(path + " ===== ")
    content = os.walk(path)
    for files in content:
        for file in files[2]:
            if file == VISITED_JSON :
                pathToFile = path + "\\" + VISITED_JSON
                processVisited(pathToFile)
                print(file)



def fromFunctions(szar):
    print(szar)

def getDateWithTime(timestamp) -> str:
    #print(timestamp)
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    #print(dt_obj)
    return "20" + str(dt_obj)

def processJson(file):
    person = ""
    first = ""
    last = ""
    print("=========================")
    abcDaysFile = []
    #print(file)
    #print(doneFiles)
    if file in doneFiles:
        print(file + " already has been processed.")
        logging.info(file + " already has been processed.")
        return "", "", "", 0, 0, True, doneFiles
    with open(file) as json_file:

        # print(file.split('\\')[-1])
        data = json.load(json_file)
        for p in data['participants']:
            p = encodeText(p['name'])
            if p == STRING_VIDA_CSABA:
                continue
            else:
                person = p
        countRecentFile = len(data['messages'])
        lastIndex = len(data['messages']) - 1
        firstMessageTime = functions.getDateWithTime(data['messages'][lastIndex]["timestamp_ms"])
        dateFrom = firstMessageTime.split()[0]
        # print("firstm " + firstMessageTime)
        lastMessageTime = getDateWithTime(data['messages'][0]["timestamp_ms"])
        dateTo = lastMessageTime.split()[0]
        # print("lastm " + lastMessageTime)
        if first == "":
            first = firstMessageTime
        else:
            if first > firstMessageTime:
                first = firstMessageTime
        if last == "":
            last = lastMessageTime
        else:
            # print("last "  + last)
            # print("lastMessage "  + lastMessageTime)
            if last < lastMessageTime:
                last = lastMessageTime
        htmlFileName = getHtmlFilename1(person, countRecentFile, dateFrom, dateTo, 'txt')
        #rint(htmlFileName)
        ret = createClearJson(file, htmlFileName, abcDaysFile)

        doneFiles.append(file)

def createTxtFromJsonOrXml(folderPath):

    filesOrFoldersInFolder = os.listdir(folderPath)
    jsonFiles = list(filter(lambda x: (str(x).endswith('.json')), filesOrFoldersInFolder))
    xmlFiles = list(filter(lambda x: (str(x).endswith('.xml')), filesOrFoldersInFolder))
    logging.info("List of json files "  + str(jsonFiles))
    logging.info("List of xml files "  + str(xmlFiles))
    print("List of json files "  + str(jsonFiles))
    print("List of xml files "  + str(xmlFiles))
    counter = 0
    if jsonFiles != []:
        logging.info("Json files : "  + str(jsonFiles))
        for file in jsonFiles:
            file = folderPath + '/' + file
            # volt: counter = counter +
            processJson(file)
    if xmlFiles != []:
        logging.info("Xml files : "  + str(jsonFiles))
        for file in xmlFiles:
            file = folderPath + '/' + file
            counter += processXml(file)
    return counter
    #start of xml


    setDoneFiles(doneFiles)
    #end of xml

    # if abcDaysFile:
    #     print(abcDaysFile)
    #
    # createAbcFile(abcDaysFile, person)

def getHtmlFileNameFromData(data):
    names = data['participants']
    if len(names) == 1:
        print("CSAK EGY")
        return 0
    person1 = names[0]["name"]
    person1 = encodeText(person1)
    person2 = names[1]["name"]
    person2 = encodeText(person2)
    messages = data['messages']
    firstMess = messages[len(messages) - 1]['timestamp_ms']
    lastMess = messages[0]['timestamp_ms']
    mess_count = len(messages)
    dateFrom = getDateWithTime(firstMess).split()[0]
    dateTo = getDateWithTime(lastMess).split()[0]
    htmlFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "html")
    sumFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "txt")
    return htmlFilename

def encodeText(text):
    return ftfy.ftfy(text)
    #return text.encode('cp1252').decode('utf8')

def getHtmlFilename1(name, count, dateFrom, dateTo, format):
    return getHtmlFilename(name, STRING_VIDA_CSABA, count, dateFrom, dateTo, format)

def getHtmlFilename(name1, name2, count, dateFrom, dateTo, format):
    name = ""
    now = getDateOfNow()
    if name1 == STRING_VIDA_CSABA:
        name = name2
    else:
        name = name1
    if name == "":
        name = "unknown"
    if count % 1000 == 0:
        c = str(int(count / 1000)) + 'k'
    else:
        c = str(count)
    name = unidecode.unidecode(encodeText(name))
    name = name.replace(" ", "")
    htmlFilename = "[" + dateFrom + "---" + dateTo + "]_" +str(c) + "__" + name + "." + format
    return htmlFilename

def getDateOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[0]
    return result

def getTimeOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[1]
    result = (result.split(".")[0]).replace(":", "")
    return result

def getProperDateFormat(filesPerDay):
    month = filesPerDay.split("\\")[2]
    day = filesPerDay.split("\\")[3]
    result = filesPerDay.split("\\")[1] + "-" + month + "-" + day
    return result


def buildPersonFiles(listOfAllThePersons):
    for person in listOfAllThePersons:
        print("Building PERSON(DATE:COUNT) file for person : " + person)
        buildOnePersonFile(person)

def buildOnePersonFile(person):
    dayToCountList = []
    print("person is " + person)
    sum = 0
    for filesPerDay in os.walk(FOLDER_GEN_HTML):
        files = filesPerDay[2]
        for file in files:
            name = file.split("_")[0]
            if (name == person):
                thatDate = getProperDateFormat(filesPerDay[0])
                count = (file.split("_")[1]).split(".")[0]
                sum = sum + int(count)
                recentDayToCountDict = {}
                recentDayToCountDict[thatDate] =  count
                dayToCountList.append(recentDayToCountDict)
    fileNameWithPath = FOLDER_PER_NAME_STATS + "\\" + person + "_" + str(sum) + ".stat"
    print(dayToCountList)
    with open(fileNameWithPath, "w", encoding="utf-8") as newFile:
        for record in dayToCountList:
            key = list(record.keys())[0]
            newFile.write(key + " : " + record[key])
            newFile.write("\n")
    newFile.close()

def buildOnePersonFile(person):
    dayToCountList = []
    print("person is " + person)
    sum = 0
    for filesPerDay in os.walk(FOLDER_GEN_HTML):
        files = filesPerDay[2]
        for file in files:
            name = file.split("_")[0]
            if (name == person):
                thatDate = getProperDateFormat(filesPerDay[0])
                count = (file.split("_")[1]).split(".")[0]
                sum = sum + int(count)
                recentDayToCountDict = {}
                recentDayToCountDict[thatDate] =  count
                dayToCountList.append(recentDayToCountDict)
    fileNameWithPath = FOLDER_PER_NAME_STATS + "\\" + person + "_" + str(sum) + ".stat"
    print(dayToCountList)
    with open(fileNameWithPath, "w", encoding="utf-8") as newFile:
        for record in dayToCountList:
            key = list(record.keys())[0]
            newFile.write(key + " : " + record[key])
            newFile.write("\n")
    newFile.close()

def createClearJson(fileName, htmlFileName, abcDaysFile):
    print("Processing " + fileName)
    htmlFileNameWithPath = FOLDER_TXTS_FROM_JSON_OR_XML + "/" + htmlFileName
    #print(htmlFileNameWithPath)
    if os.path.exists(htmlFileNameWithPath):
        print("Already exists, returning. File:  " + htmlFileName)
        return []
    #print(htmlFileNameWithPath)
    jsonData = {}
    with open(fileName) as f:
        data = json.load(f)
        messages = data['messages']
        if (os.path.exists(htmlFileName)):
            return []
        counter = 0
        for message in messages:
            name = encodeText(message['sender_name'])
            if "content" in message:
                msg = encodeText(message['content'])
                #print(msg)
                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
                date = getDateWithTime(message['timestamp_ms'])
                if date in abcDaysFile:
                    pass
                else:
                    abcDaysFile.append(date)
                #print(date)
                jsonData[date] = name + ": "+ msg
    res = dict(reversed(list(jsonData.items())))
    #print(res)
    with open(htmlFileNameWithPath, "w", encoding="utf-8") as newFile:
        for i in res.keys():
            newFile.write(i + " " + res.get(i))
            newFile.write('\n')
    newFile.close()
    print("Generating file " + htmlFileName)
    return abcDaysFile

def getMsgLine(dateAndTime, name, msg):
    result = ""
    if isinstance(msg, str):
        result = dateAndTime + " " + "[" + name + "]" + " : " +  msg
    return result

def processXml(file):
    person = (file.split("\\")[-1]).split(".")[0]
    person = person.split(" ")[0]
    print("Xml processing : " + file)
    print("For person " + person)
    doneFiles = getDoneFiles()
    #print(doneFiles)
    exit()
    abcDaysFile = []
    countMessages = 0
    if file in doneFiles:
        logging.info(file + " already has been processed.")
        return 0
    with open(file, 'r', encoding="utf-8") as myfile:
        try:
            obj = xmltodict.parse(myfile.read())
        except xml.parsers.expat.ExpatError as err:
            print("Expaterror ".format(err))
            return 0
        except ValueError:
            print("Could not convert data to an integer.")
            return 0
        except:
            print("Unexpected error:")
            return 0
    #print(json.dumps(obj["Log"]["Message"]))
    if "Log" in obj:
        msgList = obj["Log"]["Message"]
    else:
        #print(obj)
        return 0
    countRecentFile = len(msgList)
    # print(countRecentFile)
    # print(type(msgList))
    # print(msgList)
    if 0 in msgList:
        dateFrom = msgList[0]['@Date'].replace(".","")
        dateTo = msgList[-1]['@Date'].replace(".","")
    else:
        return 0
    counter = 0
    htmlFileName = getHtmlFilename1(person, countRecentFile, dateFrom, dateTo, 'txt')
    htmlFileNameWithPath = os.path.dirname(file) + "\\" + htmlFileName
    logging.info("Processing " + htmlFileName)
    #print(htmlFileNameWithPath)
    #print(doneFiles)


    with open(htmlFileNameWithPath, "w", encoding="utf-8") as newFile:
        for msg in msgList:
            counter += 1
            dateAndTime = msg["@Date"] + " " + msg["@Time"]
            dateAndTime = (str(dateAndTime)).replace(".", "-")
            dateAndTime = dateAndTime[:10] + dateAndTime[11:]
            name = msg['From']['User']['@FriendlyName']
            if len(name) > 20 :
                name = name[0:20]
            if "#text" in msg['Text']:
                text = msg['Text']['#text']
            else:
                text = msg['Text']
            newFile.write(getMsgLine(dateAndTime, name, text))
            newFile.write('\n')
    newFile.close()

    doneFiles.append(htmlFileName)
    #print(countRecentFile)
    print("============")
    return 1
    #ret = createClearJson(file, htmlFileName, "")
    #doneFiles.append(file)

def setDoneFiles(doneFiles):
    return
    if os.path.exists(FILE_DONEFILE):
        with open(FILE_DONEFILE, 'w', encoding="utf-8") as reader:
            for line in doneFiles:
                reader.write(line)
                reader.write("\n")
        reader.close()
    return

def getPersonnameFromTxtFile(txtFile):
    personName = txtFile.split("__")[1].split(".")[0]
    limit = len(personName)-0
    personName = personName[:limit]
    if personName == "":
        personName = "unknown"
    #print(personName)
    return personName

def createDatePath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        if int(month) < 10:
            month = "0" + month
        day = str(int(recentDate.split("-")[2]))
        if int(day) < 10:
            day = "0" + day
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\' + day + '\\'
        return result
    else:
        return False

def createYearPath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        result = FOLDER_GEN_HTML + '\\' + year
        return result
    else:
        return False

def createMonthPath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        if int(month) < 10:
            month = "0" + month
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\'
        return result
    else:
        return False

def createDayPath(recentDate):
    #print(recentDate)
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        if int(month) < 10:
            month = "0" + month
        day = str(int(recentDate.split("-")[2]))
        if int(day) < 10:
            day = "0" + day
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\' + day
        return result
    else:
        return False


def createDailyFileFromNameWithCount(person, countInString):
    #print(len(person))
    if person == "":
        return ""
    fileName = person + "_" + str(countInString) + ".day"
    fileName = unidecode.unidecode(encodeText(fileName))
    fileName = fileName.replace(" ", "")
    return fileName


def processTxtToDayFiles(folderPath):
    txtFilesList = os.listdir(folderPath)
    txtFiles = list(filter(lambda x: (str(x).endswith('.txt')), txtFilesList))
    counter = 0

    for actualTxt in txtFiles:

        print(actualTxt)
        file = folderPath + '\\' + actualTxt
        person = getPersonnameFromTxtFile(actualTxt)
        if os.path.exists(file):
            print(file + " exists")
        linesToDayFile = []
        tempRecentDate = ""
        fileCounter = 0
        messageCounter = 0
        #print(file)
        with open(file, 'r', encoding="utf-8") as reader:
            logging.info(" ")
            logging.info(str(counter) + ".th file : " + file)
            counter += 1
            datedPathAndFilename =""
            linesToDayFile = []
            for line in reader.readlines():
                # todo here 2021 05 07
                if re.match(r'^\d{4}-\d?\d-\d?\d (?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]', line):
                    messageCounter += 1
                    recentDate = line.split()[0]
                    if tempRecentDate == "":
                        tempRecentDate = recentDate
                    #print(tempRecentDate)

                    yearPath = createYearPath(tempRecentDate)

                    #print(yearPath)
                    if not os.path.exists(yearPath):
                        os.mkdir(yearPath)
                        #logging.info("Creating " + yearPath)
                    monthPath = createMonthPath(tempRecentDate)
                    #print(monthPath)
                    if os.path.exists(monthPath):
                        pass
                    else:
                        os.mkdir(monthPath)
                        #logging.info("Creating " + monthPath)
                    dayPath = createDayPath(tempRecentDate)
                    #print(dayPath)
                    if os.path.exists(dayPath):
                        pass
                    else:
                        os.mkdir(dayPath)
                        #logging.info("Creating " + dayPath)
                    datedPath = createDatePath(tempRecentDate)
                    fileNameWithCount = createDailyFileFromNameWithCount(person, messageCounter)
                    datedPathAndFilename = datedPath + fileNameWithCount
                    #print(datedPathAndFilename)
                    #exit()
                    if (recentDate != tempRecentDate) & (tempRecentDate != ""):
                        messageCounter = 0
                        #print(linesToDayFile)
                        #print(datedPathAndFilename)
                        #print(recentDate)
                        if not os.path.exists(datedPathAndFilename):
                            with open(datedPathAndFilename, "w", encoding="utf-8") as newFile:
                                newFile.write("Message count:" + str(messageCounter))
                                newFile.write("\n")
                                for i in linesToDayFile:
                                    newFile.write(i)
                            newFile.close()
                            logging.info(str(fileCounter) + "Creating file : " + datedPathAndFilename)
                            fileCounter += 1
                        linesToDayFile = []

                    tempRecentDate = recentDate
                    linesToDayFile.append(line)
                else:
                    linesToDayFile.append(line)
                    #print(linesToDayFile)

            #print(datedPathAndFilename)
            #print(linesToDayFile)
            if linesToDayFile:
                if not os.path.exists(datedPathAndFilename):
                    with open(datedPathAndFilename, "w", encoding="utf-8") as newFile:
                        newFile.write("Message count:" + str(len(linesToDayFile)))
                        newFile.write("\n")
                        for i in linesToDayFile:
                            newFile.write(i)
                    newFile.close()




    logging.info(str(counter) + " files processed.")

def createDailyFileFromName(person):
    #print(len(person))
    if person == "":
        return ""
    fileName = person + ".day"
    fileName = unidecode.unidecode(encodeText(fileName))
    fileName = fileName.replace(" ", "")
    return fileName

def processSumFile(nameOfSumFile, dateStat, data):
    fileName = data["filenameToStore"].split(".html")[0] + "_sum.txt"
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return 0

def f_links(ctx):
    for title, page in [('Home', '/home.html'),
                        ('Login', '/login.html')]:
        yield ph.li(ph.a(href=page)(title))

def getDoneFiles():
    file = FILE_DONEFILE
    doneFilesList = []
    if os.path.exists(file):
        with open(file, 'r', encoding="utf-8") as reader:
            for line in reader.readlines():
                line = line. rstrip('\n')
                doneFilesList.append(line)
    else:
        doneFilePath = FILE_DONEFILE
        with open(doneFilePath, 'w') as fp:
            pass
        return []
    return doneFilesList