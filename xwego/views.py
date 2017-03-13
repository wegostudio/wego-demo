# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import sys
import os
import json
import settings

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(path))
import wego
from wego.buttons import *

w = wego.init(
    APP_ID=settings.WG_APP_ID,
    APP_SECRET=settings.WG_APP_SECRET,
    REGISTER_URL=settings.WG_REGISTER_URL,
    HELPER=settings.WG_HELPER,

    MCH_ID=settings.WG_MCH_ID,
    MCH_SECRET=settings.WG_MCH_SECRET,
    CERT_PEM_PATH=settings.WG_CERT_PEM_PATH,
    KEY_PEM_PATH=settings.WG_KEY_PEM_PATH,
    PAY_NOTIFY_PATH=settings.WG_PAY_NOTIFY_PATH,

    PUSH_TOKEN=settings.WG_PUSH_TOKEN,
    PUSH_ENCODING_AES_KEY=settings.WG_PUSH_ENCODING_AES_KEY,

    REDIRECT_PATH=settings.WG_REDIRECT_PATH,
    REDIRECT_STATE=settings.WG_REDIRECT_STATE,
    USERINFO_EXPIRE=settings.WG_USERINFO_EXPIRE,
    DEBUG=True,
)

w.create_menu(
    MenuBtn(
        u'示例',
        ViewBtn(u'Github', 'http://github.com/wegostudio')
    ),
    MenuBtn(
        u'互动按钮',
        ClickBtn(u'点击按钮', 'click msg1'),
        ScanBtn(u'扫码打开', 'scan_btn'),
        ClickBtn(u'扫码响应', 'click msg1')
    ),
    MenuBtn(
        u'互动按钮',
        PhotoBtn(u'选择图片', 'click msg1'),
        PhotoBtn(u'系统相机', 'click msg1'),
        PhotoBtn(u'微信相册', 'click msg1')
    )
)

@csrf_exempt
def index(request):
    push = w.analysis_push(request)
    user = w.get_ext_userinfo(push.from_user)
    reply = push.reply_text('hello ' + user.nickname)
    return HttpResponse(reply)

@w.login_required
def pay(request):
    # 微信公众号支付api
    import time
    order = 'ordernum' + str(int(time.time()))
    raw_html = json.dumps(w.unified_order(
        openid=request.wx_openid,
        body='test',
        out_trade_no= order,
        total_fee='1',
        spbill_create_ip='113.16.139.82',
        trade_type='JSAPI',
    ))

    return render(request, 'pay.html', {'data': raw_html})
