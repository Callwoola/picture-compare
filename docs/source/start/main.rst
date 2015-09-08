######################
开始使用
######################



安装python
---------------

是的需要安装python2.7*版本 ，并且依据readme.md 进行安装

开始使用
---------------

pictureCompare 是更具图片色彩直方图，以及汉明距离等算法加工而成的一个图片对比工具。

.. warning::

    内容有待完善，欢迎加入开发

安装好了后可在浏览器 打开::

    http://localhost:5555


查看演示demo。

====
使用api
====

url::

    http://<server>:<port>/_index?type=json


.. code::

    {
        "query" : {
            "url" : "https://www.baidu.com/img/bd_logo1.png",
            "name" : "store one",
            "id" : "1"
        }
    }

compare image url::

    http://<server>:<port>/_pc?type=json

.. code::

    {
        "query" : {
            "url" : "https://www.baidu.com/img/bd_logo1.png"
        }
    }


upload url::

    http://<server>:<port>/_upload?type=data

.. code::

    {
        name : file_img
        body :data
    }



mix upload and get json url::

    http://<server>:<port>/_mix?type=data

.. code::

    {
        name : file_img|file
        body :data
    }