import re
import kmp

def findWord(teks, pattern):
    kmptable = []
    
    if(kmp.kmp(teks.lower(), pattern.lower(), kmptable) == -1):
        return False
    else:
        return True

def findNumberAfterWord(text, word):
    return re.findall(r'%s\s(\d+)' % word, text.lower())

def findNumberBeforeWord(text, word):
    return re.findall(r'(\d+)\s%s' % word, text.lower())

def findMatkul(text):
    matkul = re.search('([a-zA-Z])+[0-9][0-9][0-9][0-9]', text)

    return matkul

def findTopik(text):
    topics = re.findall(r'"([^"]*)"', text)

    return topics

def findTask(kalimat):
    if (findWord(kalimat, "tubes")):
        return "Tubes"
    elif (findWord(kalimat, "tucil")):
        return "Tucil"
    elif (findWord(kalimat, "kuis")):
        return "Kuis"
    elif (findWord(kalimat, "ujian")):
        return "Ujian"
    elif (findWord(kalimat, "praktikum")):
        return "Praktikum"
