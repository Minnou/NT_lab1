import requests
import time
import re

days = 100
i = 1
https = "https:"
currentUrl = "//www.cbr-xml-daily.ru/daily_json.js"
resultFile = open("./dataset.csv", "w+", encoding="utf-8")
retries = 0
maxRetries = 3
timeDelay = 0.7

while (i <= days):
    try:
        rawData = requests.get(https + currentUrl, timeout=30)
        rawData.raise_for_status()
    except:
        print("Something went wrong. ",end="")
        if retries < maxRetries:
            print("Retrying. retry #" + str(retries))
            retries += 1
            time.sleep(5)
            continue
        resultFile.close()
        raise
    
    retries = 0
    resultJSON = rawData.json()
    currentUrl = resultJSON["PreviousURL"]
    value = resultJSON["Valute"]["JPY"]["Value"]
    date = re.match(pattern="(.*)T.*", string=resultJSON["Date"]).group(1)
    resultFile.write(str(date) + ";" + str(value) + "\n")
    print("day #" + str(i) + ". days remaining: " + str(days - i) + ". date: "+ str(date) + ". value: " + str(value) + "\n" )
    time.sleep(timeDelay)
    i += 1

resultFile.close()