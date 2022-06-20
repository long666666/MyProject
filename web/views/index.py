from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product


# Create your views here.
def index(request):
    """大堂点菜首页"""
    return redirect(reverse("web_index"))


def webindex(request):
    """大堂点菜首页"""

    # 从session中获取购物车信息
    cartlist = request.session.get('cartlist', {})
    # 初始化一个总金额
    total_money = 0

    # 遍历购物车中的信息，并累加总金额
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']

    request.session['total_money'] = total_money
    context = {"categorylist": request.session.get("categorylist", {}).items()}
    return render(request, "web/index.html", context)


def log_in(request):
    """大堂登录页面"""
    slist = Shop.objects.filter(status=1)
    context = {"shoplist": slist}
    return render(request, "web/login.html", context)


def do_login(request):
    """大堂登录页面"""
    try:
        # 选择店铺校验
        if request.POST['shop_id'] == "0":
            return redirect(reverse('web_log_in') + "?errinfo=1")

        # 执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            return redirect(reverse('web_log_in') + "?errinfo=2")

        # 根据登录账号获取登录者信息
        user = User.objects.get(username=request.POST['username'])
        # print(user.username)
        # print(user.password_hash)

        # 判断当前用户是否是管理员
        if user.status == 6:
            # 判断登录密码是否相同
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt  # 从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
            if user.password_hash == md5.hexdigest():  # 获取md5值
                print('登录成功')
                # 将当前登录成功的用户信息以webuser为key写入到session中
                request.session['webuser'] = user.toDict()

                # 获取当前店铺信息
                shopob = Shop.objects.get(id=request.POST['shop_id'])
                request.session['shopinfo'] = shopob.toDict()

                # 获取当前店铺中所有菜品信息
                cateob = Category.objects.filter(shop_id=shopob.id, status=1)

                categorylist = dict()  # 菜品种类字典
                productylist = dict()  # 菜品字典

                # 遍历菜品类别信息
                num = 1  # 用于菜品字典的键值
                for vo in cateob:
                    c = {"id": vo.id, "name": vo.name, 'pids': []}
                    plist = Product.objects.filter(category_id=vo.id, status=1)
                    # 遍历菜品类别下的菜品信息
                    for p in plist:
                        c['pids'].append(p.toDict())
                        productylist[num] = p.toDict()  # 菜品字典
                        num += 1
                    categorylist[vo.id] = c  # 菜品种类字典

                print("*" * 120)
                print("菜品信息", productylist)
                print("*" * 120)
                # 将上面的结果存入到session中
                request.session["categorylist"] = categorylist
                request.session["productlist"] = productylist

                # 重定向到后台管理首页
                return redirect(reverse("web_index"))
            else:
                return redirect(reverse('web_log_in') + "?errinfo=5")
        else:
            return redirect(reverse('web_log_in') + "?errinfo=4")
    except Exception as err:
        print(err)
        return redirect(reverse('web_log_in') + "?errinfo=3")


def log_out(request):
    """大堂登录页面"""
    del request.session['webuser']
    return redirect(reverse('web_log_in'))


def verify(request):
    """大堂登录页面"""
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 定义变量，用于画面的背景色、宽、高
    # bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    # font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
