import re
import math
from datetime import date

def findRangeTanggal(tanggal1, tanggal2):
    awal = tanggal1.split('/')
    akhir = tanggal2.split('/')
    d0 = date(int(awal[2]), int(awal[1]), int(awal[0]))
    d1 = date(int(akhir[2]), int(akhir[1]), int(akhir[0]))
    delta = d1 -d0
    return delta.days

def daysToWeeks(days):
    return math.floor(days/7)

def monthToNumber(bulan):
    bulan = bulan.lower()
    if(bulan == "januari"):
        return "01"
    elif(bulan == "februari"):
        return "02"
    elif(bulan == "maret"):
        return "03"
    elif(bulan == "april"):
        return "04"
    elif(bulan == "mei"):
        return "05"
    elif(bulan == "juni"):
        return "06"
    elif(bulan == "juli"):
        return "07"
    elif(bulan == "agustus"):
        return "08"
    elif(bulan == "september"):
        return "09"
    elif(bulan == "oktober"):
        return "10"
    elif(bulan == "november"):
        return "11"
    elif(bulan == "desember"):
        return "12"
    else:
        return ""

def findTanggal(kalimat):
    format1 = re.compile("(0[1-9]|[12][0-9]|3[0-1])-(0[1-9]|[1][0-2])-(\d+)") #dd-mm-yy 21-05-2021
    format2 = re.compile("(0[1-9]|[12][0-9]|3[0-1])/(0[1-9]|[1][0-2])/(\d+)") #dd/mm/yyyy 21/05/2021
    format3 = re.compile("(0[1-9]|[12][0-9]|3[0-1])(\s)([a-zA-Z]{3,})\s(\d+)") #dd MMMM yyyy 21 Mei 2021
    tanggal = []
    valid = format1.search(kalimat)
    while valid:
        tanggal.append(valid.group().replace('-','/'))
        kalimat = kalimat.replace(valid.group(), '', 1)
        valid = format1.search(kalimat)
    valid = format2.search(kalimat)
    while valid:
        tanggal.append(valid.group())
        kalimat = kalimat.replace(valid.group(), '', 1)
        valid = format2.search(kalimat)
    valid = format3.search(kalimat)
    while valid:
        bulan = re.search("\s\w{3,}\s", valid.group())
        bulan = bulan.group().strip()
        tanggal.append(valid.group().replace(' ', '/').replace(bulan, monthToNumber(bulan)))
        kalimat = kalimat.replace(valid.group(), '', 1)
        valid = format3.search(kalimat)
    return tanggal