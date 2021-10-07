import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import requests
import re

GOOGLE_API_KEY = 'AIzaSyACfy1Gpj75UiBV-fa9NIfdhKCnskzZHvw'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.eregulations.com/georgia/hunting/wma-regulations-a-c"
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

#beginning codes for extrating Georgia hunt properties
#__________________________________________________________________________________________________________________________________________________________

#extract all elements with <h2> tags and converts Soup elements into strings
allHeaders = []

headerTwo = soup('h2')
for header in headerTwo:

    allHeaders.append(str(header))

#extract Georgia hunt properties and exclude <h2> tags that are not hunt properties
huntAreas = []

for h2Tags in allHeaders:
    if "WMA" in h2Tags:
        huntAreas.append(h2Tags)
    elif "Hatchery" in h2Tags:
        huntAreas.append(h2Tags)
    elif "State Park" in h2Tags or "state park" in h2Tags:
        huntAreas.append(h2Tags)
    elif "Area" in h2Tags:
        huntAreas.append(h2Tags)
    elif "PFA" in h2Tags:
        huntAreas.append(h2Tags)
    elif "Dove Field" in h2Tags:
        huntAreas.append(h2Tags)


#remove all <h2>/</h2> tags from hunt properties
hTagsRemoved = []

for hExtract in huntAreas:
    hStart = "h2>"
    hEnd = "</h2"
    hTagsRemoved.append(hExtract[hExtract.index(hStart)+len(hStart):hExtract.index(hEnd)])

#remove front line break tags
brRemoved = []

for brExtract in hTagsRemoved:
    brRemoved.append(brExtract.replace("<br>",""))

#remove closing line break tags
brEndRemoved = []

for brEndExtract in brRemoved:
    brEndRemoved.append(brEndExtract.replace("</br>",""))

#remove anchor tags (Clean WMA list)
cleanGeorgiaWMA = []

for aExtract in brEndRemoved:
    if "</a>" in aExtract:
        cleanGeorgiaWMA.append(aExtract.partition("</a>")[2])
    else:
        cleanGeorgiaWMA.append(aExtract)


#parse all HTML elements from url to begin scraping data for each hunt property
allHTML = []

allElements = soup()
aEStrings = (str(allElements))
allHTML.append(aEStrings)

#remove line breaks found in <h2> for allElements
noLineBreak = []
for brRMV in allHTML:
    noLineBreak.append(brRMV.replace("<br>",""))

noMoreLB = noLineBreak


#creates list of each individual hunt propety data except for the last one
indexGeorgiaWMAList = 0

finalGeorgiaWMAList = []

while indexGeorgiaWMAList < len(cleanGeorgiaWMA) - 1:
    for ancRMV in noMoreLB:
            #print(indexGeorgiaWMAList)
            ancStart = cleanGeorgiaWMA[indexGeorgiaWMAList] + "<"
            ancEnd = cleanGeorgiaWMA[indexGeorgiaWMAList + 1] + "<"
            finalGeorgiaWMAList.append(ancStart + ":" + (ancRMV[ancRMV.index(ancStart)+len(ancStart):ancRMV.index(ancEnd)]))
            indexGeorgiaWMAList = indexGeorgiaWMAList + 1


#adds the last hunt property data to the list above
finalIndex = len(cleanGeorgiaWMA) - 1
for finalLine in noMoreLB:

    finalSearchStart = cleanGeorgiaWMA[finalIndex]
    finalSearchEnd = "<footer>"
    finalGeorgiaWMAList.append(finalSearchStart + ":" + finalLine[finalLine.index(finalSearchStart)+len(finalSearchStart):finalLine.index(finalSearchEnd)])

#end of Georgia hunt propety name scrape
#__________________________________________________________________________________________________________________________________________________________

#beginning codes for extracting Legends data for each individual hunt area
#__________________________________________________________________________________________________________________________________________________________

# Legend Icons
# Names will act as place holders
sign = 'Sign In'
bonus = 'Bonus Deer Hunt'
quota = 'Quota Hunt'
archOnly = 'Archery Only Area'
specialtyHunt = 'Specialty Hunting'
huntLearn = 'Hunt & Learn'
qualityBuck = 'Quality Buck'
mobility = 'Mobility-Impaired Hunt'
birdDog = 'Bird Dog Training'
furDog = 'Furbearer Dog Training'
rabbitDog = 'Rabbit Dog Training'
archRange = 'Archery Range'
firearmsRange = 'Firearms Shooting Range'

#used to search html data unique for each Legend
signQ = 'sign-in'
bonusQ = 'bonus'
quotaQ = 'WMA-Styles_Quota-Symbol'
archOnlyQ = 'Archery Only Area'
specialtyHuntQ = 'WMA-Styles_ADULT-CHILD'
huntLearnQ = 'Hunt & Learn'
qualityBuckQ = 'Quality Buck'
mobilityQ = 'WMA-Styles_WHEELCHAIR'
birdDogQ = "<span class=\"WMA-Styles_GAHD-ICONS--black-\">" + "B"
furDogQ = "<span class=\"WMA-Styles_GAHD-ICONS--black-\">" + "F"
rabbitDogQ = 'WMA-Styles_RABBIT-DOG'
archRangeQ = 'WMA-Styles_ARCHERY-RANGE'
firearmsRangeQ = 'WMA-Styles_FIREARMS-RANGE'

#variables for the above
wmaGaLegends = [signQ, bonusQ, quotaQ, archOnlyQ, specialtyHuntQ, huntLearnQ, qualityBuckQ, mobilityQ, birdDogQ, furDogQ, rabbitDogQ, archRangeQ, firearmsRangeQ]
wmaGaLegendsStrings = [sign, bonus, quota, archOnly, specialtyHunt, huntLearn, qualityBuck, mobility, birdDog, furDog, rabbitDog, archRange, firearmsRange]

#Validates that all lists are equal
#print(len(finalGeorgiaWMAList))
#print(len(cleanGeorgiaWMA))

#finds and logs legends

def legendsParse(legend, legendNames, wmaData):
    wmaGAIndex = 0
    for line in wmaData:
        legendIndex = 0
        #print("WMA Name" + ": " + cleanGeorgiaWMA[wmaGAIndex])
        wmaGAIndex = wmaGAIndex + 1
        #print(wmaGAIndex)
        while legendIndex < len(legend):
            if legend[legendIndex] in line:
                #print(legendNames[legendIndex] + ": " + "1")
                legendIndex = legendIndex + 1
                #print(legendIndex)
            else:
                #print(legendNames[legendIndex] + ": " + "0")
                legendIndex = legendIndex + 1
                #print(legendIndex)
        #print("________________________________")
    return "Legends scrape completed. Please validate that all data was correctly extracted from the input URL."


#for user validation
#print(legendsParse(wmaGaLegends, wmaGaLegendsStrings, finalGeorgiaWMAList))
#print(len(cleanGeorgiaWMA))

#beginning codes for extracting Acres and Phone
#__________________________________________________________________________________________________________________________________________________________

indexWMAPhone = 0

for aString in finalGeorgiaWMAList:
    if "•" in aString:
        partitionedString = aString.partition('• ')
        acresPart = partitionedString[0].rsplit(">", 1)
        #print(cleanGeorgiaWMA[indexWMAPhone])


        phonePart = partitionedString[len(partitionedString) - 1]
        phoneClean = phonePart.partition('<')
        phoneNumber = phoneClean[0]
        #print(phoneNumber + " • " + acresPart[len(acresPart) - 1])
        #print(phoneClean[0])
        #print("________________________________________________________________________________")
        indexWMAPhone += 1
    else:
        print(cleanGeorgiaWMA[indexWMAPhone])
        partitionedPhoneOnly = aString.partition('Other_WMA-Section_WMA-Acres-Phone\">')
        phoneOnlyPart = partitionedPhoneOnly[2]
        #print(phoneOnlyPart)
        phoneOnlyClean = phoneOnlyPart.partition('<')
        phoneOnlyNumber = phoneOnlyClean[0]
        #print(phoneOnlyNumber)
        #print("________________________________________________________________________________")
        indexWMAPhone += 1

#print(len(cleanGeorgiaWMA))
#print(indexWMAPhone)


#beginning codes for extracting Latitude and Longitude
#__________________________________________________________________________________________________________________________________________________________

'''def extract_lat_long(address_or_zipcode):
    formatted_address, lat, lng = None, None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None, None
    try:
        results = r.json()['results'][0]
        formatted_address = results['formatted_address']
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return formatted_address, lat, lng

#print(extract_lat_long(input("Enter Hunt Area: ",)))


latLongList =[]
for line in cleanGeorgiaWMA:
    toady = line, extract_lat_long(line)
    latLongList.append(toady)

for item in latLongList:
    print(item)'''

#beginning codes for phone and acre

#beginning codes for extracting indvidual WMA data
#__________________________________________________________________________________________________________________________________________________________

wmaSubDataList = []

for dataSeparation in finalGeorgiaWMAList:
    blankList = []
    #print(dataSeparation)
    #separate all <h3> tags via indexing
    h3String = "<h3>"
    h3Index = [i for i in range(len(dataSeparation)) if dataSeparation.startswith(h3String, i)]
    h3IndexInt = (h3Index)
    #locate </div> tags to clean up last property pull
    divString =  "</div>"
    divIndex = [i for i in range(len(dataSeparation)) if dataSeparation.startswith(divString, i)]
    #print(h3IndexInt)
    subIndex2 = 0

    while subIndex2 < len(h3IndexInt) - 1:

        subIndex3 = subIndex2 + 1
        h3IndexStart = h3IndexInt[subIndex2]
        h3IndexEnd = h3IndexInt[subIndex3]
        blankList.append(dataSeparation[h3IndexStart:h3IndexEnd])
        #print("________________________________________")
        subIndex2 += 1
        #print(subIndex2)
        #print("________________________________________")

    lastSubItem = dataSeparation[h3Index[len(h3Index) - 1]:]
    partedSubItem = lastSubItem.partition("</div>")
    blankList.append(partedSubItem[0])
    wmaSubDataList.append(blankList)
    #print("_______________________________________________________________________________________________________________________________")

wmaSubDataListLastIndex = len(wmaSubDataList) - 1
#print(wmaSubDataList[wmaSubDataListLastIndex])

#for subLine in wmaSubDataList:
#    print(subLine.get_text())
#    print("____________________________________________________________")

#beginning codes for cleaning up wmaSubDataList
#__________________________________________________________________________________________________________________________________________________________

wmaSubDataDone = []

for sweepLine in wmaSubDataList:
    sweepLine = [w.replace('<h2>', '') for w in sweepLine]
    sweepLine = [w.replace('<h3>Directions</h3>', 'Directions: ') for w in sweepLine]
    sweepLine = [w.replace('<h3>', 'Game Type: ') for w in sweepLine]
    sweepLine = [w.replace('</h3>', '') for w in sweepLine]
    sweepLine = [w.replace('&amp;', '&') for w in sweepLine]
    sweepLine = [w.replace('<h4>', 'Weapon Type: ') for w in sweepLine]
    sweepLine = [w.replace('</h4>', '') for w in sweepLine]
    sweepLine = [w.replace('Buck Only:', 'Buck Only') for w in sweepLine]
    sweepLine = [w.replace('<p class=\"Other_WMA-Section_WMA-Seasons\"><span class=\"Other_WMA-Section_WMA-Medium\">', '') for w in sweepLine]
    sweepLine = [w.replace('Game Type: Special Regs', 'Special Regs: ') for w in sweepLine]
    sweepLine = [w.replace('Special Regs: \n<p class="Other_WMA-Section_WMA-Seasons">', 'Special Regs: \n') for w in sweepLine]
    sweepLine = [w.replace('<ul>', '') for w in sweepLine]
    sweepLine = [w.replace('</ul>', '') for w in sweepLine]
    sweepLine = [w.replace('</li>', '') for w in sweepLine]
    sweepLine = [w.replace('<li class="Other_WMA-Section_WMA-Seasons-Sub-Bullets">', 'Dates: ') for w in sweepLine]
    sweepLine = [w.replace('</span>', '') for w in sweepLine]
    sweepLine = [w.replace('</p>', '') for w in sweepLine]
    sweepLine = [w.replace('<p class="Other_WMA-Section_WMA-Seasons">', 'Dates: ') for w in sweepLine]
    sweepLine = [w.replace('<span class=', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_HONORARY"', '') for w in sweepLine]
    sweepLine = [w.replace('"Other_WMA-Section_WMA-Medium"', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_Quota-Symbol"', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_ADULT-CHILD"', '') for w in sweepLine]
    sweepLine = [w.replace('>C', '') for w in sweepLine]
    sweepLine = [w.replace('>Q40 "WMA-Styles_GAHD-ICONS--black-">s', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_GAHD-ICONS--black-"', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_RABBIT-DOG"', '') for w in sweepLine]
    sweepLine = [w.replace('>B ', '') for w in sweepLine]
    sweepLine = [w.replace('>R ', '') for w in sweepLine]
    sweepLine = [w.replace('>F ', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor018"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor018"</a', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_WHEELCHAIR"', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor019"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('>s ', '') for w in sweepLine]
    sweepLine = [w.replace('"blue">', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor023"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('>H>', '') for w in sweepLine]
    sweepLine = [w.replace('>b>', '') for w in sweepLine]
    sweepLine = [w.replace('>H ', '') for w in sweepLine]
    sweepLine = [w.replace('>s>', '') for w in sweepLine]
    sweepLine = [w.replace('"WMA-Styles_HUNT-TO-LEARN">', '') for w in sweepLine]
    sweepLine = [w.replace('>b ', '') for w in sweepLine]
    sweepLine = [w.replace('>W>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor020"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<strong>', '') for w in sweepLine]
    sweepLine = [w.replace('</strong>', '') for w in sweepLine]
    sweepLine = [w.replace('Deer & bear', 'Deer & Bear') for w in sweepLine]
    sweepLine = [w.replace('l>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor022"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor024"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor021"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('>F> ', '') for w in sweepLine]
    sweepLine = [w.replace('>', '') for w in sweepLine]
    sweepLine = [w.replace('  ', ' ') for w in sweepLine]
    sweepLine = [w.replace(' :', ':') for w in sweepLine]
    sweepLine = [w.replace('s ', '') for w in sweepLine]
    sweepLine = [w.replace(' - ', '-') for w in sweepLine]
    sweepLine = [w.replace(' -', '-') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor018"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor018"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor019"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor019"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor020"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor023"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor020"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor021"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor022"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor024"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor021"></a>', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor026"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor027"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor028"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor029"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor030"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor031"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor032"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor033"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor034"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor035"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor036"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor037"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor038"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor039"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor040"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor041"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor042"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<li', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor043"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor044"</a', '') for w in sweepLine]
    sweepLine = [w.replace('<a id="_idTextAnchor022"</a', '') for w in sweepLine]
    wmaSubDataDone.append(sweepLine)

#print(len(wmaSubDataDone))

#for subSweep in wmaSubDataDone:
    #print(subSweep)
    #for subSubSweep in subSweep:
    #    print(subSubSweep)
     #   print("========================")
    #print('______________________________________________________________________________')


#beginning codes for dates
#__________________________________________________________________________________________________________________________________________________________

#Convert linebreaks into pipes used for delimters
delimeterList = []

for lineClean in wmaSubDataDone:
    lineClean = [l.replace('\n\n', ' | ') for l in lineClean]
    lineClean = [l.replace('\n', ' | ') for l in lineClean]
    #lineClean = [l.replace('| Weapon Type', '** Weapon Type ') for l in lineClean]
    delimeterList.append(lineClean)

#Removes Special Regs and Directions list items
for line in delimeterList:
    for poofLine in line:
        if 'Special Regs:' in poofLine:
            indexOfSR = line.index(poofLine)
            line.remove(line[indexOfSR])

for line in delimeterList:
    for poofLine in line:
        if 'Directions:' in poofLine:
            indexOfDir = line.index(poofLine)
            line.remove(line[indexOfDir])

#Removes ending pipes
cleanFullList = []

for line in delimeterList:
    cleanList = []
    for subLine in line:
        lastCharIndex = subLine.rfind("|")
        subLine = subLine[:lastCharIndex] + "" + subLine[lastCharIndex+1:]
        cleanList.append(subLine)
    cleanFullList.append(cleanList)


#Splits every element inside list into their own lists to prep for dictionary conversion
splitList = []

for line in cleanFullList:
    subList = []
    for subLine in line:
        subList.append(subLine.split(', '))
    splitList.append(subList)

#Converts all list elements to strings to consolidate dates
stringList = []

for line in splitList:
    subList = []
    for subLine in line:
        outString = " "
        subList.append(outString.join(subLine))
    stringList.append(subList)

#Create lists from each list items using "|" delimiter
dataComplete = []

for line in stringList:
    subList = []
    for subLine in line:
        subList.append(subLine.split('|'))
    dataComplete.append(subList)

'''for line in dataComplete:
    for subLine in line:
        print(subLine)
    print('__________________________________________________________________')'''

#remove : after Q
#______________________________________________________________________________________________________________________

quotaRemoval = []
quota = ".+Q.+:"

for line in dataComplete:
    subList = []
    for subLine in line:
        lowerList = []
        for lowerLine in subLine:
            match = bool(re.match(quota, lowerLine))
            if match == True:
                #print(lowerLine)
                quotaIndex = []
                for i in range(len(lowerLine)):
                    if (lowerLine[i] == ':'):
                        quotaIndex.append(i)
                if len(quotaIndex) > 1:
                    idx = quotaIndex[1]
                    lowerList.append(lowerLine[:idx] + lowerLine[idx+1:])
                else:
                    lowerList.append(lowerLine)
            else:
                lowerList.append(lowerLine)
        #print(lowerList)
        #print('________________________________________________')
        subList.append(lowerList)
    quotaRemoval.append(subList)

#add Dates key to orphan dates

datesKey = []

for line in quotaRemoval:
    subList = []
    for subLine in line:
        lowerList = []
        for lowerLine in subLine:
            if ':' in lowerLine:
                lowerList.append(lowerLine)
            else:
                lowerList.append("Dates:" + lowerLine)
        subList.append(lowerList)
    datesKey.append(subList)


#begin dictionary conversion
#orphan dates need to be concatenated with keys
dictionConvert = []

for line in datesKey:
    subList = []
    for subLine in line:
        #print(subLine)
        d = {}
        for lowerLine in subLine:
            i = lowerLine.split(': ')
            d[i[0]] = i[1]

        subList.append(d)
    #print(subList)
    dictionConvert.append(subList)

#begin collision avoidance for dates and game weapon type

datesAntiCollision = []

for line in dictionConvert:
    subList = []
    for subLine in line:
        #print(subLine)
        count = 1
        countTwo = 1
        d = {}
        for key, value in subLine.items():
            if 'Dates' in key:
                upCount = str(count)
                key = key.replace(key, key + " " + upCount)
                d.update({key:value})
                count = count + 1
            elif 'Weapon Type' in key:
                upCountTwo = str(countTwo)
                key = key.replace(key, key + " " + upCountTwo)
                d.update({key:value})
                countTwo = countTwo + 1
            else:
                d.update({key:value})
        subList.append(d)
    datesAntiCollision.append(subList)


for line in datesAntiCollision:
    for subLine in line:
        print(subLine)
    print('______________________________________________')

    
