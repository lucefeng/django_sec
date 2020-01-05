from bs4 import BeautifulSoup
import requests
#周排行网址
url="https://javdb2.com/rankings/video_weekly"
def get_html(url):
    try:
        html=requests.get(url).text
        #print(html)
    except:
        print("errors")
    return html
def get_girl_main_info(url):
    html = get_html(url)
    soul = BeautifulSoup(html,'lxml')
    index_urls=soul.find_all(class_="grid-item column")
    movie_info = {}
    for x in index_urls:
        #print(x.find('a').get('href'))
        #print(x.find('a').get('title'))
        #print(x.find('a').find('img').get('src'))
        #print(x.find('a').find(class_='uid').string)
        #key 是 车牌号,value 是 标题 详细页地址 缩略图地址
        movie_info[x.find('a').find(class_='uid').string] = [x.find('a').get('title'),x.find('a').get('href'),x.find('a').find('img').get('src')]
        #temp = x.contents
#       #temp = "".join(temp.split(r'\n'))
        #print(movie_info)
    return movie_info

def get_more_info(girl_url):
    girl_info = {}
    html = get_html('https://javdb2.com/v/'+girl_url)
    soul = BeautifulSoup(html,'lxml')
    girl_info['image_url'] = soul.find(class_='column column-video-cover').find('img').get('src')
    girl_info['video_url'] = soul.find(class_='column column-video-cover').find('source').get('src')
    girl_info['video_chepaihao'] = soul.find(class_='button copy-to-clipboard').get('data-clipboard-text')
    urls = soul.find_all(class_='panel-block')
    for url in urls:
        try:
            title = url.find('strong').string
            print(title)
            txt_temp = str(url.find(class_='value').contents)
            txt_temp = txt_temp.replace(r',\xa0', '')
            print(txt_temp)
        except Exception as e:
            print(e)
    girl_urls = soul.find(class_='tile-images preview-images').find_all('a')
    for girl_image_url in girl_urls:
        print(girl_image_url.get('href'))
print(get_girl_main_info(url))
