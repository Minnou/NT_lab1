import requests
import time
import re
from http import HTTPStatus

retry_codes = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]

days = 5
i = 1
https = "https:"
currentUrl = "//www.cbr-xml-daily.ru/daily_json.js"
resultFile = open("./usd.csv", "w+", encoding="utf-8")
retries = 0
maxRetries = 3
timeDelay = 0.7

while (i <= days):
    try:
        rawData = requests.get(https + currentUrl)
        rawData.raise_for_status()
    except requests.HTTPError as exc:
        code = exc.response.status_code
        
        if code in retry_codes and retries < maxRetries:
            print("Something went wrong, retrying. retry #" + retries)
            retries += 1
            time.sleep(5)
            continue
        resultFile.close()
        raise
    
    retries = 0
    resultJSON = rawData.json()
    currentUrl = resultJSON["PreviousURL"]
    value = resultJSON["Valute"]["USD"]["Value"]
    date = re.match(pattern="(.*)T.*", string=resultJSON["Date"]).group(1)
    resultFile.write(str(date) + ";" + str(value) + "\n")
    print("day #" + str(i) + ". days remaining: " + str(days - i) + ". date: "+ str(date) + ". value: " + str(value) + "\n" )
    time.sleep(timeDelay)
    i += 1

resultFile.close()