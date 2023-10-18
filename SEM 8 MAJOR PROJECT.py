#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install msedge-selenium-tools')


# In[2]:


import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
import pandas as pd
import csv
import json
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
import time


# In[3]:


q = input("Enter product name (Searching on flipkart)")
q = q.replace(" ","+")
test = []
names = []
flipPrices = []
prodNames = []
info,price = [],[]
url = "https://flipkart.com/search?q="
# query to search for.
#     q = input("Enter a query: ")
file_name = q.replace(" ", "_")
# response recieved in bytes
resp = requests.get(url+q)
# parsing response content using BeautifulSoup class, so that we can perform operations on it.
parsed_html = bs(resp.content, 'html.parser')
# data cleaning
raw_data = parsed_html.find("script", attrs={"id":"is_script"})
data = raw_data.contents[0].replace("window.__INITIAL_STATE__ = ","").replace(";","")
json_data = json.loads(data)
req_data = json_data["pageDataV4"]["page"]["data"]["10003"]   #[10]["widget"]["data"]["products"][3]["productInfo"]
#req_json_data = json_data["seoMeta"]["answerBox"]["data"]["renderableComponents"][0]["value"]["data"]

data_list = []
# print(len(req_data))
try:
    for i in range(1, len(req_data)):
        d = {}
        jd = req_data[i]["widget"]["data"]["products"]
        # print(len(jd))
        # print("i: ", i, end="\n")
        for j in range(len(jd)):
            jd2 = jd[j]["productInfo"]["value"]

            d["title"] = jd2["titles"]["title"]
            d["keySpecs"] = jd2["keySpecs"]
            d["rating"] = jd2["rating"]["average"]
            d["ratingCount"] = jd2["rating"]["count"]
            d["price"] = jd2["pricing"]["finalPrice"]["value"]
#                 d["warranty"] = jd2["warrantySummary"]
            d["url"] = jd2["smartUrl"]

            # You can uncomment below lines if you want to print json output on terminal

            # print("Title: ",jd2["titles"]["title"],end="\n")
            # print("key specs: ", jd2["keySpecs"], end="\n")
            # print("Rating: ", jd2["rating"]["average"], end="\n")
            # print("Total ratings: ", jd2["rating"]["count"], end="\n")
            # print("Price: ", jd2["pricing"]["finalPrice"]["value"],end="\n")
            # print("warranty: ", jd2["warrantySummary"], end="\n")
            # print("Smart url: ", jd2["smartUrl"], end="\n")
        data_list.append(d)


except:
    pass 
# dumping data to result.json file
#     print(list(data_list))
with open("flipkart"+'.json', 'w') as fp:
     json.dump(data_list, fp)

# Now let us write our data to csv file
data_file = open("flipkart"+'.csv', 'w') 

# create the csv writer object 
csv_writer = csv.writer(data_file) 

# Counter variable used for writing  
# headers to the CSV file 
count = 0

for data in data_list:
    if count == 0: 

        # Writing headers of CSV file 
        header = data.keys() 
        csv_writer.writerow(header) 
        count += 1
    # Writing data of CSV file 

    csv_writer.writerow(data.values()) 


with open('flipkart.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    rows = list(reader)
i,j = 0,2
while i in range(len(rows)):
    try:
        name = rows[j][0]
        #             name = " ".join(name.split(' ')[0:2])
#         print(name)
#         print("name = ",name)
        names.append(name)
        i += 1
        j += 2
    except:
            break
            
            
print("Best results",len(names))
#     print(names,len(names))
if len(names) < 10:
    f = open("flipkart.csv", "w")
    f.truncate()
    f.close()
    flipkart_url = "https://www.flipkart.com/search?q=" + q
    print(flipkart_url)
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    bigboxes = flipkart_html.find_all("a", {"class": "s1Q9rs"})
    soup = BeautifulSoup(flipkartPage, 'html.parser')
    info = soup.select("[class~=s1Q9rs]")
    if info == []:
        info = soup.select("[class~=IRpwTa]")
        
    flipPrices = soup.select("[class =_30jeq3]")
    prodNames = [i.get('title') for i in info]
    names = prodNames
    df = pd.DataFrame(list(zip(prodNames, flipPrices)), 
                   columns =['product_name', 'Flipkart_price']) 
    df.to_csv('test.csv')
    print(df,"brooooooooooooooooooo")

else:
    with open('flipkart.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rows = list(reader)
#     i,j = 0,2
#     while i in range(len(rows)):
#         try:
#             name = rows[j][0]
#             #             name = " ".join(name.split(' ')[0:2])
#         #     print(name)
#     #         print("name = ",name)
#             names.append(name)
#             i += 1
#             j += 2
#         except:
#                 break

    i,j = 0,2
    while i in range(len(rows)):
        try:
            price = rows[j][4]
#             price = price[i].text
#             print("price = ",price)
            flipPrices.append(price)
            i += 1
            j += 2
        except:
            break
    df = pd.DataFrame(list(zip(names, flipPrices)), 
               columns =['Product_name', 'Flipkart_price'])
    
    df.to_csv('test.csv')
    print(df)


data_file.close()


# In[4]:


flipPrices


# In[5]:


import pandas as pd
df = pd.read_csv("test.csv", sep=",")
df.head(100)


# In[6]:


print(len(names),len(flipPrices))
# flipPrices


# In[7]:


from bs4 import BeautifulSoup
import requests
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

flipkart=''
ebay=''
amazon=''
olx=''

amazonlist = []
amazonName = []
i = 0
while i in range(len(names)):
    print(names[i])
    def amazon(name):
            try:
                global amazon
                name = " ".join(name.split(' ')[0:2])
                name1 = name.replace(" ","-")
                name2 = name.replace(" ","+")
                amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
                res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
                print("\nSearching in amazon:")
                soup = BeautifulSoup(res.text,'html.parser')
                amazon_page = soup.select('.a-color-base.a-text-normal')
                amazon_page_length = int(len(amazon_page))
                for i in range(0,amazon_page_length):
                    name = name.upper()
                    amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                    if name in amazon_name[0:20]:
                        amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                        amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                        amazonlist.append(amazon_price)
                        print("Amazon:")
                        print(amazon_name)
                        amazonName.append(amazon_name)
                        print("₹"+amazon_price)
                        print("-----------------------")
                        break
                    else:
                        i+=1
                        i=int(i)
                        if i==amazon_page_length:
                            print("amazon : No product found!")
                            print("-----------------------")
                            amazon_price = '0'
                            amazonlist.append(amazon_price)
                            amazonName.append("No similar product")
                            break
                
                return amazon_price
            except:
                print("amazon: No product found!")
                print("-----------------------")
                amazon_price = '0'
                amazonlist.append(amazon_price)
                amazonName.append("No similar product")
            return amazon_price
    amazon_price = amazon(names[i])
    flipkart=''
    ebay=''
    croma=''
    amazon=''
    olx=''
    i += 1
flip = flipPrices
idk = []
for i in range(len(flip)):
#     x = 
    try:
        x = flip[i].text.replace('₹','')
        print(x)
        idk.append(x)
    except:
        idk = test
df = pd.DataFrame(list(zip(names,idk,amazonName, amazonlist)), 
               columns =["Product_name_Flipkart","Flipkart_price",'Product_name_Amazon', 'Amazon_price'])
    
df.to_csv('flipkartandamazon.csv')
df


# In[8]:


df = pd.DataFrame(list(zip(amazonName, amazonlist)), 
               columns =['Product_name', 'Amazon_price'])
    
print(df)
# len(amazonName)


# In[9]:


test = flipPrices


# In[10]:


flip = flipPrices


# In[11]:


idk = []


# In[12]:


flip = flipPrices
idk = []
for i in range(len(flip)):
#     x = 
    try:
        x = flip[i].text.replace('₹','')
        print(x)
        idk.append(x)
    except:
        idk = test


# In[13]:


# idk[0].replace('₹','')


# In[14]:


idk


# In[15]:


flip


# In[16]:


# len(flip)
amazonlist


# In[17]:


import csv
# opening the csv file in 'w+' mode

file = open('flipkartandamazon.csv', 'w+', newline ='')
# csv_data = pd.read_csv(csvpath,encoding='iso-8859-1')
# writing the data into the file
with file:    
    write = csv.writer(file)
    write.writerows(names)
    write.writerows(idk)
    write.writerows(amazonName)
    write.writerows(amazonlist)


# In[18]:


df = pd.DataFrame(list(zip(names,idk,amazonName, amazonlist)), 
               columns =["Product_name_Flipkart","Flipkart_price",'Product_name_Amazon', 'Amazon_price'])
    
df


# In[ ]:





# In[ ]:




