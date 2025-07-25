
from bs4 import BeautifulSoup

def parse_html_file(filepath):
    usernames = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        for a_tag in soup.find_all('a', target='_blank'):
            href = a_tag.get('href')
            if href and 'instagram.com' in href:
                username = href.split('/')[-1]
                usernames.add(username)
    return usernames

following_users = parse_html_file('/home/ubuntu/upload/following.html')
followers_users = parse_html_file('/home/ubuntu/upload/followers_1.html')

not_following_back = following_users - followers_users

if not_following_back:
    print("As seguintes pessoas que você segue NÃO te seguem de volta:")
    for user in sorted(list(not_following_back)):
        print(user)
else:
    print("Todas as pessoas que você segue te seguem de volta!")


