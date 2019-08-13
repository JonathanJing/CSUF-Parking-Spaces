import os
import urllib.request as ur
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
from apscheduler.schedulers.blocking import BlockingScheduler

#Web
url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
html = ur.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

#SQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="parking"
)
cur = mydb.cursor()

#cur.execute("DROP TABLE IF EXISTS Parking")

#cur.execute("CREATE TABLE Parking (Name VARCHAR(30), Available INTEGER, Time DATETIME)")

class rec_data:
  def __init__(self,building_id):
    self.i = building_id
  def data(self):
    for name in soup.find_all(id='gvAvailability_HyperLink_LocationName_'+ self.i):
      print(name.text)
    for time in soup.find_all(id='gvAvailability_Label_LastUpdated_'+ self.i):
      datetime_str = time.text
      datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
      print(datetime_object)
    for available in soup.find_all(id='gvAvailability_Label_Available_'+ self.i):
      print(available.text)
    sql = "INSERT IGNORE INTO Parking (Name, Available, Time) VALUES (%s,%s,%s)"
    val = (name.text, available.text, datetime_object)
    cur.execute(sql, val)
    mydb.commit()

def tick():
    loop = ['0','1','2']
    for i in loop:
        p1 = rec_data(i)
        p1.data()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=90)
    print('Press Ctrl+C to exit')
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    cur.close()
    pass
