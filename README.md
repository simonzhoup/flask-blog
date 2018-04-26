<h2>flask-blog</h2>
<p>一个基于 Flask 的多人博客</p>

<h3>使用步骤</h3>
因为已包含最新的迁移脚本，建立好正确的数据库后，只需upgrade更新即可。
<pre>
<code>
$ pip install -r requirements.txt
#然后在MySQL中手动建立一个名为weblog的数据库
$ python manage.py db upgrade
$ python manage.py runserver 
</code>
</pre>

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
* ......


### 其它

* [点击这里](http://ocooc.cc) 可以查看网站效果
