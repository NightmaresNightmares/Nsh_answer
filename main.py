import base64
import urllib
import requests
import json
import tkinter as tk
import io
import base64
from PIL import ImageGrab

#OCR密钥
API_KEY = "*****"
SECRET_KEY = "*****"
#AI密钥
API_KEY2 = "*****"
SECRET_KEY2 = "*****"


def main():


    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis?access_token=" + get_access_token()
    jpgbase64 = get_file_content_as_base64("D:\\cc.png", True)
    #print(jpgbase64)
    # image 可以通过 get_file_content_as_base64("C:\fakepath\微信截图_20250108075925.png",True) 方法获取
    payload = f'image={jpgbase64}&detect_language=false&detect_direction=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'

    }

    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))

    _data_json=response.text
    parsed_data = json.loads(_data_json)  # 将JSON字符串转换为字典
    word_content = parsed_data["results"][0]["words"]["word"]
    print(word_content)

    #print(response.text)






    tw_url2 = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token2()

    tw_payload2 = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"{word_content}"
            }
        ],
        "temperature": 0.95,
        "top_p": 0.8,
        "penalty_score": 1,
        "enable_system_memory": False,
        "disable_search": False,
        "enable_citation": False
    })
    tw_headers2 = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xxxxxxx'  #这里填入百度云Bearer密钥
    }

    response2 = requests.request("POST", tw_url2, headers=tw_headers2, data=tw_payload2)

    #print(response2.text)

    _data_json2 = response2.text
    parsed_data2 = json.loads(_data_json2)  # 将JSON字符串转换为字典
    word_content = parsed_data2["result"]
    print(word_content)


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_access_token2():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY2, "client_secret": SECRET_KEY2}
    return str(requests.post(url, params=params).json().get("access_token"))

def save_clipboard_image_to_file(filename):
    """
    保存剪贴板中的图像到指定文件
    :param filename: 图像保存的文件名及路径
    """
    # 从剪贴板获取图像数据
    image = ImageGrab.grabclipboard()

    if image is not None:
        # 如果剪贴板中有图像，则保存
        image.save(filename)
        print(f"图像已保存至：{filename}")
    else:
        print("剪贴板中没有图像数据。")


if __name__ == '__main__':
    save_path = "D:\\cc.png"
    save_clipboard_image_to_file(save_path)
    main()

