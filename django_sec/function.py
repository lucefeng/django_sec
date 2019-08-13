import socket
#import ping
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
        print(ip)
        ip=ip[0][4][0]
    except Exception as e:
        status = e
        return status
    port=port
    status="dier"
    sk_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk_connect.settimeout(1)
    try:
        sk_connect.connect((ip,port))
        status = "在线____"+" 主机ip地址是："+ip
    except Exception :
        status = "不在线____"+" 主机ip地址是："+ip
    sk_connect.close()
    return status