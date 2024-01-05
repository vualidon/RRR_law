import requests
from bs4 import BeautifulSoup
import json

def get_page_content(url):
    """Get html from url"""
    page_content = requests.get(url)

    if page_content.status_code == 200:
        soup = BeautifulSoup(page_content.text, 'html.parser')

        item = {}
        # Get title
        title = soup.find('h1', class_='title')
        if title:
            item['title'] = title.text.strip()
        # Get content
        content = soup.find('section', id="news-content")
        if content:
            #get question
            question = content.find('strong', class_="sapo")
            if question:
                item['question'] = question.text.strip()
            #remove question
            question.extract()
            #remove div with id= "accordionMucLuc" from content
            accordion = content.find('div', id="accordionMucLuc")
            if accordion:
                accordion.extract()
            #get content
            item['content'] = content.text.strip()

        return item 
    else:
        print("Error when get page content")
        with open("./error.txt", "a", encoding="utf-8") as f:
            f.write(url + "\n")
        return {}

def get_content_from_major(major):
    # page = 0
    url = f"https://thuvienphapluat.vn/hoi-dap-phap-luat/{major}?page="
    for page in range(1,11):
        url = url + str(page)
        page_links = requests.get(url)
        soup = BeautifulSoup(page_links.text, 'html.parser')
        links = soup.find_all('a', class_='title-link')
        for link in links:
            print(link['href'])
            page_content = get_page_content(link['href'])
            if page_content != {}:
                with open("./data.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(page_content, ensure_ascii=False) + "\n")
            # break
        # break
        # page_content = get_html(url)

def get_content_from_category(category):
    url = f"https://thuvienphapluat.vn/hoi-dap-phap-luat/chu-de/{category}?page="
    for page in range(1,11):
        url = url + str(page)
        page_links = requests.get(url)
        soup = BeautifulSoup(page_links.text, 'html.parser')
        links = soup.find_all('a', class_='title-link')
        for link in links:
            print(link['href'])
            page_content = get_page_content(link['href'])
            if page_content != {}:
                with open("./data.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(page_content, ensure_ascii=False) + "\n")
        

# get_content_from_major("tien-te-ngan-hang")

majors = ['tien-te-ngan-hang', 'quyen-dan-su','chung-khoan', 'so-huu-tri-tue', 'tai-chinh-nha-nuoc',
          'thu-tuc-to-tung', 'the-thao-y-te', 'giao-thong-van-tai', 'xuat-nhap-khau', 'doanh-nghiep',
          'lao-dong-tien-luong', 'bat-dong-san', 'vi-pham-hanh-chinh', 'bao-hiem', 'van-hoa-xa-hoi',
          'thuong-mai', 'trach-nhiem-hinh-su', 'xay-dung-do-thi', 'ke-toan-kiem-toan', 'thue-phi-le-phi',
          'dau-tu', 'dich-vu-phap-ly', 'tai-nguyen-moi-truong', 'cong-nghe-thong-tin', 'giao-duc',
          'bo-may-hanh-chinh', 'linh-vuc-khac']

categories = ['kinh-doanh-van-tai', 'nghia-vu-quan-su', 'thua-ke', 'thue-gia-tri-gia-tang',
              'bien-so-xe', 'thu-tuc-ly-hon', 'che-do-thai-san', 'so-bao-hiem-xa-hoi', 'the-bao-hiem-y-te',
              'tro-cap-thoi-viec', 'muc-luong-toi-thieu', 'giam-tru-gia-canh', 'thoi-han-su-dung-dat',
              'giay-khai-sinh', 'vung-nuoc-cang-bien',  'ngach-cong-chuc']


# for major in majors:
#     get_content_from_major(major)

for category in categories:
    get_content_from_category(category)


    