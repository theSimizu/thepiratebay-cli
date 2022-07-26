# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import requests
from requests_html import HTMLSession

session = HTMLSession()

r = session.get(f'https://thepiratebay.org/search.php?q=batman&cat=0')
r.html.render(retries=2, timeout=15, sleep=4, keep_page=True, scrolldown=1)

cat = r.html.find('#cat')[0]

opts = cat.find('optgroup')

for opt in opts:
    options = opt.find('option')
    for option in options:
        # print(f'{option.text}: {option.attrs["value"]}')
        print(f"'{option.text}': {option.attrs['value']},")










# r = requests.get()


# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options = Options()
# driver = webdriver.Chrome(options=chrome_options)


# categories = {
#     'All': 0,

#     # Audio
#     'Music': 101,
#     'Audio Books': 102,
#     'Soundclips': 103,
#     'FLAC': 104,
#     'Other Audio': 199,

#     # Video
#     'Music': 101,
#     'Audio Books': 102,
#     'Soundclips': 103,
#     'FLAC': 104,
#     'Other Audio': 199,
    
# }


# search = input('Search\n> ')
# pirate = f'https://thepiratebay.org/search.php?q={search}&cat=0'

# driver.get(pirate)

# links = driver.find_elements(By.CLASS_NAME, 'list-entry')
