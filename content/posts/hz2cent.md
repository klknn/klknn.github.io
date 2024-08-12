---
title: "周波数Hz比から半音階への変換"
date: 2024-08-12 13:25:33 +0900
draft: false
tags: ["dtm", "music"]
isCJKLanguage: true
---

オーケストラなどA=440Hz以外の基準周波数で録音するとき、440Hzで設定されてるプラグイン側の周波数を修正したいことはよくある。しかし大抵は半音単位やセントでチューニングを指定することになる。それを自動的に求めるJSを書いてみた。

<!--more-->

## やり方

プラグイン標準の基準周波数 x (例 440Hz) 、目的の基準周波数 y (例 443Hz) に変更するには半音階のパラメータ z との間には、1オクターブ (= 2倍の周波数間) を12等分する平均律の定義から:

\begin{align}
2 ^\frac{z}{12} &= \frac{y}{x} \newline
z &= 12 \log_2 \frac{y}{x}
\end{align}

たとえば 440Hz の音源を 443Hz にピッチシフトしたい場合は $ z = 12 \log_2 \frac{443}{440} = 0.1176381... $ 半音上げれば良い。関数電卓が手元にない人のためにJavaScriptで書いてみると、こんな感じ:

{{< render-code file="/static/js/hz2cent.js" language="js" >}}


{{< js_hz2cent >}}


## プラグインの設定

シンセサイザーなどはユニゾンのためなど比較的わかりやすくfinetuneなどの項目があるが、サンプラー系はわかりにくいので注意。

East West Playの場合はここ

![image](https://github.com/user-attachments/assets/24662da4-5886-4d44-bbed-39bab4f8579c)

Kontakt の場合はここ

![image](https://github.com/user-attachments/assets/0754f988-b824-41ce-a1db-bdb5a9263c18)