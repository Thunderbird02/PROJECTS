import requests
from bs4 import BeautifulSoup

Base_Url = "https://github.com/search?"
repo_names = []
repo_description = []
star_s = []
languages = []

def github_search(search_term):
    query = 'q='+ search_term
    page = requests.get(Base_Url + query)
    #Soup Object 
    soup = BeautifulSoup(page.content , 'html.parser') 
    #did this to get all the lists  
    repo_list = soup.find('ul' , class_ = 'repo-list')
    #getting elements from the repo_lists
    repo_descr = repo_list.find_all('p' , class_ = 'mb-1')
    #extract languages 
    stars = repo_list.find_all('a' , class_ ='Link--muted' )

    lang = repo_list.find_all('span' , {'itemprop' : True })

    manipulate_repo_list(repo_list , repo_descr , stars , lang)

def manipulate_repo_list(repo_list , repo_descr , stars  , lang):

     index = 0   
     description = repo_list.find_all('a' , class_ = 'v-align-middle')
     divs_tags = []
  
     for item in description:
         repo_names.append(item.text)

     for repo_desc_item in repo_descr:
         repo_description.append(repo_desc_item.text.strip())

     for x in stars :
         if len(x.get('class')) == 2:
             continue
         else:
             star_s.append(x.text)

     for language in lang :
         print(language.text)

         
if __name__ == "__main__":
    search_term = input("'Enter keyword(s)[e.g python, flask, postgres]:")
    github_search(search_term)

