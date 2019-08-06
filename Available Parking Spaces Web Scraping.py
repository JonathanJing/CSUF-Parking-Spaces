import re
import urllib.request as ur
from bs4 import BeautifulSoup


url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
html = ur.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
tags = soup('td')
   

for tag in tags:
    #name = tag.find('a')
    #num = tag.find('span')
    
    #time = tag.find_all('span')
    #time = tag.find('p',class_='LastUpdated')
   
    content = tag.get_text()
    content = content.strip()
    content = content.split('\n')
    
    #if re.findall('Structure',name.contents[0]):
      #print(name.contents[0])
    #if re.findall('[0-9]',num.contents[0]):
      #print(num.contents[0])
      
    if re.findall('[a-z]',content[0]):
      print(content[0]) #Name
      print('Total:',content[2]) #Total Available
      u_time = content[3]
      #print(content[3]) #Upload time
    if re.findall('[0-9]',content[0]):
      print('Current:',content[0]) #Current Available
      print(u_time,'\n')
