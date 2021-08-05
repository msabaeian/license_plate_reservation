import requests
from bs4 import BeautifulSoup
import sys
import enum
import urllib3
import re
import json
import codecs
urllib3.disable_warnings()

baseUrl = "https://nobatdehi.epolice.ir"
HEADERS = {
    "Sec-Ch-Ua": '"Chromium";v="91", " Not;A Brand";v="99"',
    "Accept": "*/*",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://nobatdehi.epolice.ir",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close"
}


def main(sessId,user_id,office,service_type,pelak_type,pelak_first,pelak_middle,pelak_last,pelak_city_number,):
    r = requests.session()
    cookies = dict(
        PHPSESSID=sessId,
        epolicenopardaz_userid=user_id
    )

    # step 1: get office id
    print("[*] Getting Office details")
    try:
        res = r.get(baseUrl+"/office/"+office, headers=HEADERS, cookies=cookies, verify=False)
    except Exception as e:
        print("[error]: {}".format(e))
        sys.exit()
    soup = BeautifulSoup(res.content, features="html.parser")
    officeId = re.findall('var office_id = (.*?);\s*$', str(soup), re.M)[0].replace('"',"")
    print("[*] Office Id is "+officeId)


    # step 2: get dates
    data = "office={}&special={}".format(officeId,service_type)
    print("[*] Getting dates of service")
    try:
        res = r.post(baseUrl+"/appointment_daftar/", data=data, headers=HEADERS, cookies=cookies, verify=False)
    except Exception as e:
        print("[error]: {}".format(e))
        sys.exit()
    soup = BeautifulSoup(res.content, features="html.parser")
    lastDay = soup.find_all('a',{'class':'day-active-v'})[-1].get('data-load')
    print("[*] Last day is: "+lastDay)

    # step 3: Getting times
    data = "office_id={}&special={}&get_date={}".format(officeId,service_type,lastDay)
    print("[*] Getting times")
    try:
        res = r.post(baseUrl+"/reserve_office/", data=data, headers=HEADERS, cookies=cookies, verify=False)
    except Exception as e:
        print("[error]: {}".format(e))
        sys.exit()
    soup = BeautifulSoup(json.loads(codecs.decode(res.text.encode(), 'utf-8-sig')).get('print'), features="html.parser")

    timeInputMode = False
    times = soup.find_all('a',{'class':'btn-success ltr'})
    if(len(times) == 0):
        times = soup.find_all('input',{'type':'hidden', 'name': 'time'})
        timeInputMode = True
    print("[*] {} open times founded".format(len(times)))

    reserved = False
    reservedText = "window.location.href"
    successReserve = "alert alert-success"
    for time in times:
        date = time.get('value') if timeInputMode else time.text+":00"
        print("[*] Trying to reserve",date)
        data = "mod=search&action=reserve&time={}".format(date)
        try:
            res = r.post(baseUrl, data=data, headers=HEADERS, cookies=cookies, verify=False)
        except Exception as e:
            print("[error]: {}".format(e))
            sys.exit()
        # soup = BeautifulSoup(res.content, features="html.parser")
        if reservedText in res.text:
            print("[-] {} has been reserved by another person",date)
            continue
        data = "special={}&type_pelak={}&txtnation0={}&txtnation3={}&txtnation2={}&txtnation1={}&txtmotor1=&txtmotor0=&shomare_shasi=&term=1&mod=search&action=payment_reserve".format(service_type, pelak_type,pelak_city_number,pelak_last,pelak_middle,pelak_first)
        try:
            res = r.post(baseUrl, data=data, headers=HEADERS, cookies=cookies, verify=False)
        except Exception as e:
            print("[error]: {}".format(e))
        if successReserve in res.text:
            print("[*] The {} on {} has been reserved for you".format(date,lastDay))
            break
    sys.exit()
        



def enum(**enums):
    return type('Enum', (), enums)


############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################


    
ServiceType = enum(
   Enteghal = 13,
   Ehraz = 14,
   Mozayedeei = 15,
   Varedati = 16,
   CartAlmosana = 17,
   SanadAlmosana = 18,
   FakRahn = 19,
   Eslah = 20,
   PelakAlmosana = 21,
   PelakMajazi = 22,
   TaeidieNaghl = 23,
   TavizArkan = 24
)

CarType = enum(
   SavariShakhsi = "khodro",
   SavariDolati = "khodro_dolati",
   SavariOmumi = "savari_omoomi",
   VanetShakhsi = "vanet",
   VanetDolati = "vanet_doulati",
   VanetOmumi = "vanet_omoomi",
   Taxi = "taxi",
   KhodroSangin = "khodro_sangin",
   MashinKeshavarzi = "keshavarzi"
)

CarPelakType = enum(
    A = "01",
    GH = "10",
    L = "11",
    M = "12",
    N = "13",
    V = "14",
    H = "15",
    Y = "16",
    Malolin = "19",
    B = "02",
    J = "04",
    D = "05",
    S = "06",
    SAD = "07",
    TA = "08",
    T = "03",
    EIN = "09",
    K = "18"
)

main(
    sessId="", # your PHPSESSID
    user_id="", # your epolicenopardaz_userid
    office = "177842", # office id in website url
    service_type = ServiceType.Enteghal,
    pelak_type = CarType.SavariShakhsi,
    pelak_first = "", # the first 2 numbers of plate
    pelak_middle = CarPelakType.V,
    pelak_last = "", # the 3 numbers of plate
    pelak_city_number = "" # city code of plate
)