import requests
from bs4 import BeautifulSoup
import os
import shutil
import re

class Kaggle:
    __login_url__ = 'https://www.kaggle.com/account/login'

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        
        login_data = {'UserName': self.user, 
                    'Password': self.pwd  }
        self.s = requests.Session()
        self.s.post(Kaggle.__login_url__, data=login_data)
            
    def download_data(self, url, dir):
        
        # Before downloading the data, you must accept the rules. That can be
        # at link/rules.
        url_rules = url+'/rules'
        r = self.s.get(url_rules)
        soup = BeautifulSoup(r.text, 'lxml')
        token = soup.find('input', attrs = {'name' : '__RequestVerificationToken'})['value']
        post_data = { "__RequestVerificationToken" : token, "doAccept": "I understand and accept" }
        self.s.post(url_rules+'/accept', post_data)
        
    
        # Find a list of the files needed to be downloaded
        soup = BeautifulSoup(self.s.get(url+'/data/').text, 'lxml')
        data_files = soup('a', href = re.compile('/c/\S+/download'))
        data_files = map(lambda x : x.attrs['name'], data_files)
        
        # Download the files and save them into the directory dir
        for file in data_files:
            with open(os.path.expanduser(dir+'/'+file), 'wb') as f:
                r = self.s.get(url+'/download'+file, stream=True)
                shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":
    main()
