---
title: "VirtualBoxで別ディスクのOSを起動する"
date: 2023-08-11 16:25:33 +0900
draft: false
tags: ["memo"]
isCJKLanguage: true
---

机にWindowsとLinux二台置くのはだるいし、ちょっとした動作確認とかなら性能もいらずにGUIを触れることが大事なので、一つのPCに両OSをインストールしてVirtualBoxで起動するのが便利です。

<!--more-->

ホストOS(例Windows11)ではこんな感じで仮想ハードディスクであるvmdkファイルを作成できる。 
```shell
cd 'C:\Program Files\Oracle\VirtualBox\'
.\VBoxManage.exe createmedium -filename "C:\Users\aaa\VirtualBox VMs\ubuntu22.vmdk" --format=VMDK --variant RawDisk --property RawDrive=\\.\PHYSICALDRIVE1
```
出力先や`\\.\PHYSICALDRIVE1` の番号は適宜disk managementなどのアプリで確認したものを指定してください。
`internalcommands createrawvmdk` を[使う場合](https://www.serverwatch.com/guides/how-to-use-a-physical-hard-drive-with-a-virtualbox-vm/)、なぜかWindows11だとNOT FOUNDみたいなエラーでてきて作れませんでした。

そんで仮想マシンを新規作成するときのUIがややこしくて、まず一番下のハードディスク欄でvmdkファイルを指定すると、一番上の方の名前を入力して完了。実際起動するとこんなエラーがでるので、

> 仮想マシンの実行中にエラーが発生しました！エラーの詳細を以下に示します。説明されたエラーを修正し、仮想マシンの再実行することができます。
The I/O cache encountered an error while updating data in medium &quot;ahci-0-0&quot; (rc=VERR_ACCESS_DENIED). Make sure there is enough free space on the disk and that the disk is working properly. Operation can be resumed afterwards.

> Error ID:BLKCACHE_IOERR
Severity:致命的でないエラー

設定の[ストレージ]で先述のvmdkファイルを選んで、[ホストのI/O キャッシュを使う]を有効にします。参考: https://so-zou.jp/software/tool/virtualization/virtual-box/

![ゲストアドオンCDを入れたスクショ](https://github.com/klknn/klknn.github.io/assets/57452864/3b738654-a2cf-4940-8c04-d15c235f2ae5)

画面のリサイズは「デバイス>Guest Additions CDイメージの挿入」をクリックすると、ゲストOS側にCDが認識されるので `autorun.sh` というファイルを実行すると機能します。
