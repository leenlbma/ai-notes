# AI 手记 / AI Notes

AI 手记：技术让事情变快，我想让它们仍然有意义。

- 系列首页：https://leenlbma.github.io/ai-notes/ （English: https://leenlbma.github.io/ai-notes/en/）

## 文章 / Posts

| # | 中文 | English | 日期 |
|---|---|---|---|
| 01 | [仍然是一个亲手创造东西的人](https://leenlbma.github.io/ai-notes/posts/01-still-building-by-hand/) | [Still Someone Who Builds Things by Hand](https://leenlbma.github.io/ai-notes/posts/01-still-building-by-hand/en/) | 2026-10 |

## 目录结构

```
index.html, en/index.html     系列首页（由 tools/build.py 生成）
posts/<NN-slug>/index.html    中文文章（独立、自包含）
posts/<NN-slug>/en/index.html 英文文章
posts.json                    文章登记表（首页、llms.txt、sitemap 的唯一来源）
templates/post/               新文章骨架（中/英）
assets/home.css               首页样式（文章页不依赖它）
tools/build.py                从 posts.json 重新生成首页、llms.txt、sitemap.xml
```

## 新文章发布步骤（以 02 为例）

1. 复制模板：`cp -r templates/post posts/02-<英文-slug>`。
2. 替换 `{{...}}` 占位符（`{{SLUG}}` 填 `02-<英文-slug>`，`{{NO}}` 填 `02`），写入正文；有英文版就填 `en/index.html`，没有就删掉 `en/` 和语言切换。
3. 在 `posts.json` 的 `posts` 数组末尾追加一条（no、slug、date、zh/en 的 title 与 summary）。
4. 运行 `python3 tools/build.py`，更新首页、`llms.txt`、`sitemap.xml`。
5. 本地用浏览器打开检查（手机宽度 390px、深色与浅色），然后 `git add -A && git commit && git push`，GitHub Pages 约 1 分钟后生效。

无需构建工具也能发布：第 4 步只是便利脚本，也可手工编辑首页和 llms.txt。

## 许可

本仓库内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 许可，署名 Leen Ma。
