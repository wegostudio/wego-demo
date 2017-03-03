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

@w.login_required
def index(request):

    return HttpResponse('Hello %s!' % request.wx_user.nickname)

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
