import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter URL: ",)
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

#extract all elements with <h2> tags and converts Soup elements into strings
allHeaders = []

headerTwo = soup('h2')
for header in headerTwo:

    allHeaders.append(str(header))

#extract WMAs and Hatcheries
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


#remove all <h2>/</h2> tags
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
removeAnchors = []

for aExtract in brEndRemoved:
    if "</a>" in aExtract:
        removeAnchors.append(aExtract.partition("</a>")[2])
    else:
        removeAnchors.append(aExtract)


#parse all HTML elements from url
allHTML = []

allElements = soup()
aEStrings = (str(allElements))
allHTML.append(aEStrings)

#remove line breaks found in <h2> for allElements
noLineBreak = []
for brRMV in allHTML:
    noLineBreak.append(brRMV.replace("<br>",""))

noMoreLB = noLineBreak


#lists all iterations except last
squat = 0

metaDataOne = []

while squat < len(removeAnchors) - 1:
    for ancRMV in noMoreLB:
            #print(squat)
            ancStart = removeAnchors[squat]
            ancEnd = removeAnchors[squat + 1]
            metaDataOne.append(ancStart + ":" + (ancRMV[ancRMV.index(ancStart)+len(ancStart):ancRMV.index(ancEnd)]))
            squat = squat + 1


            #print(ancStart)
            #print(ancEnd)
            #print("_____________________________________________________________________________")
            #print(varTest)


#appends last listing to data list
finalIndex = len(removeAnchors) - 1
for finalLine in noMoreLB:

    finalSearchStart = removeAnchors[finalIndex]
    finalSearchEnd = "<footer>"
    metaDataOne.append(finalSearchStart + ":" + finalLine[finalLine.index(finalSearchStart)+len(finalSearchStart):finalLine.index(finalSearchEnd)])


#print(len(metaDataOne))
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

#Georgia search queries
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

# Could also just set a search input with these criteria and print the instances that present
# The argument intake needs to be addressed. If we have a search bar it needs to be able to supply all the instance combinations through accessing the function.

#def search(meta):

wmaGaLegends = [signQ, bonusQ, quotaQ, archOnlyQ, specialtyHuntQ, huntLearnQ, qualityBuckQ, mobilityQ, birdDogQ, furDogQ, rabbitDogQ, archRangeQ, firearmsRangeQ]
wmaGaLegendsStrings = [sign, bonus, quota, archOnly, specialtyHunt, huntLearn, qualityBuck, mobility, birdDog, furDog, rabbitDog, archRange, firearmsRange]

#Validates that all lists are equal
print(len(metaDataOne))
print(len(removeAnchors))


#finds and logs legends

def legendsParse(legend, legendNames, wmaData):
    wmaGAIndex = 0
    for line in wmaData:
        legendIndex = 0
        print("WMA Name" + ": " + removeAnchors[wmaGAIndex])
        wmaGAIndex = wmaGAIndex + 1
        #print(wmaGAIndex)
        while legendIndex < len(legend):
            if legend[legendIndex] in line:
                print(legendNames[legendIndex] + ": " + "1")
                legendIndex = legendIndex + 1
                #print(legendIndex)
            else:
                print(legendNames[legendIndex] + ": " + "0")
                legendIndex = legendIndex + 1
                #print(legendIndex)
        print("________________________________")
    return "Legends scrape complete."




print(legendsParse(wmaGaLegends, wmaGaLegendsStrings, metaDataOne))
print(len(removeAnchors))
