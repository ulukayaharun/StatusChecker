from sqlalchemy import create_engine
import pandas as pd
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

link_df = pd.DataFrame(columns=["URL","DATETIME"])  # Linkleri saklamak için DataFrame

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        if link :
            add_link(link)
    #templates klasörü oluşturup içinde html dosyası oluşturmaya gerek kalmaması için kod 
    html_index="""
    <h1>Status Checker</h1>
    <form method="POST">
        <label for="link">Link Ekleyin:</label>
        <input type="text" name="link" id="link">
        <button type="submit">Ekle</button>
    </form>
    """
    return html_index

#Linkleri dataframe'e ve database'e kaydetmek için fonksiyon
def add_link(link):
    timestamp=datetime.now()
    link_df.loc[len(link_df)] = [link, timestamp]
    save_to_database()


def save_to_database():
    global link_df
    #database'e bağlanma
    sqlalchemy_database_url = "mysql+pymysql://remote:BIw883k8@212.31.2.93/monitor"
    engine = create_engine(sqlalchemy_database_url, connect_args={"charset": "utf8mb4"},echo=True)
    try:
        link_df.to_sql("url", engine, if_exists="append", index=False)
        link_df = pd.DataFrame(columns=["URL","DATETIME"])  # DataFrame'i sıfırlar ve aynı linkin veritabanında tekrar tekrar girilmesini engeller.
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(debug=True)
