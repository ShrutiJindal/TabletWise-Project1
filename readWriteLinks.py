import bs4 as bs
import urllib2
from slugify import slugify
import pandas as pd
import os.path
import SendEmail


# Global Params #
domainLinkFilename = "domain_links_06_28_2017.csv"
changedSitesFileName = "changedSites.txt"

# Purpose
# 1. Read Domain Links csv File"
# 2. If the Website is hit for the first time create its corresponding file
# 3. Else compare the job links already present in file and now present on that Website
# 4. If all the links are same do nothing
# 5. Else append the changed link to the ChangedLinks File and email it

readLines = pd.read_csv(domainLinkFilename)
for index,row in readLines.iterrows():
    url = row[0]
    if pd.notnull(row[1]):
        divId = row[1]
    elif pd.notnull(row[2]):
        classId = row[2]
    else:
        raise ValueError("Either DivId or ClassId must be specied")
    print url,divId
    source = urllib2.urlopen(url).read()
    soup = bs.BeautifulSoup(source,"lxml")
    nav=soup.nav

    linksStrFromSite = ""
    linkStrfromFile = ""
    slugifiedFileName = slugify(url)
    for div in soup.find_all('div',{"id": divId}):
        for url in div.find_all('a'):
            linksStrFromSite = linksStrFromSite + (url.get('href'))
    if(os.path.isfile(slugifiedFileName + ".txt")):
        readFile = open(slugifiedFileName + ".txt","r")
        for link in readFile.readline():
            linkStrfromFile = linkStrfromFile + link
        if(linkStrfromFile != linksStrFromSite):
            writeFile = open(changedSitesFileName,"a")
            writeFile.write("\n"+slugifiedFileName)
            writeFile.close()
            SendEmail.send_mail("shruti15792@gmail.com","shruti15792@gmail.com","check","check",changedSitesFileName)
    else:
        writeFile = open(slugifiedFileName + ".txt","w")
        writeFile.write(linksStrFromSite)
        writeFile.close()








