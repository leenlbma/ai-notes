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
        if lang not in p: continue
        t=p[lang];url=f"{pre}posts/{p['slug']}/"+('' if zh else 'en/')
        alt=f"posts/{p['slug']}/en/" if zh else f"../posts/{p['slug']}/"
        en_alt=('' if 'en' not in p else f'<a class="alt" href="{alt}" hreflang="{'en' if zh else 'zh-CN'}">{'EN' if zh else '中文'}</a>')
        items+=f'''<li><a class="post" href="{url}"><span class="no">{p['no']}</span><span class="body"><h2>{html.escape(t['title'])}</h2><p>{html.escape(t['summary'])}</p></span><span class="date">{p['date'].replace('-','.')}</span></a>{en_alt}</li>'''
    title=f"{s['name']} · {S['zh']['name'] if not zh else S['en']['name']}"
    url=B+('' if zh else 'en/')
    sw='<b>中文</b> / <a href="en/" hreflang="en">EN</a>' if zh else '<a href="../" hreflang="zh-CN">中文</a> / <b>EN</b>'
    return f'''<!DOCTYPE html><html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{html.escape(s['tagline'])}"><link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{B}"><link rel="alternate" hreflang="en" href="{B}en/"><link rel="alternate" hreflang="x-default" href="{B}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(s['tagline'])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{'zh_CN' if zh else 'en_US'}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{html.escape(s['tagline'])}">
<meta name="author" content="{S['author']}"><link rel="license" href="https://creativecommons.org/licenses/by/4.0/"><link rel="stylesheet" href="{pre}assets/home.css"><script defer src="https://cloud.umami.is/script.js" data-website-id="8ba58f50-24d2-4d61-a09c-1aa3558a4ade"></script></head>
<body><header class="wrap"><div class="top"><span>{s['name']} · {S['author']}</span><span class="lang">{sw}</span></div>
<h1>{s['name']}</h1><div class="x" aria-hidden="true"></div><p class="tag">{html.escape(s['tagline'])}</p><p class="intro">{html.escape(s['intro'])}</p>
<div class="count"><span>{'系列' if zh else 'Series'}</span><b>{sum(lang in p for p in P):02d}</b><span>{'篇' if zh else 'essays'}</span></div></header>
<main class="wrap"><div class="label">{'目录' if zh else 'Contents'}</div><ol class="list">{items}</ol></main>
<footer class="wrap"><div class="about"><div class="label">{'作者' if zh else 'Author'}</div><p>{S['author']} · {'写产品、写代码，也写下想法。' if zh else 'Writes products, code, and the thoughts in between.'}</p></div>
<div class="sub"><div class="label">{'关注' if zh else 'Follow'}</div><p><a href="https://github.com/leenlbma/ai-notes">GitHub · Watch</a> · <a href="{pre}llms.txt">llms.txt</a></p></div>
<small>© {S['author']} · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></small></footer></body></html>
'''
open(os.path.join(R,'index.html'),'w',encoding='utf-8').write(page('zh'))
os.makedirs(os.path.join(R,'en'),exist_ok=True)
open(os.path.join(R,'en','index.html'),'w',encoding='utf-8').write(page('en'))
L=[f"# {S['zh']['name']} / {S['en']['name']}\n",f"> {S['zh']['tagline']} {S['en']['tagline']} 作者 / Author: {S['author']}，{S['license']}。\n",f"- 系列首页 / Series home: {B} · {B}en/\n","## 文章（中文）\n"]
L+=[f"- [{p['no']} · {p['zh']['title']}]({B}posts/{p['slug']}/): {p['zh']['summary']}" for p in P]
L+=["\n## Posts (English)\n"]+[f"- [{p['no']} · {p['en']['title']}]({B}posts/{p['slug']}/en/): {p['en']['summary']}" for p in P if 'en' in p]
open(os.path.join(R,'llms.txt'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
urls=[B,B+'en/']+[u for p in P for u in ([f"{B}posts/{p['slug']}/"]+([f"{B}posts/{p['slug']}/en/"] if 'en' in p else []))]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(R,'sitemap.xml'),'w').write(sm)
print('ok',len(P),'posts')

# check: every html carries Umami
import glob as _g
for _f in _g.glob(os.path.join(R,'**','*.html'),recursive=True):
    assert 'data-website-id="8ba58f50-24d2-4d61-a09c-1aa3558a4ade"' in open(_f,encoding='utf-8').read(), 'Missing Umami: '+_f
