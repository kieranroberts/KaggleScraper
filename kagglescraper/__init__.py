import kagglescraper


"""
asdasd
"""

user = '<username>'
pwd = '<password>'
url = '<url for competition page>'
dir = '<directory to save data files>'

def main():
    kaggle = kagglescraper.Kaggle(user,pwd)
    kaggle.download_data(url,dir)
