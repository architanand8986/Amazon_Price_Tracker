import requests
from bs4 import BeautifulSoup
from datetime import date

 
# look for headers so we can bypass the security protocols of Amazon

# this would return dictionary if the url is valid otherwise None
# as a extra feature we could add image url of amazon of the product in the site
def extract_Data(url):
    # headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36' }
    headers = { 
               'Accept-Encoding':'gzip, deflate, br',
               'Accept-Language':'en-US,en;q=0.9',
               'Referer':'https://www.amazon.in/',
               'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
               'Sec-Ch-Ua-Mobile':'?0',
               'Sec-Ch-Ua-Platform':"Windows",
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    try:
        res=requests.get(url,headers=headers)
        soup=BeautifulSoup(res.content,'html.parser')

        product_name=soup.select_one('h1#title').text
        price=soup.select_one('span.a-price-whole').text+soup.select_one('span.a-price-fraction').text
        symbol=soup.select_one('span.a-price-symbol').text
        today=date.today().strftime("%d/%m/%Y")

        dict={
            "name":product_name.strip(),
            "price":price,
            "currency":symbol,
            "date":today
        }
        
        return dict
    
    except:
        
        return None

if __name__=="__main__":
    mydict=extract_Data('https://www.amazon.in/OnePlus-Nord-Pastel-128GB-Storage/dp/B0BY8JZ22K/ref=lp_1389401031_1_2')
    
    print(type(mydict['price']),type(mydict['date']))
    
