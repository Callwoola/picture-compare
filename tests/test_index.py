# coding:utf-8
import os
import json
import requests

class Index:
    target_url = "http://120.25.56.146:1565/_index"
    def index(self.id, name, image_url):
        post = {
            'query' : {
                'id'     : id,
                'name'   : name,
                'url'    : image_url,
                'search' : {
                },
                'data': {
                    'origin_url' image_url:,
                },
            }
        }
        payload = payload % (id, name, image_url, image_url)
        headers = {
            'content-type': "application/json",
        }
        response = requests.request(
            "POST",
            self.target_url,
            data=payload,
            headers=headers
        )
        print(response.text)

if __name__ == '__main__':
    # 请把本地图片上传到在线服务器
    # 并把对应内容填写到下面的变量
    # python main.py
    online_image_repo = 'http://online.app/images/'
    local_image_repo = '/Users/n/image_repo'
    img_list = os.listdir(path)
    capsule = Index()
    for i in img_list:
        capsule.index(img_list.index(i), i, online_repo_url + i)
