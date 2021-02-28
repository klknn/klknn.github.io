---
title: "WindowsでのDplug開発"
date: 2021-02-28T14:24:12+09:00
draft: false
tags: ["dplug", "lang-ja"]
isCJKLanguage: true
---

[Synth2](https://github.com/klknn/synth2) 開発のために，普段の音楽制作で使ってるWindowsで開発環境を構築しました．その備忘録です．

## コンパイラ

以下のツールが必要

- MSVC x64/x86 build tools (v14.28) + Windows 10 SDK (10.01924.10) : https://visualstudio.microsoft.com
  64bitバイナリのリンクに必要．数GBあるのなんなんですかね．(XCodeよりはマシだが)．Github Actions読み解けば減らせるかもしれない．
- ldc2 最新版 (ldc2-1.25.0-windows-x64.7z): https://github.com/ldc-developers/ldc/releases
  D言語のコンパイルに必要．
- dplug-build: https://github.com/AuburnSounds/Dplug/wiki/Getting-Started#step-3-build-the-dplug-build-tool
  動的ライブラリをVST3等のプラグインに変換するときに必要．

色々書くのが面倒で動画も作ったので，暇な人は見てください．

https://www.youtube.com/watch?v=vZEgpgHGI-A&t=17s

動画ではPowerShellを使ってますが，私はzsh (+tmux+emacs) が好きなので，基本 [MSYS2](https://www.msys2.org/) で開発してます．

## エディタ

拘りがなければ [VSCode の D 言語拡張](https://github.com/Pure-D/code-d) を入れるのが一番いいと思います．私はemacsが好きなので使ってませんが．

とにかくEmacs対応が一番大変でした．D言語での補完などはDCDが一般的なツールで，それをもとにLSPなどが整備されているようですが，現状VSCode以外で動かせず (Linuxでもできなかった)．結局いつもLinuxで使ってるDCDの薄いラッパーである company-dcd に Windows 特有の問題 (DUBパッケージの場所，パスの文法，CR改行) を対処するパッチをあてて使いました．正確には company-dcd が依存してる flycheck-dmd-dub というパッケージにもパッチが必要です．

- https://github.com/klknn/flycheck-dmd-dub/tree/fix-cygwin
- https://github.com/klknn/company-dcd/tree/fix-cygwin

上記のパッケージにelispのパスを通して，こんな感じで設定してます．

```elisp
(add-to-list 'load-path "flycheck-dmd-dubのパス")
(add-to-list 'load-path "company-dcdのパス")
(add-hook 'd-mode-hook 'company-dcd-mode)
(setq company-dcd-client-execulable "dcd-client.exeのパス")
(setq company-dcd-server-execulable "dcd-server.exeのパス")
```

こんな風にcompanyによる補完や `C-c .` による定義ジャンプが動くはずです．

![emacs-company-dcd.png](/emacs-company-dcd.png)

とりあえず [flycheck-dmd-dub に PR](https://github.com/atilaneves/flycheck-dmd-dub/pull/15) を出しました，もし無事マージされたら company-dcd にもPRしたいと思います．

とても久しぶりにelisp書きましたが，シェルスクリプトばりに雑に書けてインタラクティブに動作できるので気持ちいいなと思いました．この適当にhackして治せる点が，他のエディタにない醍醐味だと思います．もしWindowsでemacsがうまく動かなかったらブチ切れてMacを買っていたかもしれません(そっちで動く保証はないですが)．現在Macは持っていないのでサポートする予定ないです．
