from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

start_date = datetime(2021, 12, 20)
end_date = datetime.now()

date_range = pd.date_range(start=start_date, end=end_date, freq='D')
df_tarihler = pd.DataFrame({'date': date_range,'entry_count':0})

website="https://eksisozluk1923.com/recep-tayyip-erdogan--95281?p=" 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}
html_text=requests.get(website,headers=headers).text
soup=BeautifulSoup(html_text,"html.parser")
data=soup.find("div",id="topic")
page_count=soup.find("div",class_="pager")

all_entries=data.find_all("div",class_="content")
authors=data.find_all("a",class_="entry-author")
sent_date=data.find_all("a",class_="entry-date permalink")


for pages in range(1,3476):
    
    
    html_text=requests.get(website+str(pages),headers=headers).text
    soup=BeautifulSoup(html_text,"html.parser")
    data=soup.find("div",id="topic")
    page_count=soup.find("a",class_="last")
    
    all_entries=data.find_all("div",class_="content")
    authors=data.find_all("a",class_="entry-author")
    sent_date=data.find_all("a",class_="entry-date permalink")

    for i in range(10):
        
        """
        print(all_entries[i].text.strip())
        print("Yazar :",authors[i].text)
        print("Tarih :",sent_date[i].text)
        
        if(i==9):
            print(f"--------------{pages}.SAYFA BİTTİ-------------- \n")
        else:
            print("-"*40)
        """
        
        year=(sent_date[i].text[6:10])
        day=(sent_date[i].text[0:2].lstrip("0"))
        month=(sent_date[i].text[3:5].lstrip("0"))
    
        tarih_count=datetime(int(year),int(month),int(day))
        df_tarihler.loc[df_tarihler["date"] == tarih_count, "entry_count"] += 1
        
        with open("entryler.txt","a",encoding="utf-8") as file:
            file.write(f"{all_entries[i].text.strip()} \n")
            file.write(f"Yazar : {authors[i].text} \n")
            file.write(f"Tarihi : {sent_date[i].text} \n")
            
    
            if(i==9):
                file.write(f"--------------{pages}.SAYFA BİTTİ-------------- \n")
            else:
                file.write("-"*40)
    
            file.write("\n")            
    print(f"Yazlıdı! {pages}")
df_tarihler.to_csv("tarihler.csv",index=False)