import json
import requests
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup
df= pd.read_csv('Preat.com-product-links.csv')  
links = df['Links'].tolist()
links= links[:10]
class scrap:
    Title= []
    Seller_Platform= []
    Seller_SKU= []
    Manufacture_Name=[]
    Manufacture_Code=[]
    Packaging=[]
    Qty=[]
    Att_url=[]
    Product_Page_URL=[]
    Categories= []
    Sub_Categories=[]
    Description=[]
    Image_URL=[]
    Attributes= []
    uids=[]
    baseurl= 'https://www.preat.com'
    def __init__(self):
        for link in links:
            self.get_uids(link)
            self.parse(link)
            self.parse2(link)
        self.save_data()
    def get_uids(self,link):
        r= requests.get(link)
        bs = BeautifulSoup(r.content,'lxml')
        tag= bs.find('script', id="__NEXT_DATA__")
        resp= json.loads(tag.text)
        for i in resp['props']['pageProps']['product']['configurable_options'][0]['values']:
            self.uids.append(i['uid'])
    def parse(self,url):
        images=[]
        r= requests.get(url)
        bs = BeautifulSoup(r.content,'lxml')
        tag= bs.find('script', id="__NEXT_DATA__")
        resp= json.loads(tag.text)
#         print(resp)
        name = resp['props']['pageProps']['product']['name']
        price = resp['props']['pageProps']['product']['price_range']
        sku = resp['props']['pageProps']['product']['sku']
        image= resp['props']['pageProps']['product']['media_gallery']
        s_description = resp['props']['pageProps']['product']['short_description']
        l_description =resp['props']['pageProps']['product']['description']
        cat = resp['props']['pageProps']['product']['categories']
        for i in image:
            images.append(i['url'])
        self.Title.append(name)
#         data=resp['props']['pageProps']['product']
        self.Seller_Platform.append('Preat')
        self.Manufacture_Name.append('-1')
        self.Manufacture_Code.append('-1')
        self.Packaging.append('-1')
        self.Qty.append('-1')
        self.Sub_Categories.append('Misc')
        self.Attributes.append('-1')
        self.Product_Page_URL.append(r.url)
        self.Seller_SKU.append(sku)
        self.Categories.append(cat[0]['name'])
        self.Image_URL.append(images)
        bs= BeautifulSoup(l_description['html'],'lxml')
        descrip = bs.find('html')
        try:
            descrip= descrip.text
        except:
            descrip=''
        final_descript= descrip+s_description['html']
        self.Description.append(final_descript)
        bs =BeautifulSoup(r.content, 'lxml')
        try:
            attachment=bs.find('div',class_='product__description').find('a').get('href')
        except:
            attachment=''
        self.Att_url.append(self.baseurl+attachment)
    def parse2(self,link):
        sku= ''.join(self.Seller_SKU)
        image=[]
        for a in self.uids:
            url =f'https://www.preat.com/magento-shop-api?query=%0A++query+getConfigurableProduct%28%0A++++%24filter%3A+ProductAttributeFilterInput%0A++++%24configurableOptionValueUids%3A+%5BID%21%5D%0A++%29+%7B%0A++++products%28filter%3A+%24filter%29+%7B%0A++++++items+%7B%0A++++++++...+on+ConfigurableProduct+%7B%0A++++++++++__typename%0A++++++++++configurable_product_options_selection%28%0A++++++++++++configurableOptionValueUids%3A+%24configurableOptionValueUids%0A++++++++++%29+%7B%0A++++++++++++options_available_for_selection+%7B%0A++++++++++++++attribute_code%0A++++++++++++++option_value_uids%0A++++++++++++%7D%0A++++++++++++media_gallery+%7B%0A++++++++++++++url%0A++++++++++++++label%0A++++++++++++%7D%0A++++++++++++variant+%7B%0A++++++++++++++sku%0A++++++++++++++name%0A++++++++++++++price_range+%7B%0A++++++++++++++++minimum_price+%7B%0A++++++++++++++++++regular_price+%7B%0A++++++++++++++++++++...money%0A++++++++++++++++++%7D%0A++++++++++++++++%7D%0A++++++++++++++%7D%0A++++++++++++++price_tiers+%7B%0A++++++++++++++++final_price+%7B%0A++++++++++++++++++...money%0A++++++++++++++++%7D%0A++++++++++++++++quantity%0A++++++++++++++%7D%0A++++++++++++%7D%0A++++++++++%7D%0A++++++++%7D%0A++++++%7D%0A++++%7D%0A++%7D%0A%0A++%0A++fragment+money+on+Money+%7B%0A++++currency%0A++++value%0A++%7D%0A%0A&variables=%7B%22configurableOptionValueUids%22%3A%5B%22{a}%22%5D%2C%22filter%22%3A%7B%22sku%22%3A%7B%22eq%22%3A%22{sku}%22%7D%7D%7D'
            r= requests.get(url)
            r2= requests.get(link)
            bs = BeautifulSoup(r2.content,'lxml')
            tag= bs.find('script', id="__NEXT_DATA__")
            resp= json.loads(tag.text)
            data= json.loads(r.content)
            s_description = resp['props']['pageProps']['product']['short_description']
            l_description =resp['props']['pageProps']['product']['description']
            cat = resp['props']['pageProps']['product']['categories']
            bs= BeautifulSoup(l_description['html'],'lxml')
            descrip = bs.find('html')
            try:
                descrip= descrip.text
            except:
                descrip=''
            final_descript= descrip+s_description['html']
            self.Description.append(final_descript)
            try:
                images= data['data']['products']['items'][0]['configurable_product_options_selection']['media_gallery']
                self.Image_URL.append(images)
            except:
                pass
            try:
                name= data['data']['products']['items'][0]['configurable_product_options_selection']['variant']['name']
                self.Title.append(name)
            except:
                print(url)
                pass
            try:    
                sku = data['data']['products']['items'][0]['configurable_product_options_selection']['variant']['sku']
                self.Seller_SKU.append(sku)
            except:
                print(url)
                pass
           
            
            self.Seller_Platform.append('Preat')
            self.Manufacture_Name.append('-1')
            self.Manufacture_Code.append('-1')
            self.Packaging.append('-1')
            self.Qty.append('-1')
            self.Sub_Categories.append('Misc')
            self.Attributes.append('-1')
            self.Product_Page_URL.append(r2.url)
            
            self.Categories.append(cat[0]['name'])
#             self.Image_URL.append(images)
            bs =BeautifulSoup(r.content, 'lxml')
            try:
                attachment=bs.find('div',class_='product__description').find('a').get('href')
            except:
                attachment=''
            self.Att_url.append(self.baseurl+attachment)


            
    
    def save_data(self):
        data_dict={"Seller Platform":self.Seller_Platform, "Seller SKU":self.Seller_SKU, "Manufacture":self.Seller_Platform,"Manufacture Code":self.Seller_SKU,
          "Product Title":self.Title,"Description":self.Description, "Packaging":self.Packaging,"Categories":self.Categories, "Subcategories":self.Sub_Categories,
           "Product Page URL":self.Product_Page_URL,"Attachment URL":self.Att_url[0],"Image URL":self.Image_URL, "Attributes":self.Attributes }
        df= pd.DataFrame.from_dict(data_dict)
#         print(data_dict)
#         df.to_csv("Preat-Sample-data.csv", index=False)
        
        


if __name__ =='__main__':
    scrap=scrap()