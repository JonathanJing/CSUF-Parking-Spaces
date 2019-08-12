import urllib.request as ur
from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3

#Web
url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
html = ur.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

#SQL
conn = sqlite3.connect('parking.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Nutwood')

cur.execute('''
CREATE TABLE Nutwood (available INTEGER, time TIME)''')


for name in soup.find_all(id='gvAvailability_HyperLink_LocationName_0'):
  print(name.text)
for time in soup.find_all(id='gvAvailability_Label_LastUpdated_0'):
  print(time.text)
  datetime_str = time.text
  datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
  print(datetime_object)
for available in soup.find_all(id='gvAvailability_Label_Available_0'):
  avai_num = available.text
  print(available.text)

cur.execute('''INSERT INTO Nutwood (available, time)
        VALUES (?,?)''', (avai_num, datetime_object))

conn.commit()
cur.close()
