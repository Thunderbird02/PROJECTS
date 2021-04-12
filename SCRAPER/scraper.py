#github_api imports
from github import Github
import requests
import json
import base64

#scrape imports
from bs4 import BeautifulSoup

Base_Url = "https://github.com/search?"
repo_names = []
repo_description = []
star_s = []
languages = []
issues = []
Last_updated = []
license_s = []


#github_api stuff
g = Github(per_page=10)

def github_api(search_term , num_pages = 1):

    List = []

    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        rate.reset
        return
   
    query = '+'.join(search_term) 
    result = g.search_repositories(query)
 
    max_size = 10
    count = 0
    
    if result.totalCount > max_size:
        result = result[:max_size]

    for repo in result :

        repo_names.append(repo.name)

        repo_description.append(repo.description)

        languages.append(repo.language)

        star_s.append(repo.stargazers_count)

        Last_updated.append(str(repo.updated_at))     

        try:
            license_s.append(repo.get_license().license.name)
        except:
            license_s.append('none')

    List = list_of_dicts_api()
    
    return List
    

def scrape_github(search_term , num_pages = 1):
    query = 'q='+ search_term
    page = requests.get(Base_Url + query)
    #Soup Object 
    soup = BeautifulSoup(page.content , 'html.parser')  
    repo_list = soup.find('ul' , class_ = 'repo-list')#repo list with items
    repo_descr = repo_list.find_all('p' , class_ = 'mb-1')#finding repo desciption
    stars = repo_list.find_all('a' , class_ ='Link--muted' )#stars 
    footer = repo_list.find_all('div' , class_ = 'd-flex flex-wrap text-small color-text-secondary')
    

    manipulate_repo_list(repo_list , repo_descr , stars  , footer)

def manipulate_repo_list(repo_list , repo_descr , stars , footer ):

    List = []

    index = 0   
    description = repo_list.find_all('a' , class_ = 'v-align-middle')
    divs_tags = []

    #extracting the repo names from the soup object
    repository_names(description)

    #extracting repo description from the soup object
    repository_description(repo_descr)
    
    #extracting number of stars from the soup object
    repository_stars(stars)
    
    #extracting languages from the soup object
    repository_languages(footer)

    #extracting number of issues
    repository_number_of_issues(footer)  

    #extracting last updated from the soup object
    repository_last_update(footer)

    List = list_of_dicts_scrape()

    print(List)


def repository_names(description):
    for item in description:
        repo_names.append(item.text)

def repository_description(repo_descr):
    for repo_desc_item in repo_descr:
        repo_description.append(repo_desc_item.text.strip())

def repository_stars(stars):
    for x in stars :
        if len(x.get('class')) == 2:
            continue
        else:
            star_s.append(x.text.strip())

def repository_languages(footer):
    for Item in footer :
        if len(Item.findChildren('div' , recursive = False)) >= 3:
            children = Item.find_all('div' , class_ ='mr-3')
            for child in children:
                language = child.find_all('span' , {'itemprop': True})
                if len(language) != 0:
                    languages.append(language[0].text)
        else:
            languages.append('none')

def repository_number_of_issues(footer):
    for _item in footer :
        if len(_item.findChildren('div' , recursive = False)) >= 3:
            number_of_issues = _item.find_all('a' , class_ = 'Link--muted f6')
            if len(number_of_issues) != 0 :
                issues.append(number_of_issues[0].text.strip())
            else:
                issues.append('none')
        else:
            issues.append('none')

def repository_last_update(footer):
    for item_ in footer :
        date_  = item_.find('relative-time' , class_ = 'no-wrap')
        Last_updated.append(date_.text)

def list_of_dicts_api():
    myList = []
   
    for   i    in    range(10):
        myList.append({'repo_name'  : str(repo_names[i]),
                      'description' : str(repo_description[i]),
                      'num_stars'   : str(star_s[i]),
                      'language'    : str(languages[i]),
                      'license'    : str(license_s[i]),
                      'last_updated': str(Last_updated[i]),
                      })

    return myList

def list_of_dicts_scrape():
    myList = []
   
    for   i    in    range(10):
        myList.append({'repo_name'  : str(repo_names[i]),
                      'description' : str(repo_description[i]),
                      'num_stars'   : str(star_s[i]),
                      'language'    : str(languages[i]),
                      'last_updated': str(Last_updated[i]),
                      'num_issues'  : str(issues[i])                      })

    return myList
           
if __name__ == "__main__":
    github  = False
    if github == True:
        keywords = input('Enter keyword(s)[eg Python , Flask , Postgres]')
        keywords = [keyword.strip() for keyword in keywords.split(',')]
        github_api(keywords , 1)
    else:
        keywords = input('Enter keyword(s)[eg Python , Flask , Postgres]')
        scrape_github(keywords , 1)
        
    
    






