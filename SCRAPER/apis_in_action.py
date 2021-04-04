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
    #footer containing many elements
    footer = repo_list.find_all('div' , class_ = 'd-flex flex-wrap text-small color-text-secondary')
    

    manipulate_repo_list(repo_list , repo_descr , stars  , footer)

def manipulate_repo_list(repo_list , repo_descr , stars , footer ):

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

    print()
    print('Licence starts ')
    #Licence 
    for ITEM in footer :
        if len(ITEM.findChildren('div' , recursive = False)) >= 3:
   
            Children = ITEM.findChildren('div' , recursive = False)
                         
       
    print('language starts')
    #Language
    for Item in footer :
        if len(Item.findChildren('div' , recursive = False)) >= 3:
            children = Item.find_all('div' , class_ ='mr-3')

            for child in children:
                language = child.find_all('span' , {'itemprop': True})
                if len(language) != 0:
                    print(language[0].text)
        else:
            print('none ' +  ' ')

    #language has been debugged it works nicely         

    print()
    print('Number_Of_Issues')
    #Number_Of_Issues
    for _item in footer :
        if len(_item.findChildren('div' , recursive = False)) >= 3:
            number_of_issues = item.find('a' , class_ = 'Link--muted f6')
            print(number_of_issues.text)
            print()
        else:
            print(' none ' + ' ')

        print()
        print('Last Updated')
       #Last Updated 
    for item_ in footer :
        date_  = item_.find('relative-time' , class_ = 'no-wrap')
        print('Updated on ' + date_.text )

             
if __name__ == "__main__":
    search_term = input("'Enter keyword(s)[e.g python, flask, postgres]:")
    github_search(search_term)






