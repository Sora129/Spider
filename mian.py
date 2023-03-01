from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EgdeService
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv


def find_title(d):
    title = d.find_elements(By.XPATH, '//*/div/h3/a')
    final_title = []
    for i in title:
        final_title.append(i.text)
    return final_title
    pass


def find_content(driver):
    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")
    content = soup.find_all('div', class_="result-op c-container xpath-log new-pmd")
    content_3 = []
    content_4 = []
    url_list= []
    data = []
    for i in range(2,len(content)+2):
        st = "/html/body/div/div[3]/div[1]/div[4]/div[{}]/div/h3/a".format(i)
        logo_1 = driver.find_element(By.XPATH, st)
        ActionChains(driver).click(logo_1).perform()
        driver.switch_to.window(driver.window_handles[2])
        url = driver.current_url
        url_list.append(url)
        element = driver.find_elements(By.XPATH, '//p')
        for j in element:
            content_2 = j.text
            content_3.append(content_2)
        s =''.join(content_3)
        s.strip()
        content_4.append(s)
        content_3.clear()
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
    data.append(content_4)
    data.append(url_list)
    return data
    pass


def find_or(driver):
    origin = driver.find_elements(By.XPATH, '//*/div/div/div/div/a/span[@aria-label]')
    final_origin = []
    for i in origin:
        final_origin.append(i.text)
    return final_origin
    pass

def check(url):
    flage = 1
    with open(file='./data.csv', mode='r+', encoding='utf-8', newline='') as f:
        f_reader = csv.DictReader(f)
        for i in f_reader:
            c = i['网址']
            if c == url:
                flage = 0
                break
    return flage
    pass

def main():
    print("输入搜索内容:", end='')
    name = str(input())
    print("输入爬取的页数:", end='')
    page_num = eval(input())
    option = webdriver.EdgeOptions()
    location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    option.binary_location = location
    service = EgdeService(executable_path='./edgedriver_win32/msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=option)
    driver.get("https://www.baidu.com/")
    logo1 = driver.find_element(By.XPATH,'//*[@id="s-top-left"]/a[1]')
    ActionChains(driver).click(logo1).perform()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH, "//input[contains(@id,'ww') and contains(@class,'word')]").send_keys(name)
    logo2 = driver.find_element(By.XPATH,'//*[@id="s_btn_wr"]')
    ActionChains(driver).click(logo2).perform()
    for i in range(page_num):
        list_1 = find_title(driver)
        list_2 = find_or(driver)
        list_3 = find_content(driver)[1]
        list_4 = find_content(driver)[0]
        row = []
        for i in range(len(list_1)):
            row.append(list_1[i])
            row.append(list_2[i])
            row.append(list_3[i])
            row.append(list_4[i])
            num_0 = check(row[2])
            if num_0 == 1:
                with open(file='./data.csv', mode="a+", encoding='utf-8', newline='') as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(row)
            row = []
        next = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/a[text()='下一页 >']")
        ActionChains(driver).click(next).perform()
    driver.quit()


if __name__ == '__main__':
    header = ['标题', '来源', '网址', '内容']
    with open(file='./data.csv', mode="a+", encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
    main()
