import requests
import re
from  fake_useragent import UserAgent

#title, datail, replies
find_block =re.compile(r'<li class=" j_thread_list clearfix thread_item_box".*?</li>',re.S)
find_replies_num = re.compile(r'<span .*? title="回复">(.*?)</span>',re.S)
find_href_title = re.compile(r'<a rel="noopener" href="(.*?)" title=".*?" target="_blank" class="j_th_tit ">(.*?)</a>',re.S)
find_detail = re.compile(r'<div class="threadlist_abs threadlist_abs_onlyline ">(.*?)</div>',re.S)
find_replies =  re.compile(r'<div id=".*?" class="d_post_content j_d_post_content " style="display:;">(.*?)</div>',re.S)

def main():
    basesuffix = ["main", "hotthread", "album", "good", "video"]
    baseurl = "http://c.tieba.baidu.com/f?kw=弱智&ie=utf-8&tab="
    pageturn = {   
        "main": "https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA&ie=utf-8&pn=",
        "good": "https://tieba.baidu.com/f?kw=%E5%BC%B1%E6%99%BA&ie=utf-8&tab=good&cid=&pn="
    }
    page_pull_num = 3
    pullNum = 50 * (page_pull_num+1)

    # for suffix in basesuffix:
    #     url = baseurl+suffix
    #     html = askURL(url)
    #     with open(f'{suffix}.txt',"w",encoding="utf-8") as f:
    #         f.write(html)
    #     # for i in range(50,pullNum,50):
    #     #     pageturn_url = pageturn[suffix]+str(i)
    #     #     html = askURL(pageturn_url)
    #     #     with open(f'{suffix}.txt',"w",encoding="utf-8") as f:
    #     #         f.write(html)
    #     #     print("一页爬取结束")
    #     #只爬一页
    #     break       
    with open("main.txt","r",encoding="utf-8") as f:
        data = f.read()
    dataProcessed = dataProcess(data)
    print("处理结束")
    with open("mianProcessed.txt","w",encoding="utf-8") as f:
        f.write(dataProcessed)

def dataProcess (data):
    blocks = re.findall(find_block,data)
    dataProcessed = ""
    i = 0
    for block in blocks:
        i += 1
        href=re.search(find_href_title,block).group(1).replace(" ", "").replace("\n", "")
        title=re.search(find_href_title,block).group(2).replace(" ", "").replace("\n", "")
        detail=re.search(find_detail,block).group(1).replace(" ", "").replace("\n", "")
        replies_num=re.search(find_replies_num,block).group(1).replace(" ", "").replace("\n", "")
        replies = get_reply(href)
        dataProcessed += f"标题：{title}\n内容：{detail}\n回复数：{replies_num}\n回答:{replies}\n\n"
        if i == 5:
            break
    return dataProcessed

def get_reply(href):
    url="https://tieba.baidu.com"+href
    html = askURL(url)
    replies=re.findall(find_replies,html)
    replies = [reply.replace(" ", "").replace("\n", "") for reply in replies]
    replies = [re.sub(r'<.*?>','',reply) for reply in replies]
    replies = [reply for reply in replies if reply]
    return replies

def askURL (url):
    ua = UserAgent()
    head = {
        "User-Agent": ua.random
    }
    response = requests.get(url, headers=head)
    html = response.text
    return html

if __name__ == "__main__":
    main()
    print("爬虫结束")