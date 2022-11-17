import horoscopedb as horoscopedb
import os
os.system("del -rf horoscope.db")
horoscopedb.CreateTables()
import loadExcel
