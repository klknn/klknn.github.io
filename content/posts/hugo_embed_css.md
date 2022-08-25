---
title: "HugoにおけるCSSの埋め込みと後処理"
date: 2022-08-26T04:55:30+09:00
draft: false
tags: ["hugo"]
isCJKLanguage: true
---

CSSを試行錯誤中なのですがブラウザのキャッシュが効いて反映されないため面倒だなと思い、Hugo の asset 管理を使ってHTMLに埋め込んでみました。
おまけに最小化やSCSSの導入など、思わぬ副次効果もありました。

<!--more-->

## これまでの問題

ここ最近の更新では、たびたびCSSを弄っていました。これまでは元ファイルを `/static/main.css` に置いてそのまま直接リンクを貼っていたのですが、リンクを介すことでブラウザのキャッシュが効いてしまい、 `$ hugo serve` をしているとき即座に反映されない悩みがありました。

ついでに生のCSSって冗長で人間が書くものでは無いな...と思っていたのでどうせHugoを使って処理するなら...とSASS/SCSSに移行していきます。

一方、埋め込むことで読み込みに時間がかかるのではという懸念もありますが、後処理がてら`hugo --minify`で最小化できます。これで普段は人間に読める形で試行錯誤できる上に、デプロイ時は最小化してるので良いところどりです。
最終的に埋め込みが問題になれば `.RelURL` によるリンク生成も可能なのでキャッシュ効く形に戻すのも容易です。

## SCSSの読み込み

というわけでHugoのasset管理を使って、HTMLに直接埋め込みます。 `/assets/main.scss` にファイルを移動した上で、このように読み込みます。

```Go HTML Template
    {{ $css := resources.Get "main.scss" | resources.ToCSS }}
    <style>
      {{ $css.Content | safeCSS }}
    </style>
```

でてくる関数の詳細は https://gohugo.io/categories/asset-management を読んでください。SCSSを使うには extended と書いてあるバイナリを使う必要があるので注意です。生成されたファイルは `/resources/_gen/*` に作られるので `.gitignore` などに含めておくと良いでしょう

ちなみにSCSSはCSSと概ね互換性があるので、そのまま読めます。文法はここ　https://sass-lang.com/documentation/syntax より https://sass-lang.com/guide のほうが簡単にまとまってていいです。今回はとりあえず変数と演算を使ってページの幅とか調整しました。正直文法が気持ち悪いのであまり深追いしたくはないです。

## まとめ

気が変わっていにしえのHTML/CSS直書き原理主義にもどるかもしれませんが、いまのところMarkdown -> HTML と SCSS -> CSSと変換できるHugoに満足です。
全体的な変更は以下のcommitを参考にしてください:
https://github.com/klknn/klknn.github.io/commit/8274c0765fe232a562ce229983d7a955bf480bad
