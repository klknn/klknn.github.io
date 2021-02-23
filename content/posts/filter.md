---
title: "デジタルフィルタの実装"
date: 2021-02-22T23:24:12+09:00
draft: false
tags: ["dsp", "lang-ja"]
---

[自作シンセにLPFを実装したとき](https://github.com/klknn/synth2/commit/e8ee1bc4a237c5b2c5c388d2fab7a3fb1977c26a) の備忘録。私は大学生のころに、制御理論や複素解析もやっていたのですが、その辺の予備知識ないと理解できないと思う。

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

一般的なフルIIRフィルタ (IIRおよびFIRフィルタも含む) は時間ドメインでは入出力信号とフィルタ係数の畳み込みで実装できる:
\begin{align}
y[n] = \sum_{t=0}^{B} b_t x[n - t] - \sum_{t=1}^{A} a_t y[n - t]
\end{align}
これをZ変換 (回路理論で用いられるフーリエ変換の仲間)した入出力比を伝達関数(transfer function)と呼ぶ:
\begin{align}
H(z) &= \frac{Y(z)}{X(z)}
= \frac{X(z) \sum_{t=0}^{B} b_t z^{-t} - Y(z) \sum_{t=1}^{A} a_t z^{-t}}{X(z)} \nonumber \newline
&= \sum_{t=0}^{B} b_t z^{-t} - H(z) \sum_{t=1}^{A} a_t z^{-t} \nonumber \newline
&= \frac{\sum_{i=0}^{B} b_i z^{-i}}{1 + \sum_{j=1}^{A} a_j z^{-j}}
\end{align}
ここで次のような bilinear 変換によりラプラスドメインの伝達関数 $H(s)$ にできる:
\begin{align}
s &= \frac{2}{T} \frac{z-1}{z+1}, \newline
z &= \frac{2 + sT}{2 - sT},
\end{align}

なお、さらに角周波数・位相領域を捉えるにはフーリエ変換として $s = j \omega$ を代入すれば $|H(j \omega)|$ が周波数ごとの音量 amplitude (db/octの傾きとかわかる), $\angle{H(j \omega)}$ が周波数ごとの位相応答 (線形位相かなどわかる) を表す関数となる。私はこの Z <-> ラプラス <-> フーリエの互換性が、工学的に回路・制御・信号処理の世界を自由にわたる橋のようで、とても好きなのです。


## Butterworth

というフィルタが音響処理では普及している。他のフィルタと比べてカットオフ周波数のロールオフが緩やかという性質がある。以下にラプラス領域での定義を示す。Z変換した値は数式記号処理ソフトを使って式 (3) を代入するか、以下の本の 8.10 節で確認すると良い

> Sean Luke, 2019, Computational Music Synthesis, zeroth edition, available for free at http://cs.gmu.edu/~sean/book/synthesis/ 

より一般的な Butterworth フィルタについてはこの PDF が詳しい (余談だが、著者はNIのMassiveやReaktorの開発者らしい [linkedin](https://www.linkedin.com/in/vadim-zavalishin-451bb812b))

> Vadim Zavalishin, The Art of VA Filter Design https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf

つぎに実際の定義を見ていく

## 1-pole Low Pass Filter (LPF) 6db/oct

天下り的に普及してるフィルタを覚えてもいいが、自分の中で納得する説明を考えてみる。

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

### 離散信号への適用

得られたラプラス領域の伝達関数を冒頭の式(2), (3)を用いたZ変換することで、デジタルフィルタの定義 ($a_t$ と $b_t$ の値) が得られる。手計算してもいいがしんどいので面倒なことはPython (の数式処理ライブラリであるSymPy) に頼ろう。

[filter_coeff.py](/filter_coeff.py)
```python
# requires version '1.7.1
from sympy import *

s = Symbol('s')
z = Symbol('z')
Q = Symbol('Q')    # resonance
T = Symbol('T')    # sampling interval
w0 = Symbol('w0')  # cutoff freq

# z2s = 2 / T * (z - 1) / (z + 1)
s2z = 2 / T * (z - 1) / (z + 1)

def print_coeff(hs):
    hz = simplify(hs.subs(s, s2z))  # Z transform
    npole = degree(denom(hs), s)
    print("=== Transfer function ===")
    print("H(s) =", hs)  # transfer function in Laplace domain
    print("H(z) =", hz)  # transfer function in Z domain
    print("#pole =", npole)
    print("=== Filter coeffients ===")
    # FIR coeff
    dhz = collect(expand(denom(hz) * z ** -npole), z)
    nhz = collect(expand(numer(hz) * z ** -npole), z)
    a0 = dhz.coeff(z, 0)  # to normalize a0 = 1
    for i in range(npole + 1):
        print(f"b{i} =", nhz.coeff(z, -i) / a0)
    # IIR coeff
    for i in range(1, npole + 1):
        print(f"a{i} =", dhz.coeff(z, -i) / a0)


print("Filter: 1-pole LPF")
print_coeff(hs = 1 / (s / w0 + 1))
print()
print("Filter: 1-pole HPF")
print_coeff(hs = s / (s + w0))
print()
print("Filter: 2-pole LPF")
print_coeff(hs = w0**2 / (s**2 + s * w0 * Q + w0**2))
print()
print("Filter: 2-pole HPF")
print_coeff(hs = (s**2 / w0**2) / (s**2 + s * w0 * Q + w0**2))
```
ある程度、展開できればいいやと思ってたが、完全に自動化できると思ってなかった...天才かもしれない(sympyがすごいだけである)。ちなみにsympyのインストールが面倒ならGoogle colabとかから試せると思う。

このフィルタの結果は以下の通り
```
Filter: 1-pole LPF
=== Transfer function ===
H(s) = 1/(s/w0 + 1)
H(z) = T*w0*(z + 1)/(T*w0*(z + 1) + 2*z - 2)
#pole = 1
=== Filter coeffients ===
b0 = T*w0/(T*w0 + 2)
b1 = T*w0/(T*w0 + 2)
a1 = (T*w0 - 2)/(T*w0 + 2)
```
この辺の話は VA Filter Design の2章が詳しい。

## 1-pole High Pass Filter (HPF) 6db/oct

LPFと同じような議論で、$s / \omega_0$ の代わりに二倍低い周波数が二倍小さいレベルとなるよう $\omega_0 / s$が使えることがわかる。代入するとこのような伝達関数が得られる:
\begin{align}
H(s) = \frac{\frac{s}{\omega_0}}{\frac{s}{\omega_0} + 1}
\end{align}
上記のプログラムの `hs` を変更すると、結果は以下の通り
```
Filter: 1-pole HPF
=== Transfer function ===
H(s) = s/(s + w0)
H(z) = 2*(z - 1)/(T*w0*(z + 1) + 2*z - 2)
#pole = 1
=== Filter coeffients ===
b0 = 2/(T*w0 + 2)
b1 = -2/(T*w0 + 2)
a1 = (T*w0 - 2)/(T*w0 + 2)
```

## Low Pass Filter (LPF) 12db

単純に1-pole LPFを二回かけると 2 pole (分母 = 0の方程式が2つの解をもつ) で 12db/octave で高域が減衰するLPFになる。フィルタは畳み込みなので、そのラプラス変換は積つまり、もとのLPFの二乗になる。

単純に二回かけるかわりに、2-poleではレゾナンス $Q$ により周波数ピークをたたせることができる。
\begin{align}
H(s) = \frac{1}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}
TODO: なぜ Q でピークがたつかの説明 (天下り的に周波数応答みればよいが、直感的な説明があるとよい)。詳細はVA Filter Designの 4.2 Resonanceを読むとよい。

プログラムの結果は以下の通り
```
=== Transfer function ===
H(s) = w0**2/(Q*s*w0 + s**2 + w0**2)
H(z) = T**2*w0**2*(z + 1)**2/(2*Q*T*w0*(z - 1)*(z + 1) + T**2*w0**2*(z + 1)**2 + 4*(z - 1)**2)
#pole = 2
=== Filter coeffients ===
b0 = T**2*w0**2/(2*Q*T*w0 + T**2*w0**2 + 4)
b1 = 2*T**2*w0**2/(2*Q*T*w0 + T**2*w0**2 + 4)
b2 = T**2*w0**2/(2*Q*T*w0 + T**2*w0**2 + 4)
a1 = (2*T**2*w0**2 - 8)/(2*Q*T*w0 + T**2*w0**2 + 4)
a2 = (-2*Q*T*w0 + T**2*w0**2 + 4)/(2*Q*T*w0 + T**2*w0**2 + 4)
```
ぱっと見、CMS 8.10の結果と一致してる気がする。

## High Pass Filter (HPF) 12db

上に同じ性質をもつが逆に低域が減衰する。

\begin{align}
H(s) = \frac{\frac{s^2}{\omega_0^2}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

```
Filter: 2-pole HPF
=== Transfer function ===
H(s) = s**2/(w0**2*(Q*s*w0 + s**2 + w0**2))
H(z) = 4*(z - 1)**2/(w0**2*(2*Q*T*w0*(z - 1)*(z + 1) + T**2*w0**2*(z + 1)**2 + 4*(z - 1)**2))
#pole = 2
=== Filter coeffients ===
b0 = 4/(2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)
b1 = -8/(2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)
b2 = 4/(2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)
a1 = (2*T**2*w0**4 - 8*w0**2)/(2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)
a2 = (-2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)/(2*Q*T*w0**3 + T**2*w0**4 + 4*w0**2)
```


## Band Pass Filter (BPF) 12db

上に同じ性質を持つが高域と低域の両方が減衰する。

\begin{align}
H(s) = \frac{\frac{s}{\omega_0 Q}}{\frac{s^2}{\omega_0^2} + \frac{s}{\omega_0 Q} + 1}
\end{align}

```
=== Transfer function ===
H(s) = s/(Q*w0*(Q*s*w0 + s**2 + w0**2))
H(z) = 2*T*(z - 1)*(z + 1)/(Q*w0*(2*Q*T*w0*(z - 1)*(z + 1) + T**2*w0**2*(z + 1)**2 + 4*(z - 1)**2))
#pole = 2
=== Filter coeffients ===
b0 = 2*T/(2*Q**2*T*w0**2 + Q*T**2*w0**3 + 4*Q*w0)
b1 = 0
b2 = -2*T/(2*Q**2*T*w0**2 + Q*T**2*w0**3 + 4*Q*w0)
a1 = (2*Q*T**2*w0**3 - 8*Q*w0)/(2*Q**2*T*w0**2 + Q*T**2*w0**3 + 4*Q*w0)
a2 = (-2*Q**2*T*w0**2 + Q*T**2*w0**3 + 4*Q*w0)/(2*Q**2*T*w0**2 + Q*T**2*w0**3 + 4*Q*w0)
```

## メモ・疑問

- リアルタイム性は犠牲になるが、位相が変化しない線形位相フィルタとはどういうものか
- 1-pole フィルタはレゾナンスをもたない?
- 全く周波数を変化しない代わりに周波数ごとの位相を変える All Pass Filterというものがある。周波数ごとに音の遅れ方を変えたいリバーブなどで使う
- より一般化されたButterworth filter自体の定義とは?私にはまだN-poleのLPFとかがどういう形なのか完全に理解できてない
