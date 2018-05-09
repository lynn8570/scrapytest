# 创建项目

```
#创建项目后，在终端进入项目录入
# source venv/bin/activate 来激活环境，最前面出现 (venv)
# (venv) zowee-laiscdeMacBook-Pro:scrapytest zowee-laisc$ pip install Scrapy 然后安装Scrapy
```

> 激活虚拟环境后，如果要退出活着删除可以使用如下命令
>
> **退出虚拟环境**$
>     deactivate
> **删除虚拟环境**
>     rm -r venv

创建scrapy项目 `scrapy startproject tutorial`

```
(venv) zowee-laiscdeMacBook-Pro:scrapytest zowee-laisc$ scrapy startproject tutorial
New Scrapy project 'tutorial', using template directory '/Users/zowee-laisc/lynn/pycharmProject/scrapytest/venv/lib/python3.6/site-packages/scrapy/templates/project', created in:
    /Users/zowee-laisc/lynn/pycharmProject/scrapytest/tutorial

You can start your first spider with:
    cd tutorial
    scrapy genspider example example.com
```

# 示例

1. ## 生成爬虫类

   生成一个spider爬虫类 scrappy genspider spiderName xxxxdomain

   会在spider文件夹下生成一个 spiderXXX.py文件

   示例：爬一下公司内网的buglist

   ​

2. ## 定义item字段

   定义我们要处理哪些数据在 items.py文件中添加如下定义

   ```
   import scrapy
   class ChandaoItem(scrapy.Item):
       # define the fields for your item here like:
       #bug title
       title = scrapy.Field()
       #严重等级
       severity = scrapy.Field()
       #bug 发现者
       founder = scrapy.Field()
       #当前责任人
       current = scrapy.Field()
   ```

   ​

3. ## 登录数据

   一般网站都要账号密码登录流程

   在进入请求的时候，将用户数据封好后，再返回给引擎，要求请求完成后由after_login来处理。

   在after_login中在重新请求到我们需要爬取的页面，这个时候，已经是登录状态了，然后再将请求后的数据交给parse_buglist处理

   ```
   def parse(self, response):
           return scrapy.FormRequest.from_response(
               response,
               formdata={'account':'linlian','password':'XXXX'},
               callback = self.after_login
           )
   def after_login(self,response):
           print("after......")
           print(response.xpath('//script').extract()[0])
           #with open("body.txt", 'wb') as f:
           #    f.write(response.body)
           #b"<script>parent.location='/zentao/index.html';\n\n</script>\n"
           return scrapy.Request('http://192.168.2.27/zentao/bug-browse-21.html',
                                 callback= self.parse_buglist)
                                 
                                 
   ```

   ​

4. ## 页面解析

   拿到页面数据后，通过xpath拿到我们需要的节点，进行迭代解析我们需要的数据，然后通过页面分析拿到需要进一步请求的连接地址

   ```
    def parse_buglist(self,response):
           print("parse_buglist")


           node_list = response.xpath("//tr[@class='text-center']")
           for node in node_list:
               item =  ChandaoItem()
               item['severity'] = node.xpath("./td[2]/span/text()").extract()[0]
               item['title'] = node.xpath("./td[4]/a/text()").extract()[0]
               item['founder'] = node.xpath("./td[5]/text()").extract()[0]
               item['current'] = node.xpath("./td[6]/text()").extract()[0]
               yield item

           try:
               url = response.xpath("//i[@class='icon-play']/../@href").extract()[0]
               print(url)
               if len(url) !=0:
                   yield      scrapy.Request('http://192.168.2.27'+url,callback=self.parse_buglist)
           except IndexError:
               print("Get next Error")
   ```

   ​

5. ## 数据保存

   运行爬虫 `scrapey crawl Buglist -o items.json` 并将结果保存在 items.json





