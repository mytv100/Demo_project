from selenium import webdriver
import json
import urllib.request
import os

# User-Agent를 통해 봇이 아닌 유저정보라는 것을 위해 사용
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/43.0.2357.134 Safari/537.36'}

dir_path = 'C:/Users/mytv1/PycharmProjects/Demo_project/movie/module/image/'
url_info = 'https://www.google.co.kr/search?'

# 파일 읽기
file = open('C:/Users/mytv1/PycharmProjects/Demo_project/movie/module/data/ml-100k/u.item', 'rb')
for line in file.readlines():

    string = line.decode('ISO-8859-1')
    string_list = string.split('|')
    movie = string_list[1]
    # 검색에 사용될 단어
    search_term = movie + 'movie poster'

    browser = webdriver.Chrome('C:/Users/mytv1/PycharmProjects/Demo_project/movie/module/chromedriver')
    # browser.implicitly_wait(3)
    url = 'https://www.google.com/search?q=' + search_term + '&tbm=isch'
    browser.get(url)

    # 디렉토리 명으로 사용하기 위해서 특수문자 제거
    movie = movie.replace(':', '_')
    movie = movie.replace('\\', '_')
    movie = movie.replace('/', '_')
    movie = movie.replace('*', '_')
    movie = movie.replace('?', '_')
    movie = movie.replace("'", '_')
    movie = movie.replace('"', '_')
    movie = movie.replace('|', '_')
    movie = movie.replace('<', '_')
    movie = movie.replace('>', '_')

    # 디렉토리 생성
    try:
        if not (os.path.isdir(dir_path + movie + '/')):
            os.makedirs(dir_path + movie + '/')
        else:
            continue
    except OSError as e:
        print('Failed to create directory!!!!!')
        raise

    # 이미지 카운트 (이미지 저장할 때 사용하기 위해서)
    counter = 0
    succounter = 0

    # div태그에서 class name이 rg_meta인 것을 찾아온다
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        # 3개까지만
        if counter == 3:
            break
        print('Total Count:', counter)
        print('Succsessful Count:', succounter)
        print('URL:', json.loads(x.get_attribute('innerHTML'))['ou'])

        # 이미지 url
        img = json.loads(x.get_attribute('innerHTML'))['ou']
        # 이미지 확장자
        imgtype = json.loads(x.get_attribute('innerHTML'))['ity']

        # 구글 이미지를 읽고 저장한다.
        try:
            req = urllib.request.Request(img, headers={'User-Agent': header})
            raw_img = urllib.request.urlopen(req.full_url)
            r = raw_img.read()
            File = open(dir_path
                        + movie + '/' + movie + '_' + str(counter) + '.' + imgtype, 'wb')
            File.write(r)
            File.close()
            succounter = succounter + 1
        except:
            print("can't get img")

        counter = counter + 1

    print(succounter, 'succesfully downloaded')
    browser.close()
