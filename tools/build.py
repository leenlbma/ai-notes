#!/usr/bin/env python3
"""Regenerate series homes (/ and /en/), llms.txt and sitemap.xml from posts.json.
Optional helper: outputs are plain static files committed to the repo. Run: python3 tools/build.py"""
import json,html,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d=json.load(open(os.path.join(R,'posts.json'),encoding='utf-8'));S=d['series'];B=S['base'];P=list(reversed(d['posts']))
def page(lang):
    zh=lang=='zh';s=S[lang];pre='' if zh else '../'
    items=''
    for p in P:
        t=p[lang];url=f"{pre}posts/{p['slug']}/"+('' if zh else 'en/')
        alt=f"posts/{p['slug']}/en/" if zh else f"../posts/{p['slug']}/"
        items+=f'''<a class="post" href="{url}"><div class="meta"><span class="no">{p['no']}</span><span>{p['date']}</span></div>
<h2 class="serif">{html.escape(t['title'])}</h2><p>{html.escape(t['summary'])}</p><span class="more">{'阅读全文 →' if zh else 'Read →'}</span></a>
<p class="alt">{'English：' if zh else '中文：'}<a href="{alt}" hreflang="{'en' if zh else 'zh-CN'}">{html.escape(p['en' if zh else 'zh']['title'])}</a></p>'''
    title=f"{s['name']} · {S['zh']['name'] if not zh else S['en']['name']}"
    url=B+('' if zh else 'en/')
    sw='<b>中文</b> / <a href="en/" hreflang="en">EN</a>' if zh else '<a href="../" hreflang="zh-CN">中文</a> / <b>EN</b>'
    return f'''<!DOCTYPE html><html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{html.escape(s['intro'])}"><link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{B}"><link rel="alternate" hreflang="en" href="{B}en/"><link rel="alternate" hreflang="x-default" href="{B}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(s['intro'])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{'zh_CN' if zh else 'en_US'}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{html.escape(s['intro'])}">
<meta name="author" content="{S['author']}"><link rel="license" href="https://creativecommons.org/licenses/by/4.0/"><link rel="stylesheet" href="{pre}assets/home.css"><script defer src="https://cloud.umami.is/script.js" data-website-id="8ba58f50-24d2-4d61-a09c-1aa3558a4ade"></script></head>
<body><header><div class="wrap"><div class="lang">{sw}</div><div class="eyebrow">{'系列 · ' if zh else 'SERIES · '}{len(P)} {'篇' if zh else ('essay' if len(P)==1 else 'essays')}</div>
<h1 class="serif">{s['name']}</h1><p class="intro">{html.escape(s['intro'])}</p></div></header>
<main class="wrap">{items}</main>
<footer>{s['name']} · © {S['author']} · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> · <a href="https://github.com/leenlbma/ai-notes">GitHub</a></footer></body></html>
'''
open(os.path.join(R,'index.html'),'w',encoding='utf-8').write(page('zh'))
os.makedirs(os.path.join(R,'en'),exist_ok=True)
open(os.path.join(R,'en','index.html'),'w',encoding='utf-8').write(page('en'))
L=[f"# {S['zh']['name']} / {S['en']['name']}\n",f"> {S['zh']['intro']} {S['en']['intro']} 作者 / Author: {S['author']}，{S['license']}。\n",f"- 系列首页 / Series home: {B} · {B}en/\n","## 文章（中文）\n"]
L+=[f"- [{p['no']} · {p['zh']['title']}]({B}posts/{p['slug']}/): {p['zh']['summary']}" for p in P]
L+=["\n## Posts (English)\n"]+[f"- [{p['no']} · {p['en']['title']}]({B}posts/{p['slug']}/en/): {p['en']['summary']}" for p in P]
open(os.path.join(R,'llms.txt'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
urls=[B,B+'en/']+[u for p in P for u in (f"{B}posts/{p['slug']}/",f"{B}posts/{p['slug']}/en/")]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(R,'sitemap.xml'),'w').write(sm)
print('ok',len(P),'posts')

# check: every html carries Umami
import glob as _g
for _f in _g.glob(os.path.join(R,'**','*.html'),recursive=True):
    assert 'data-website-id="8ba58f50-24d2-4d61-a09c-1aa3558a4ade"' in open(_f,encoding='utf-8').read(), 'Missing Umami: '+_f
