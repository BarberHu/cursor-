from django.shortcuts import render, HttpResponse
import os
import time
import json
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .pyneo_utils import *
from django.views.decorators.csrf import csrf_exempt
import jieba
from .models import MyNode, MyWenda
from django.conf import settings
# Create your views here.
from django.conf import settings


@login_required
def index(request):
    try:
        start = request.GET.get("start", "")
        relation = request.GET.get("relation", "")
        end = request.GET.get("end", "")
        all_datas = get_all_relation(start, relation, end)
        
        # 确保数据不为空
        links = json.dumps(all_datas.get("links", []))
        datas = json.dumps(all_datas.get("datas", []))
        categories = json.dumps(all_datas.get("categories", []))
        legend_data = json.dumps(all_datas.get("legend_data", []))

        print("Data to render:", {
            "links": links,
            "datas": datas,
            "categories": categories,
            "legend_data": legend_data
        })
    except Exception as e:
        print("Error in index view:", e)
        links, datas, categories, legend_data = "[]", "[]", "[]", "[]"
    
    return render(request, "index.html", locals())

@login_required
def wenda(request):
    try:
        user = request.user

        if request.method == "GET":
            key = request.GET.get("key", "")
            clean = request.GET.get("clean", "")
            if clean:
                all_wendas111 = MyWenda.objects.filter(user=user).order_by("id")
                print(all_wendas111)
                for js in all_wendas111:
                    js.delete()
            daan = ''
            if key.lower() in {'你好', '您好', 'hello', '你好！'}:
                daan = '你 好 👋 ！ 我 是 您 的 地 理 建 模 小 助 手 ！ 很 高 兴 见 到 你 ， 欢 迎 问 我 任 何 有 关 地 理 建 模 的 问 题 。'
            elif key:
                res_classify = settings.CLASSIFIER.classify(key)
                final_answers = []

                if res_classify:
                    res_sql = settings.PARSER.parser_main(res_classify)
                    final_answers = settings.SEACHER.search_main(res_sql)

                daan = '\n'.join(
                    final_answers if final_answers
                    else settings.ZHIPU.get_chatglm_response(key)
                )

            if daan:
                wenda = MyWenda.objects.filter(user=user, question=key, anster=daan)
                if len(wenda) > 0:
                    for w in wenda:
                        w.delete()
                wenda = MyWenda()
                wenda.user = user
                wenda.question = key
                wenda.anster = daan
                wenda.save()
            all_wendas = MyWenda.objects.filter(user=user).order_by("id")[:10]
            return render(request, "wenda.html", locals())
    except Exception as e:
        print(e)
        return render(request, "wenda.html", locals())

