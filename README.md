# flask-blog

这是一个使用python的flask框架编写的多人博客网站

****
|Author|simonzhoup|
|---|---
|E-mail|simonzhoup@gmail.com

### 功能

* 注册/登录系统
* 个人信息设置、头像上传
* 用户动态展示
* 站内消息功能
* 用户关注系统/话题关注系统
* 博客包含技术问答板块和主题文章板块
* 文章评论
* 问答系统
* 文章标题和内容支持关键字搜索
* 响应式布局，支持移动设备
* 文章标签
* 简单的后台管理系统（完成中...


## 截图

### 主页
![](/Screenshots/index.png)
### 主题
![](/Screenshots/topic.png)
### 文章
![](/Screenshots/post.png)
### 文章列表
![](/Screenshots/posts.png)
### 新文章
![](/Screenshots/new.png)
### 问答
![](/Screenshots/qa.png)
### 问题
![](/Screenshots/q.png)
### 后台管理
![](/Screenshots/manage.png)


## 如何使用

* 创建数据库
```python
#项目使用Flask-Migrate扩展, 用来管理数据库
#创建迁移仓库
$ python manage.py db init

#自动创建迁移脚本
$ python manage.py db migrate -m "initial migration"

* 更新数据库
$ python manage.py db upgrade
```


## 启动程序
```python
$ python manage.py runserver
```


## 访问
浏览器打开 http://127.0.0.1:5000



### 其它

* [点击这里](http://ocooc.cc) 可以查看网站效果
