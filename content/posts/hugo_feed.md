---
title: "はてなブログ的なfeedをHugoで生成"
date: 2022-08-24T23:32:31+09:00
draft: false
tags: ["hugo"]
isCJKLanguage: true
toc: false
---

RSSリーダーのFeedlyを使っていて、はてなブログとかは全文リーダー内に表示されるのに、うちだけ表示されないな？と疑問に思っていました。
今回ははてなブログのフィードとHugoのデフォルトのフィードを比べた上でよりRSSリーダーフレンドリーなフィードを構築していきます。

<!--more-->

## はてなのfeed

まずFeedlyで適当に普段読んでるhatenaブログをみてみると、取得してるURLが設定画面で把握できます。大抵は以下のようなXMLがでてきます:

```xml
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="ja">
  <title>・ｘ・ぼくののうみそ</title>

  <link href="https://bokunonoumiso.hatenablog.com/"/>
  <updated>2022-08-09T12:41:41+09:00</updated>
  <author>
    <name>bokunonoumiso</name>
  </author>
  <generator uri="https://blog.hatena.ne.jp/" version="149d375eb29bfc5c8439e961a2b85a">Hatena::Blog</generator>
  <id>hatenablog://blog/6653812171403772804</id>
    <entry>
        <title>高い車に乗って安い車を煽る</title>
        <link href="https://bokunonoumiso.hatenablog.com/entry/2022/08/09/124141"/>
        <id>hatenablog://entry/4207112889907092076</id>
        <published>2022-08-09T12:41:41+09:00</published>
        <updated>2022-08-09T12:41:41+09:00</updated>
        <summary type="html">高い車が安い車を煽る…</summary>
        <content type="html">&lt;p&gt;高い車が安い車を煽る&lt;/p&gt;</content>
   </entry>
</feed>
```

注意点としては

- RSS 1.0/2.0ではなく[ATOM規格](http://www.w3.org/2005/Atom)っぽい。summaryに概要、contentに本文を入れることができる。
- summaryでは多くのリーダーで対応するために、htmlタグなしの plainify されたテキストが良さそう。
- contentの中身はhtmlなので、escape するか CDATA 属性に突っ込む。なおhugo組み込み関数のescapeHTMLでは`&`も変換されてしまいうまくいかなかった。
- もし RSS 1.0/2.0 を使いたい場合、本文を表示するには `<content:encoded>` を使うと良いらしい https://www.w3.org/wiki/RssContent


## Hugoのfeed

[Hugo標準付属のrss.xml](https://github.com/gohugoio/hugo/blob/988e1417a057b937a766385f79f46a52e933baee/tpl/tplimpl/embedded/templates/_default/rss.xml)はRSS 2.0なのかAtomなのかよくわからない感じですね。
hatenaブログのフィードっぽくしたテンプレートはこんな感じです。

{{< render-code file="/layouts/index.xml" language="xml" >}}

詳細は以下のcommitを見てください。

https://github.com/klknn/klknn.github.io/commit/afb831f515d54b451e70fbc5e5ae95e669d79c75


## まとめ

RSSリーダーって10年前まではみんな使ってたのにGoogle readerが終わって一気に死んだよね...インターネット老人ネタでした。
