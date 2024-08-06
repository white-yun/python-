import json
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session():
    session = requests.Session()  # 创建一个新的会话对象
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])  # 配置重试策略
    session.mount('http://', HTTPAdapter(max_retries=retries))  # 对 HTTP 请求使用重试策略
    session.mount('https://', HTTPAdapter(max_retries=retries))  # 对 HTTPS 请求使用重试策略
    return session  # 返回配置好的会话对象


def fetch_category_ids(url):
    """从接口获取所有 categoryId。"""
    data = {
        'categoryId': 0,
        'pageNum': '1',
        'pageSize': '10',
        'siteId': '5601',
        'terminal': 'PC',
        'sourceType': '58pc-zz-khbz'
    }
    session = create_session()
    try:
        response = session.post(url, data=data, timeout=10)
        response.raise_for_status()  # 确保请求成功
        requestsData = response.json()
        return [item2['categoryId'] for item in requestsData['data']['categoryList']
                if item.get('childList')
                for item2 in item['childList']]
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

def fetch_content_ids(url, categoryId):
    """根据 categoryId 从接口获取所有 contentId。"""
    data = {
        'categoryId': categoryId,
        'pageNum': '1',
        'pageSize': '10',
        'siteId': '5601',
        'terminal': 'PC',
        'sourceType': '58pc-zz-khbz'
    }
    session = create_session()
    try:
        response = session.post(url, data=data, timeout=10)
        response.raise_for_status()  # 确保请求成功
        requestsData1 = response.json()
        return [item['contentId'] for item in requestsData1['data']['contentList']]
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

def fetch_details(url, content_ids):
    """根据 content_ids 从接口获取详细信息。"""
    results = []
    session = create_session()
    for content_id in content_ids:
        payload2 = {
            'contentId': content_id,
            'siteId': '5601',
            'terminal': 'PC',
            'pageType': '',
            'searchId': '',
            'recommendId': ''
        }
        try:
            response2 = session.post(url, data=payload2, timeout=10)
            response2.raise_for_status()  # 确保请求成功
            data2 = response2.json()

            result = {
                'instruction': data2['data']['title'],
                'input': '',
                'output': data2['data']['richText']
            }
            print(result)
            results.append(result)
        except requests.RequestException as e:
            print(f"请求失败: {e}")
    return results

def save_results(results, file_path='output_data_temp.json'):
    """将结果保存到 JSON 文件中。"""
    try:
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        print("现有文件内容不是有效的 JSON，使用空列表作为替代")
                        existing_data = []
            else:
                existing_data = []
        else:
            existing_data = []

        combined_data = existing_data + results

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=4)

        print("数据已追加到 'output_data_temp.json'")
    except IOError as e:
        print(f"文件操作失败: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解码失败: {e}")

def main():
    url1 = 'https://helps.58.com/listpage/gdwt/query/pc'
    url2 = 'https://helps.58.com/detailpage/rule'

    categoryIdList = fetch_category_ids(url1)
    print(categoryIdList)
    # [3432, 3433, 3434, 3435, 4015, 4017, 4053]
    for categoryId in categoryIdList:
        content_ids = fetch_content_ids(url1, categoryId)
        print(content_ids)
        results = fetch_details(url2, content_ids)
        save_results(results)

if __name__ == '__main__':
    main()
