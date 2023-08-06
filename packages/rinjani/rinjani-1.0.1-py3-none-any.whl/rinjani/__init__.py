

# python package to run machine learning tasks

__version__ = "0.0.3"
__author__ = "Connor Beard"
__all__ = ['yeet','google_news']


from datetime import datetime
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  


from bs4 import BeautifulSoup as bs
import re
import requests


def yeet():
    return('yeet indeed')
        




def google_news(query = '', driver_path = '', date = datetime.today(),binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):

    if driver_path == '':
        return('Must have chromedriver installed in a driver_path')
        
    a = query.split(' ')
    search = a[0]
    for word in range(1,len(a)):
        search += '+' + a[word]

    search = 'https://www.google.com/search?q='+search+'&biw=1342&bih=717&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'+str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year) + '%2Ccd_max%3A' + str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year) + '&tbm=nws'

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = binary_location
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)

    driver.get(search)
    webpage = driver.page_source

    soup = bs(webpage,'lxml')


    INVISIBLE_ELEMS = ('style', 'script', 'head', 'title')
    RE_SPACES = re.compile(r'\s{3,}')



    text = ' '.join([
        s for s in soup.strings
        if s.parent.name not in INVISIBLE_ELEMS
    ])

    
    a = RE_SPACES.sub(' ',text)

    b = np.array(a.split('...'))

    return b

    
