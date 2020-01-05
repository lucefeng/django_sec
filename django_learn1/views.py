from django.shortcuts import render
from django_learn1.models import *
from django_sec.function import *
from django_sec.ip_text import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
import requests
import PyPDF2
from django_sec.form import *
#import youtube_dl
#import pytube
#from django.shortcuts import redirect

# Create your views here.
per_num = 3 #每页显示的行数

def content(request):
    return render(request,"content.html")
def index(request):
    bookinfo = Comments_Note.objects.all() #Queryset对象？
    #print(type(bookinfo))
    #hello = {}
    #hello["kk"] = bookinfo
    info=page_index(1,per_num,bookinfo)
    if "input_email" in request.session :
        txt_filed="<a href=/logout title='注销'>"+request.session["input_email"]+"</a>"
    else:
        txt_filed="未登录"
    info["login_name"]=txt_filed
    if request.method == "POST" :
        if "input_email" in request.session and "input_psw" in request.session:
            input_email =request.session["input_email"]
            comments = request.POST['comments']
            if len(comments) >= 3 :#关联外键的必须以以下方式获取user表实例
                Comments_Note.objects.create(hname=User.objects.get(email=input_email),hcontent=comments)
                info["status"] = "评论成功了！"
                return render(request, "index.html", info)
            else:
                info["status"]="评论字数太少啦！"
                return render(request,"index.html",info)

        else:
            return render(request,"login.html",{"status":"需要登录"})

    return render(request,"index.html",info)
def page(request):
    bookinfo = Comments_Note.objects.all()
    info = page_index(request.path.split('_')[1], per_num, bookinfo)
    if "input_email" in request.session :
        txt_filed="<a href=/logout title='注销'>"+request.session["input_email"]+"</a>"
    else:
        txt_filed="未登录"
    info["login_name"]=txt_filed
    return render(request, "index.html", info)
def show(request,id):#暂时没用了
    bookinfo = BookInfo.objects.get(pk=id)
    heroinfo = bookinfo.heroinfo_set.all()
    context = {}
    context["list"]= heroinfo
    return render(request,"heroshow.html",context)

def login(request):
    if "input_email" in request.session and "input_psw" in request.session:
        return render(request,"content.html",{"status":"登陆过了"})

    if request.method == 'POST':
        input_email = request.POST["email"]
        input_psd = request.POST["pwd"]
        valid_code = request.POST["yzm"]
        if request.session["valid_code"].upper() == valid_code.upper():
            try:
                User.objects.get(email=input_email)
            except ObjectDoesNotExist:
                return render(request, "login.html", {'status': ' 无此用户'})
            else:
                try:
                    User.objects.get(password=input_psd,email=input_email)
                except ObjectDoesNotExist:
                    return render(request, "login.html", {'status': ' 密码错误'})
                else:
                    request.session["input_email"] = input_email
                    request.session["input_psw"] = input_psd
                    return render(request,"content.html",{"status":input_psd + input_email+request.session["valid_code"]})
        else:
            return render(request, "login.html", {'status': ' 验证码错误'})
        # if input_email == "1@1.com" and input_psd == "123":
        #     return redirect("http://www.baidu.com")
        # else:
        #     return render(request,"login.html",{'status':'ERROR Incorrect username or password'})
        #
        # return HttpResponse(input_psd+input_email)
    return render(request,"login.html")

def register(requset):
    if requset.method == 'POST':
        register_name = requset.POST['username']
        register_email = requset.POST['email']
        register_gender = requset.POST['gender']
        register_psw = requset.POST['pwd']
        register_pwd_check =requset.POST['pwd_check']
        # form表验证模式
        f = registerForm({'register_name':register_name,'register_email':register_email,'register_gender':register_gender,'register_psw':register_psw})
        #f =registerForm(requset.POST)
        if register_psw != register_pwd_check :
            return render(requset,'register.html',{"status":"密码不一致"})
        if f.is_valid() == False:
            return render(requset,'register.html',{"status":f.errors})
        try:
            User.objects.get(name=register_name)
            return render(requset, "register.html", {"status": "用户名重复"})
        except ObjectDoesNotExist:
            pass
        User.objects.create(name=register_name,password = register_psw,email = register_email,gender_sex = register_gender)
        return render(requset,"register.html",{"status":register_email+register_gender+register_name+register_psw})
    return render(requset,"register.html")

def get_valid_img(request):
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    width = 120
    height =27
    img_obj = Image.new('RGB', (width, height), get_random_color())

    draw_obj = ImageDraw.Draw(img_obj)
    font_obj = ImageFont.truetype("static/Font/arial.ttf",25)
    # #draw_obj.text()
    #
    #
    tmp_list =[]
    for i in range(5):
        u = chr(random.randint(65,90))#大写字母
        l = chr(random.randint(97,122))#lower letter
        n = str(random.randint(0,9)) #number
        temp_text = random.choice([u,l,n])
        tmp_list.append(temp_text)
        draw_obj.text((20+20*i,0),temp_text,fill=get_random_color(),font=font_obj)
    #保存到session
    request.session["valid_code"] = "".join(tmp_list)
    for i in range(5):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw_obj.line((x1,y1,x2,y2),fill=get_random_color())#干扰线
        draw_obj.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())#干扰点
        #干扰弧线
        draw_obj.arc((random.randint(0,width),random.randint(0,height),random.randint(0,width)+4,random.randint(0,height)+4),0,90,fill=get_random_color())


    io_obj = BytesIO()
    img_obj.save(io_obj, "png")
    data = io_obj.getvalue()
    return HttpResponse(data)


def delivery(request):#发送大iftt
    webbook_url = "https://maker.ifttt.com/trigger/{}/with/key/cTF4B4kBT-g0AhUxXHT0Cw"
    info ={}
    if request.method == "POST":
        smstext = request.POST['sms']
        #smstext ="iii"
        json_txt ={'value2':smstext}
        url = webbook_url.format('test_event')
        requests.post(url,json=json_txt)
        info['status']="发送成功"
        return render(request,"delivery.html",info)
    info['status_home'] = test_net('efeng.dynv6.net',5000)
    info['status_home_2'] = test_net('lucefeng.f3322.net', 5000)
    info['status_company'] = test_net('lucefeng.dynv6.net',5000)
    info['status_bwg'] = test_net('vess.goobeaf.xyz',80)
    info['status_alpha'] = test_net('efeng.us',80)
    return render(request,"delivery.html",info)


#注销
def logout(request):
    del request.session["input_email"]
    del request.session["input_psw"]
    #也可以用如下面的
    #request.session.flush()
    return render(request,"login.html")


#pdf读取页面
def pdf_read(request):
    #为什么同样下面这句就报错呢？？！！！需要的是一个文件对象 file("路径",'rb')才对或者一个字符串对象
    #with open('static/pic/test.pdf','rb') as pdf_read:
    pdf_filereader=PyPDF2.PdfFileReader(open('static/pic/America_beef.pdf','rb'))
    pdf_watermarkfilereader = PyPDF2.PdfFileReader(open('static/pic/watermark.pdf', 'rb'))
    #total_num=pdf_filereader.getNumPages()
    if request.session.get("pdf_num"):
        pdf_num=int(request.session["pdf_num"])-1
    else:
        pdf_num=0
    temp = pdf_filereader.getPage(pdf_num)
    temp.mergePage(pdf_watermarkfilereader.getPage(0))
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(temp)
    with open("temp.pdf",'wb') as pdf_filewrite:
        pdf_writer.write(pdf_filewrite)
    with open('temp.pdf','rb') as pdf_read:
        response=HttpResponse(pdf_read.read(),content_type='application/pdf')
        #response['Content-Disposition'] = 'inline;filename="extracted_page_{}.pdf"'.format(total_num)
    return response

def pdf_show(request):
    pdf_nownum=request.path.split("_")[1]
    request.session["pdf_num"]=pdf_nownum
    total_num=request.session["pdf_totalnum"]
    text=pdf_index(pdf_nownum,total_num)
    return render(request, "pdf_show.html", {"status":text})

def pdf_first(request):
    if not request.session.get("pdf_totalnum"):
        pdf_filereader = PyPDF2.PdfFileReader(open('static/pic/America_beef.pdf', 'rb'))
        request.session["pdf_totalnum"] = pdf_filereader.getNumPages()
    #pdf_filereader = PyPDF2.PdfFileReader(open('static/pic/America_beef.pdf', 'rb'))
    #total_num = pdf_filereader.getNumPages()
    #request.session["pdf_num"]=0
    text=["<a href=pdfshow_2>下一页</a>"]
    return render(request, "pdf_show.html", {"status": text})


def hours_ahead(request,offset):#直接取到url类似/home/2/中的2
    # try:
    #     offset = int(offset)
    # except ValueError:
    #     raise Http404()
    # #ip_text = get_log()
    # #ip_info1 = get_total_ip(ip_text, offset)
    # if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
    #ip = search_ip(str(re))
    # # for i in re :
    # #     yield {
    # #            'bianhao': i
    # #
    # #     }
    #ip=search_ip(re)
    # if ip != '':
    #     ip=ip[0]
    #files = read_dir_allfile("d")

    #yt = pytube.YouTube("https://www.youtube.com/watch?v=MFc1HmhI9v4&list=PLYiIZZiUKRvoe82viKKwkEbwaZgLpDUPy&index=2&t=1s")
    #txt = yt.streams.all()

    return HttpResponse("sdfsf")

    #return render(request, 'ip_show.html', {"ip_st": ip_info1})
    #return re



def return_form(request):
    t = "zhengc"
    if request.method == 'POST':
        f = ContactForm(request.POST)
        t=f.errors
    return  render(request,"test.html",{"status":t})


#ip检测网页
def ip_test(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    #把文件名放到session里
    if 'file_name' in request.session:
        fname = request.session['file_name']
    else:
        fname = "access.log"

    # 得到post的文件名
    if request.method == 'POST' :
        request.session['file_name'] = request.POST['file_name']
        fname = request.POST['file_name']
        #return HttpResponse(fname)
    ip_text =get_log(fname)
    ip_info1 = get_total_ip(ip_text,offset)
    #return HttpResponse(ip_info1)
    if request.META.__contains__('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    ip_info1['myip'] = get_ip_info(ip)
    global sys_dir
    files_name = read_dir_allfile(sys_dir)
    ip_info1['myfiles'] = files_name
    return render(request,'ip_show.html',ip_info1)






def proxy_read(request):
    welcome = "欢迎使用"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    if request.method == 'P0ST':
        url = request.POST["url"]

        response = requests.get(url, headers=headers)
        return render(request, "proxy_show.html", {'http': response.content})
    else:
        return render(request, 'proxy_show.html', {'http': welcome})

def proxy(request):
    welcome = "欢迎使用"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    if request.method == 'POST':
        if request.POST["url"] :
            url = request.POST['url']
            response = requests.get(url, headers=headers)
            welcome = change_src(response.content,str(url))
        else:
            welcome = "不能为空。"
    if request.method == 'GET':
        try:
            url = request.GET['url']
            response = requests.get(url, headers=headers)
            replace_html = change_src(response.content,str(url))
            welcome = replace_html
        except:
            welcome = "欢迎1"
    return render(request, 'proxy_show.html', {'http': welcome})