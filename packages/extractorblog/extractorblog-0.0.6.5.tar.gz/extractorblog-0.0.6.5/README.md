
# 文章提取

1. 提取文章标题
2. 提取文章内容
3. 转换成Markdown格式
4. 摘要提取（TODO）
5. 关键词提取（TODO）


```
示例：

import extractorblog

ua_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}
blog = extractorblog.get(url='https://statmodeling.stat.columbia.edu/2018/08/01/thanks-nvidia/', headers=ua_headers)

# 获取网页html内容
print(blog.getHtml)

# 获取网页标题
print(blog.getTitle)

# 获取网页主体html内容
print(blog.getBodyHtml)

# 获取网页主体markdown内容
print(blog.getMarkdown)
```
