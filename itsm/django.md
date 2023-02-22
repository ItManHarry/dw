# 虚拟环境Conda
1. 安装&配置
    官网地址：https://conda.io/projects/conda/en/latest/user-guide/install/index.html
2. 常用命令
    2.1 查看版本：conda --version
    2.2 升级版本：conda update conda
    2.3 创建虚拟环境：conda create --name 'env-name' python=3.11 (指定虚机环境python版本)
    2.4 激活虚拟环境：conda activate 'env-name' 
    2.5 查看虚拟环境清单：conda info --envs
    网址：https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
# Django 4.0
## 安装（使用pip）
```bazaar
pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple
```    
## Django命令
1. 创建工程：
```bazaar
django-admin startprojects project-name
```
2. 工程文件目录

| 文件/目录         | 说明                                                                                                                                                                                     |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| manage.py     | A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py                     |
| pro-name(文件夹) | The inner pro-name/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. pro-name.urls). 
| pro-name/__init__.py| package remark                                                                                                                                                                         |
| pro-name/asgi.py|An entry-point for ASGI-compatible web servers to serve your project. See How to deploy with ASGI for more details.|
| pro-name/wsgi.py|An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.|
| pro-name/urls.py|The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.|
| pro-name/settings.py|Settings/configuration for this Django project. Django settings will tell you all about how settings work|