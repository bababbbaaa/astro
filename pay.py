import pandas as pd
from horoscopedb import ConnectDb
import xlsxwriter
import pyodbc


conn = ConnectDb()
cur=conn.cursor()
with pd.ExcelWriter("Output.xlsx", engine="xlsxwriter") as writer:
    try:
        cur.execute("SELECT * FROM Users")
        df=cur.fetchall()
        df = pd.DataFrame(df)
        df.to_excel(writer, sheet_name='name')
        print("File saved successfully!")
    except:
        print("There is an error")
