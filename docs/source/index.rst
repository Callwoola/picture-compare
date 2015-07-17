.. pictureCompare documentation master file, created by
   sphinx-quickstart on Tue Jul 14 09:35:20 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pictureCompare's documentation!
==========================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


index file
http://<server>:<port>/_index?type=json
{
    "query" : {
        "url" : "http://dmc-oss.yoozi.cn/images/f3f16faee39224fb36bcc871b67a305e.png@1e_400w_400h_1c_0i_1o_90Q_1x.jpg",
        "name" : "asdfasdf",
        "id" : "223"
    }
}

compare image
http://localhost:6666/_pc?type=json
{
    "query" : {
        "url" : "https://www.baidu.com/img/bd_logo1.png"
    }
}

upload
http://192.168.1.106:8888/_upload?type=data
{
    name : file_img
    body :data
}