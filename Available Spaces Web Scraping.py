import re
import urllib.request as ur
from datetime import datetime
from bs4 import BeautifulSoup

url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
html = ur.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

for name in soup.find_all(id='gvAvailability_HyperLink_LocationName_0'):
  print(name.text)
for time in soup.find_all(id='gvAvailability_Label_LastUpdated_0'):
  print(time.text)
  datetime_str = time.text
  datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
  print(datetime_object)
for available in soup.find_all(id='gvAvailability_Label_Available_0'):
  print(available.text)
