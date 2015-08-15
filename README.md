pictureCompare python 视图服务
=============================================

### python 的第三方视图服务

* 1 当前版本的视图成功率并不理想,在如果内置的几个算法在不同类型的图片发挥不同(详情请看文档)
* 2 色彩对比在当前版本比较糟糕
* 2 单进程(可配置),所以如果需要高性能请使用mapreduce等工具


### 使用
* 首先配置好yaml文件 
* 请保证 redis正常运行...

```python
sudo pip install requirements.txt
```

### 运行

```shell
sudo service picturecompare start
sudo service picturecompare stop
```

欢迎大家PR
