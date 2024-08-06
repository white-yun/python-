import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 确保浏览器在无头模式下运行
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 初始化Chrome WebDriver
service = Service('D:\\chromedriver-win64\\chromedriver.exe')  # 请设置chromedriver的正确路径
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义URL
url = "https://helps.58.com/base/question?categoryId=0&from=1&siteId=5601&sourceType=58pc-zz-khbz&terminal=PC"

# 打开URL
driver.get(url)

# 等待页面加载
time.sleep(1)

# 定位主菜单的各个专区
sections = driver.find_elements(By.CSS_SELECTOR, '.treeNodeClose___1L0hR')  # 更新选择器

# 初始化字典以存储结果
results = {}
arr1=[]
arr2=[]
arr3=[]
arr4=[]
# 遍历每个专区并提取子菜单项
for section in sections:
    arr1.append(section.text)
    print("专区====",arr1)
    section.click()
    # time.sleep(2)  # 等待页面加载

    # 提取子菜单项
    # submenu_items = driver.find_elements(By.CSS_SELECTOR, '.treeNodeChildTitle___ZJqiJ')  # 更新选择器
    # for submenu in submenu_items:
    #     submenu_name = submenu.text
    #     print(submenu.text)
    #     # submenu.click()
    #     time.sleep(2)  # 等待页面加载
    #
    #     # 提取具体问题内容
    #     questions = driver.find_elements(By.CSS_SELECTOR, '.questionListUl___1J9ok li span')  # 更新选择器
    #     question_texts = [question.text for question in questions]
    #
    #     # 存储结果
    #     if section_name not in results:
    #         results[section_name] = {}
    #     results[section_name][submenu_name] = question_texts
    #
    #     # 返回上一级菜单
    #     driver.back()
    #     time.sleep(2)  # 等待页面加载
    #
    # # 返回主页
    # driver.get(url)
    # time.sleep(3)  # 等待页面加载
# 提取子菜单项
submenu_items = driver.find_elements(By.CSS_SELECTOR, '.treeNodeChildTitle___ZJqiJ')  # 更新选择器
for submenu in submenu_items:
    arr2.append(submenu.text)
    submenu.click()
    print("子菜单===",submenu.text)
    time.sleep(3)
    # 提取具体问题内容
    # questions_items = driver.find_elements(By.CSS_SELECTOR, '.questionListUl___1J9ok')  # 更新选择器
    questions_items = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.questionListUl___1J9ok li span'))  # 更新选择器
    )
    for question in questions_items:
        arr3.append(question.text)
        print("问题===",question.text)
        question.click()
        # time.sleep(5)
        # answer_items = driver.find_elements(By.CSS_SELECTOR, '.content___385ZG')  # 更新选择器
        # for answer in answer_items:
        #     print(answer.text)
        # time.sleep(5)
        # driver.execute_script("window.history.go(-1)")
        # time.sleep(3)
      # 等待页面加载
        # 提取问题的答案
        # try:
        #     answer = WebDriverWait(driver, 3).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, '.content___5WuKx'))  # 更新选择器
        #     )
        #     arr4.append(answer.text)
        #     print(answer.text)
        # except Exception as e:
        #     print(f"Error finding answer: {e}")
        # driver.back()
        # time.sleep(2)  # 等待页面加载



    # questions_items = driver.find_elements(By.CSS_SELECTOR, '.questionListUl___1J9ok li')  # 更新选择器
    # for questions in questions_items:
    #     arr3.append(questions.text)
    #     questions.click()
    #     # time.sleep(3)
    #     # answer_items = driver.find_elements(By.CSS_SELECTOR, '.content___5WuKx')  # 更新选择器
    #     # for answer in answer_items:
    #     #     print(answer.text)
    #     # time.sleep(2)
    # print(arr3)
    # # submenu.click()
    # time.sleep(2)  # 等待页面加载

# 关闭驱动程序
driver.quit()

# 显示结果
print(results)
