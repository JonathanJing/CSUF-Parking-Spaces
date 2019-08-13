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

cur.execute('DROP TABLE IF EXISTS Parking')

cur.execute('''
CREATE TABLE Parking (
    Name TEXT UNIQUE,
    Available INTEGER,
    Time TIME
)''')

class rec_data:
  def __init__(self,building_id):
    self.i = building_id
  def data(self):
    for name in soup.find_all(id='gvAvailability_HyperLink_LocationName_'+ self.i):
      building_name = name.text
      print(name.text)
    for time in soup.find_all(id='gvAvailability_Label_LastUpdated_'+ self.i):
      datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
      print(datetime_object)
    for available in soup.find_all(id='gvAvailability_Label_Available_'+ self.i):
      avai_num = available.text
      print(available.text)
    cur.execute('''INSERT INTO Parking (Name, Available, Time)
        VALUES (?,?,?)''', (name.text, avai_num, datetime_object))

loop = ['0','1','2']
for i in loop:
  p1 = rec_data(i)
  p1.data()

conn.commit()
cur.close()
