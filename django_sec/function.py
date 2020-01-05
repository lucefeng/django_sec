import socket
#import ping
import os
from bs4 import BeautifulSoup
from django_sec.ip_text import get_ip_info
def page_index(index_num,page_total,data):
    index_num_in=int(index_num)
    page_total_in = page_total # 每页显示行数
    start = page_total_in*(index_num_in-1)
    end = page_total_in*index_num_in
    data_in = data[start:end]
    end_num=int(len(data)/index_num_in+1)
    text = []
    if index_num_in <= 1:
        if len(data)/page_total_in <= 1 :
            text.append("")
        else:
            text.append("<a href=page_%s>下一页</a>" % (index_num_in+1))
    elif index_num_in >end_num:
        index_num_in = end_num
        text.append("<a href=page_%s>上一页</a>"%(index_num_in))
        #text.append("<a href=page_%s>下一页</a>"%(index_num_in+1))
    else:
        text.append("<a href=page_%s>上一页</a>" % (index_num_in - 1))
        text.append("<a href=page_%s>下一页</a>" % (index_num_in + 1))
    return {"info":data_in,"page_no":text}

def pdf_index(pdf_nownum,total_num):
    text = []
    pdf_nownum=int(pdf_nownum)
    total_num-int(total_num)
    if pdf_nownum >= total_num:
        pdf_nownum =total_num
        text.append("<a href=pdfshow_%s>上一页</a>" % (pdf_nownum - 1))
    elif pdf_nownum == 1 :
        text.append("<a href=pdfshow_%s>下一页</a>" % (pdf_nownum + 1))
    else:
        text.append("<a href=pdfshow_%s>上一页</a>" % (pdf_nownum - 1))
        text.append("<a href=pdfshow_%s>下一页</a>" % (pdf_nownum + 1))
    return text
#测试网络连通性
def test_net(addr,port):
    status= "测试中。。。"
    try:
        ip=socket.getaddrinfo(addr,'http')
        #print(ip)
        ip=ip[0][4][0]
    except Exception as e:
        status = e
        return status
    port=port
    status="dier"
    sk_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk_connect.settimeout(1)
    ip_info = get_ip_info(ip)
    try:
        sk_connect.connect((ip,port))
        status = "在线____"+" 主机ip地址是："+"     国家是："+ip_info['国家']+"。。。城市是：  "+ip_info['城市']
    except Exception :
        status = "不在线____"+" 主机ip地址是："+"    国家是："+ip_info['国家']+"。。。城市是：   "+ip_info['城市']
    sk_connect.close()
    return status


# 读取目录下文件
def read_dir_allfile(path):
    #path = r"D:\work-program\vscode"
    files= os.listdir(path)
    files_name =[]
    key = "access"
    for file in files:
        #print(os.path.splitext(file))
        if key in file and not file.endswith('.gz'):
            files_name.append(str(file))
    return files_name


#替换html中的a标签 href
def change_src(content,url):
    pre_http ="http://127.0.0.1:8000/proxy?url="
    pre_http_efeng = "http://www.efeng.us/proxy?url="
    soul = BeautifulSoup(content,'lxml')
    urls = soul.find_all('a')
    url_origin = url
    for url in urls:
        if url.get('href'):
            url_txt = url.get('href')
            if 'http' in url_txt :
                url['href'] = pre_http_efeng+url_txt
            else:
                url['href'] = pre_http_efeng+url_origin+url_txt
        else:
            url['href'] = '#'
    return str(soul)

#判断网址，去掉不该有的东东
def remove_something():
    pass


