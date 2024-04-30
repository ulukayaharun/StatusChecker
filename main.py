from sqlalchemy import create_engine
import pandas as pd
import datetime
import requests
from time import sleep

# Veritabanı bağlantısı
engine = create_engine("mysql+pymysql://remote:BIw883k8@212.31.2.93/monitor", 
                       connect_args={"charset": "utf8mb4"}, echo=False)
link_df = pd.read_sql_table("url", engine)

def update_link_status():
    #Veritabaninda indexteki URL sütununa erişir
    for index, row in link_df.iterrows():
        link = row["URL"]
        update_link_response(index, link)
    save_to_database()

def update_link_response(index, link):
    timestamp = datetime.datetime.now()
    try:
        #Dataframe'i status_code ile beraber günceller
        response = requests.get(link)
        link_df.at[index, "STATUS"] = response.status_code
    except Exception:
        #Geçerli bir link değilse 0'a dönüştürür
        link_df.at[index, "STATUS"] = 0
    link_df.at[index, "DATETIME"] = timestamp

def save_to_database():
    #monitor/statuschecker tablosuna verileri kaydeder
    try:
        link_df.to_sql("statuschecker", engine, if_exists="append", index=False)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    update_link_status()
    print("Veritabaninda veri yok") if link_df.empty else print("Status Code Güncellendi")
    sleep(1)
