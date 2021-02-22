---
title: "Filterについて"
date: 2021-02-22T23:24:12+09:00
draft: false
tags: ["dsp", "lang-ja"]
---

[自作シンセにLPFを実装したとき](https://github.com/klknn/synth2/commit/e8ee1bc4a237c5b2c5c388d2fab7a3fb1977c26a) の備忘録。私は大学生のころに、制御理論や複素解析もやっていたのですが、その辺の予備知識ないと理解できないと思う。

記号のリスト

- $j$: 虚数
- $\omega$: 各周波数。周波数 (Hz) に $2\pi$ をかけたもの
- $T$: サンプリング周期
- $\omega_0$: カットオフ角周波数
- $Q$: レゾナンス (Quality Factorとも呼ぶ) $Q = \sqrt{1/2}$ 以上で、 $\omega_0$ にピークが立つ
- $x(n)$: 時刻 $n$ におけるフィルタの入力サンプル
- $y(n)$: 時刻 $n$ におけるフィルタの出力サンプル
- $a_i$: i時刻前の出力にかかるフィルタ係数(これをIIRフィルタと呼ぶ)
- $b_i$: i時刻前の入力にかかるフィルタ係数(これをFIRフィルタと呼ぶ)

## デジタルフィルタの定義

一般的なフルIIRフィルタ (IIRおよびFIRフィルタも含む) は時間ドメインでは以下の形をしている 
\begin{align}
y(n) = \sum_{i=0}^{B} b_i x(n - i) - \sum_{j=1}^{A} a_j y(n - j)
\end{align}
これをZ変換 (回路理論で用いられるフーリエ変換の仲間)した入出力比を伝達関数(transfer function)と呼ぶ:
\begin{align}
H(z) = \frac{Y(z)}{X(z)} = \sum_{i=0}^{B} b_i z^{-i} - H(z) \sum_{j=1}^{A} a_j z^{-j} = \frac{\sum_{i=0}^{B} b_i z^{-i}}{1 + \sum_{j=1}^{A} a_j z^{-j}}
\end{align}
ここで次のような bilinear 変換によりラプラスドメインの伝達関数 $H(s)$ にできる:
\begin{align}
s &= \frac{2}{T} \frac{z-1}{z+1}, \newline
z &= \frac{2 + sT}{2 - sT},
\end{align}

なお、さらに角周波数・位相領域を捉えるにはフーリエ変換として $s = j \omega$ を代入すれば $|H(j \omega)|$ が周波数ごとの amplitude (db/octの傾きとかわかる), $\angle{H(j \omega)}$ が周波数ごとの位相応答 (線形位相かなどわかる) を表す関数となる。私はこの Z <-> ラプラス <-> フーリエの互換性が、工学的に回路・制御・信号処理の世界を自由にわたる橋のようで、とても好きなのです。


## Butterworth

というフィルタが音響処理では普及している。他のフィルタと比べてカットオフ周波数のロールオフが緩やかという性質がある。以下にラプラス領域での定義を示す。Z変換した値は数式記号処理ソフトを使って式 (3) を代入するか、以下の本の 8.10 節で確認すると良い

> Sean Luke, 2019, Computational Music Synthesis, zeroth edition, available for free at http://cs.gmu.edu/~sean/book/synthesis/ 

より一般的な Butterworth フィルタについてはこの PDF が詳しい

> Vadim Zavalishin, The Art of VA Filter Design https://www.discodsp.net/VAFilterDesign_2.1.0.pdf

### Low Pass Filter (LPF) 6db

1 pole (分母 = 0の方程式が1つの解をもつ) で 6db/octave で高域が減衰する。

\begin{align}
H(s) = \frac{1}{s + 1}
\end{align}

### Low Pass Filter (LPF) 12db

2 pole (分母 = 0の方程式が2つの解をもつ) で 12db/octave で高域が減衰する。

\begin{align}
H(s) = \frac{1}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

### High Pass Filter (HPF) 12db

上に同じ性質をもつが逆に低域が減衰する。

\begin{align}
H(s) = \frac{\frac{s^2}{\omega_0^2}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}


### Band Pass Filter (BPF) 12db

上に同じ性質を持つが高域と低域の両方が減衰する。

\begin{align}
H(s) = \frac{\frac{s}{\omega_0 Q}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

## メモ

- 上記のフィルタは全周波数で均等に位相を変化させるので線形位相フィルタとよばれる
- 1-pole フィルタはレゾナンスをもたない
- 全く周波数を変化しない代わりに周波数ごとの位相を変える All Pass Filterというものがある。周波数ごとに音の遅れ方を変えたいリバーブなどで使う

私にはまだN-poleのLPFとかがどういう形なのか完全に理解できてない。疑問として、たとえば2-pole のフィルタを 2回かけたら 4-pole になるのだろうか (3-poleは1+2-poleなのだろうか) ？poleの数とdb/octの関係からそんな気がする。おそらく実際に2回フィルタを畳みこむ必要はなく、ラプラス(とZ)変換では単に伝達関数を二乗すればよいので楽できそう(The Art of VA Filter Design の 10.5 読んだ感じそう思える)。
