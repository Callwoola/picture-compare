pictureCompare python 识图服务(类似于google识图搜索)
=============================================

### python 的第三方识图服务

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python server.py
```

安装配置 redis (使用redis 作为指纹缓存数据)


配置 config.yaml

```yaml
redis:
  host: 192.168.10.10
  port: 6379
  db: 1

```

开始使用：

```bash
$ python server.py
```


