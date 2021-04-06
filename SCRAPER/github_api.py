from github import Github

ACCESS_TOKEN = "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"

g = Github(ACCESS_TOKEN)


def github_api(search_term , num_pages):

    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')


    query = '+'.join(search_term) 
    result = g.search_repositories(query)
 
    max_size = 10
    
    if result.totalCount > max_size:
        result = result[:max_size]

    for repo in result :
        print(repo)



if __name__ == '__main__':
    keywords = input('Enter keyword(s)[eg Python , Flask , Postgres]')
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    github_api(keywords , 1 )

