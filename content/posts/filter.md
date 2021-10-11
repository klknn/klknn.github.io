---
title: "デジタルフィルタの実装"
date: 2021-02-22T23:24:12+09:00
draft: false
tags: ["dsp", "lang-ja"]
isCJKLanguage: true
---

[自作シンセにLPFを実装したとき](https://github.com/klknn/synth2/commit/e8ee1bc4a237c5b2c5c388d2fab7a3fb1977c26a) の備忘録。

記号のリスト

- $j$: 虚数
- $\omega$: 各周波数。周波数 (Hz) に $2\pi$ をかけたもの
- $T$: サンプリング周期、サンプリング周波数の逆数
- $\omega_0$: カットオフ角周波数
- $Q$: レゾナンス (Quality Factorとも呼ぶ) $Q = \sqrt{1/2}$ 以上で、 $\omega_0$ にピークが立つ
- $x[n]$: 時刻 $n$ におけるフィルタの入力サンプル
- $y[n]$: 時刻 $n$ におけるフィルタの出力サンプル
- $a_t$: $t$ 時刻前の出力にかかるフィルタ係数(これをIIRフィルタと呼ぶ)
- $b_t$: $t$ 時刻前の入力にかかるフィルタ係数(これをFIRフィルタと呼ぶ)

## デジタルフィルタの定義

一般的なフルIIRフィルタ (IIRおよびFIRフィルタも含む) は時間ドメインでは入出力信号 $x, y$ にそれぞれフィルタ係数 $a, b$ をかけた畳み込みで実装できる:
\begin{align}
y[n] = \sum_{t=0}^{B} b_t x[n - t] - \sum_{t=1}^{A} a_t y[n - t]
\end{align}

IIRフィルタが所望の周波数特性をもつように定義するにはZ変換・ラプラス変換・フーリエ変換を用いる。
先の時間領域の等式の両辺を入力 $x[n]$ で割った入出力比を伝達関数(transfer function)と呼ぶ。さらに $x, y$ をZ変換とよばれる下記の置き換え
\begin{align}
X(z) = \sum_{t} x[t] z^{-t}
\end{align}
によりZ領域での伝達関数を考える:
\begin{align}
H(z) &= \frac{Y(z)}{X(z)}
= \frac{X(z) \sum_{t=0}^{B} b_t z^{-t} - Y(z) \sum_{t=1}^{A} a_t z^{-t}}{X(z)} \nonumber \newline
&= \sum_{t=0}^{B} b_t z^{-t} - H(z) \sum_{t=1}^{A} a_t z^{-t} \nonumber \newline
&= \frac{\sum_{t=0}^{B} b_t z^{-t}}{1 + \sum_{t=1}^{A} a_t z^{-t}}
\end{align}
ここで次のような bilinear 変換によりラプラス領域の伝達関数 $H(s)$ にできる:
\begin{align}
s &= \frac{2}{T} \frac{z-1}{z+1}, \newline
z &= \frac{2 + sT}{2 - sT},
\end{align}
ラプラス領域を介することで、さらにフーリエ変換として $s = j \omega$ を代入すれば周波数や位相の特性を得られる。絶対値をとれば $|H(j \omega)|$ が周波数ごとの音量 (db/octの傾きとかわかる), 位相をとれば $\angle{H(j \omega)}$ が周波数ごとの位相応答 (線形位相かなどわかる) を表す関数となる。

## フィルタ設計の流れ

上記の各種変換により、デジタルの実装（離散時間領域）と、位相周波数応答の特性（フーリエ領域）を定義することができる。ここでは触れないが、一時的にでてくるラプラス変換もアナログ回路との対応があり勉強すると楽しい。

1. 離散時間領域 (コード実装の世界) $x[t]$
2. Z変換領域 (信号処理における離散と連続の出入口) $X(z)$
3. ラプラス変換領域 (アナログ回路との親和性) $X(s)$
4. フーリエ変換領域 (位相・周波数の解析) $X(j\omega)$

ここまでの話を 4 から 1 に逆にたどると、デジタルフィルタの設計の流れとなる。つまり所望の位相・周波数特性を考え、逆変換により等価なフィルタ係数 $(a_t, b_t)$ を導出するという作業である。

## Butterworth

代表的なフィルタとしてButterworthフィルタが音響処理では普及している。他のフィルタと比べてカットオフ周波数のロールオフが緩やかでカットオフ後に荒ぶらない性質がある。アナログ回路に基づいているので多くの場合はラプラス領域での伝達関数が示される。デジタルフィルタとして実装する場合に必要である、Z変換した伝達関数は数式記号処理ソフトを使って式 (3) を代入すると得られる。具体例は後述する実験結果か、以下の本の 8.10 節でも確認できる

> Sean Luke, 2019, Computational Music Synthesis, zeroth edition, available for free at http://cs.gmu.edu/~sean/book/synthesis/

より一般的な Butterworth フィルタについてはこの PDF が詳しい (余談だが、著者はNIのMassiveやReaktorの開発者らしい [linkedin](https://www.linkedin.com/in/vadim-zavalishin-451bb812b))

> Vadim Zavalishin, The Art of VA Filter Design https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf

この辺の話は VA Filter Design の2章がよくまとまっている。それでは実際に使われるLPF/HPF/BPFを導出する。

## 1-pole Low Pass Filter (LPF) 6db/oct

天下り的に定義を覚えてもいいが、自分の中で納得する導出を考えてみる。

人間には音の高さや大きさが対数スケールで感じる(例えば倍の周波数が1オクターブ上として聞こえる)ので、指数的に周波数を倍にすると、音量が半分になるようなLPフィルタがほしい。そのためには周波数の逆数みたいな周波数応答がいい。
\begin{align}
|H(j\omega)| &= \frac{1}{w},
\end{align}
ただし周波数0のときに無限の音量になるのでやばい。そこで
\begin{align}
|H(j\omega)| &= \frac{1}{w + 1},
\end{align}
とすれば周波数0では元の音量のまま、他では倍の周波数では半分の音量になる。この周波数応答をもつラプラス領域での伝達関数には以下のものが考えられる
\begin{align}
H(s) &= \frac{1}{s + 1}.
\end{align}
さらに $s = s' / \omega_0$ を代入することで、対数スケールで周波数を左右に平行移動できる。これは仮定のない一般的な方法なので、同じ代入式で任意のフィルタ伝達関数にカットオフ周波数 $\omega_0$ を導入できる。
\begin{align}
H(s) = \frac{1}{\frac{s}{\omega_0} + 1}
\end{align}

この式は 1 pole (分母 = 0の方程式が1つの解をもつ) であり、倍の周波数(1 octave上) で0.5倍の音量つまりデシベル(db)でいうと $20 \log_{10} 0.5 \approx -6$ db/octave で高域が減衰するという。

## 1-pole High Pass Filter (HPF) 6db/oct

LPFと同じような議論で、$s / \omega_0$ の代わりに二倍低い周波数が二倍小さいレベルとなるよう $\omega_0 / s$が使えることがわかる。代入するとこのような伝達関数が得られる:
\begin{align}
H(s) = \frac{\frac{s}{\omega_0}}{\frac{s}{\omega_0} + 1}
\end{align}

## 2-pole Low Pass Filter (LPF) 12db/oct

単純に1-pole LPFを二回かけると 2 pole (分母 = 0の方程式が2つの解をもつ) で 12db/octave で高域が減衰するLPFになる。フィルタは畳み込みなので、そのラプラス変換は積つまり、もとのLPFの二乗になる。

単純に二回かけるかわりに、2-poleではレゾナンス $Q$ により周波数ピークをたたせることができる。
\begin{align}
H(s) = \frac{1}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}
TODO: なぜ Q でピークがたつかの説明 (天下り的に周波数応答みればよいが、直感的な説明があるとよい)。詳細はVA Filter Designの 4.2 Resonanceを読むとよい。

## 2-pole High Pass Filter (HPF) 12db/oct

上に同じ性質をもつが逆に低域が減衰する。

\begin{align}
H(s) = \frac{\frac{s^2}{\omega_0^2}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

## 2-pole Band Pass Filter (BPF) 12db/oct

上に同じ性質を持つが高域と低域の両方が減衰する。

\begin{align}
H(s) = \frac{\frac{s}{\omega_0 Q}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

## 具体的なフィルタ係数の導出 (pythonによる自動導出)

得られたラプラス領域の伝達関数を冒頭の式(2), (3)を用いたZ変換することで、実装に必要なデジタルフィルタの係数 $a_t$ と $b_t$ が得られる。1-poleくらいなら手計算してもいいが、2-poleになるとしんどいので面倒なことはPython (の数式処理ライブラリであるSymPy) にやらせよう。

コード [filter_coeff.py](/filter_coeff.py)
{{< render-code file="/static/filter_coeff.py" language="py" >}}

結果 [filter_coeff.txt](/filter_coeff.txt)
{{< render-code file="/static/filter_coeff.txt" language="txt" >}}

ある程度、展開できればいいやと思ってたが、完全に自動化できると思ってなかった...天才かもしれない(sympyがすごいだけである)。ちなみにsympyのインストールが面倒ならGoogle colabとかから試せると思う。

## メモ・疑問

- リアルタイム性は犠牲になるが、位相が変化しない線形位相フィルタとはどういうものか
- MoogやTB303に搭載されるLPFはButterworthではない ([コード](https://github.com/klknn/synth2/blob/c3d06e87b10fe31e6b68d060b1e5c8788f383d9d/tool/filter_coeff.py#L62-L73))。どのようにして設計されるか考察したい。
- 1-pole フィルタはレゾナンスをもたない?
- 全く周波数を変化しない代わりに周波数ごとの位相を変える All Pass Filterというものがある。周波数ごとに音の遅れ方を変えたいリバーブなどで使う
- より一般化されたButterworth filter自体の定義とは?私にはまだN-poleのLPFとかがどういう形なのか完全に理解できてない
