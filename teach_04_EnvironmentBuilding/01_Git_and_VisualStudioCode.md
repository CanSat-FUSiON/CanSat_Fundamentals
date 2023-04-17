# GitHubの使い方

  

本記事では、GitHubの使い方や、そのルールについてまとめます。  

ここでいうルールはあくまで過去にそのようなルールを設けていたわけではなく、過去に上手くいかなかったからこそ提案させていただくものであり、今後のメンバーでよりよいFUSiONならではのルールを模索していってほしいです。(2023年4月 塩田 記す)

  

---


## :zap:GitHubとVisualStudioCodeの接続方法

### <u>SSH接続について</u>

ここではVisualStudioCodeとgitを導入しているものとして話を進めます。  

GitHubはHTTPS接続とSSH接続の2種類の接続方法があります。  

HTTPS接続は簡単に接続ができる反面、安全性に欠ける面があります。  

一方、SSH接続は接続に多少の手間がかかるが、HTTPS接続に比べると安全に利用できます。  

そこで、FUSiONではSSH接続によるgitの利用を強く推奨します。  

同様に、以下ではSSH接続のみ説明します。

  
- - - 
### <u>SSH接続のやり方</u>

SSH接続の方法について、以下の記事を参考に。  

[GitHubでssh接続する手順~公開鍵・秘密鍵の生成から~](https://qiita.com/shizuma/items/2b2f873a0034839e47ce)

  
  

1. 公開鍵・秘密鍵を作成する。
    1. 鍵を入れるフォルダに移動`cd ./~ssh`  
    (適宜mkdirでフォルダを作成してください)  
    1. 鍵生成`ssh-keygen -t rsa`  
    (記事ではid_rsaに名前を付けるやり方を説明していますが、特に必要はないかと思います。個人的にはpassphraseの方が重要なのでは？と思ったりします。`git pull`や`git push`の時に**上手くいくと**passphraseを求められて安心する材料になりえます。)
1. 公開鍵をGitHubにアップする。
    1. [こちらのリンク](https://github.com/settings/ssh)から公開鍵の設定ができます。
    1. **New SSH Key**を押す。
    (記事ではAdd SSH Keyをボタンを押すように書かれています。)
    1. titleに任意の名前を付ける。  (特に名前に指定はないです。プログラマーの人々はWindows用のKeyとMac用のKeyと分かりやすくため「Windows」「Mac」というように名前を付けると聞いたことがあります。)
    1. Keyに公開鍵を貼り付ける。  ターミナルにて、Windowsでは`clip < ~/.ssh/id_rsa.pub`、Macでは`pbcopy < ~/.ssh/id_rsa.pub`を実行することで、クリップボードにコピーできます。  **////注意//////////////////////////////////////////**   
     間違えても秘密鍵を貼り付けないようにしましょう！！！  
     /////////////////////////////////////////////////////////
    1. Add SSH Keyで作成。
1. 接続を確かめる。
    1. `ssh -T git@github.com`を実行し、Hi (account_name)!と返ってきたら成功です。  
    記事では書かれていませんでしたが、すんなり返ってくるのではなく、yes/no/fingerprintの選択肢で聞かれることもあるようです。指示を読んで答えるようにしてください。(執筆前日に人に説明している時に起こりました。Do you continue?問う異様な内容で、yesで答えるとHi!が返ってきました。)
    1. 基本的に上手くいくと思いますが、もしもの場合は上記記事を参照にしてください。

  

---

  
  

## :globe_with_meridians:GitHub(リモート)とVScode(ローカル)の連携

  

### <u>GitHubとVScodeの簡単な違い</u>

- GitHub
    - リモート環境
    - チームのプログラムを管理する
    - 組み込みシステムの管理

- VisualStudioCode
    - ローカル環境
    - 自分でプログラムを書いたり変更したりする際に使用

  
- - - 
### <u>GitHubとVScodeの連携の仕方</u>

gitの流れと合わせて以下にコマンドを示す。

```mermaid

gitGraph

  commit id: "clone"

  branch local

  checkout local

  commit id: "branch1"

  commit id: "編集"

  branch staging_area

  commit id: "add"

  commit id: "commit"

  checkout main

  merge staging_area

  commit id: "push"

  commit id: "approve"

  commit id: "merge"

  branch local2

  checkout local2

  commit id: "pull"

  commit id: "branch2"

  commit id: "編集2"

```

#### <u>1.clone</u>

- クローン：リモートのファイルをローカルにコピーすること。

- 一度行えば基本的にそれ以降使うことはない(はず)

- SSh接続でのcloneの仕方は、`git clone git@github.com:(アカウント・organization名)/(リポジトリ名)`でclone出来ます。(リポジトリを開くと右上に出てる**<>Code▼**という緑のボタンからgitのリンクをコピーすることもできます。)

  

#### <u>2.branch</u>

- ブランチ：mainを直接編集して問題が起きるのを避けるための編集用の分岐先。

- 編集の都度立てる必要がある。(詳しくは後述するMergeと合わせて説明)

- `git branch`：現在ローカルに存在するbranchの確認・自分がいるbranchの確認ができる。

- `git branch -r`：現在リモートに存在するbranchの確認ができる。

- `git branch (ブランチ名)`：新しくブランチを切る。
(※branchを新たに作ることをbranchを***切る**といいます。)  ブランチの名前については、上手い名前の付け方を模索してほしいところでありますが、候補をあげておきます。  

1. main>daveloped>featureの順に階層を分ける。
この場合、それぞれの役割は次のようになります。  
main：全体のプログラムで確実に動くbranch  
developed：各系や機能ごとに確実に動くbranch  
feature：各系や機能ごとに編集するためのbranch  
featureのみ、Merge(後述)するごとに削除。

```mermaid

gitGraph

  commit id: "first"

  branch developed

  checkout developed

  commit id: "COMMIT-0"

  branch feature1

  branch feature2

  checkout feature1

  commit id: "COMMIT-1"

  commit id: "COMMIT-2"

  commit id: "COMMIT-3"

  checkout developed

  merge feature1

  checkout feature2

  commit id: "COMMIT-4"

  commit id: "COMMIT-5"

  checkout developed

  merge feature2

  checkout main

  merge developed

  commit id: "COMMIT-6"

```

2. 命名の仕方を統一する。  
大まかに何を編集する・まとめているbranchなのかを明記します。また、誰が編集しているかを分かるようにしておくのも大事。  
例)main_future  
developed_GPSRUN_shiota  
feature_motordriver_shiota  
(命名の長さと分かりやすさのトレードオフだと考えています。私たちも実践できていたわけではないので、Mission4に限ってはあくまで提案という形に留めて、次回以降のミッションの際には確定させてもらえるとうれしいです。)

  

- `git checkout (ブランチ名)`：ブランチの移動をする。  
**注意**  
これをしてブランチの移動をしないとブランチを切った意味が無いので気を付けてください。  

  

#### <u>3.add</u>
- `git add (ファイル名)`：作業ディレクトリ内の任意のファイルの変更(編集)をステージエリア(ステージングエリア)に移動させる。  
gitはその階層的に、ローカルからリモートに戻す際に、ステージエリアを間に挟む必要があります。
- `git add .`：作業ディレクトリ全ての変更をaddできる。

  

#### <u>4.commit</u>

- `git commit -m 'コミットメッセージ'`：ローカル内のリポジトリに変更を記録する。  
まだ、外部に公開されているわけではなく、そのあとのpush(後述)でリモートにpull request(後述)を送ることが出来ます。  
コミットメッセージの付け方について、何を変更したのか分かるようなメッセージを付けてください。また、commitを二つ以上まとめてpushするとコミットメッセージが残らない現象が確認されています。commitの度にpushするようにしてください。  
例）git commit -m 'GPSの計算方法に誤りがあったので修正しました'  
※GitHubに長けている知り合いはコミットメッセージを考えてから作業しろって言ってました。

  

#### <u>5.push</u>

- `git push origin (変更先ブランチ名)`：(変更先のランチ)にcommitした内容を反映したり、pull requestを送る。FUSiONのリポジトリでは後者を採用しています。  
これまではローカルの中で完結していましたが、この操作を行うことでようやくリモートでの作業に移ります。

  

#### <u>6.Pull requestのapprove/Merge</u>

これはリモート(GitHub)上での作業になります。  

- approve(pushの承認)  
GitHubのリポジトリに入った後、Pull requests>(任意のpull request)>File changedと画面を遷移していくと、他のメンバーが行った変更内容(pushの内容)を確認することが出来ます。追加した項目は緑の、削除した項目は赤の網掛けになっています。  
同ページの右上に緑の**Review changes▼**というボタンをクリックすると、ポップアップが表示され、approveにチェックを入れて**Submit review**をクリックすると承認できます。  
基本的に動作を確認してpushをするべきですが、誰かがダブルチェックしてそれを反映させるためにこの操作を行います。  

  

- Merge(pushの反映)  
上記のapproveが終わった後、Mergeという作業を行います。  
これは、各個人が編集してpushした内容をリモートのリポジトリに反映させるための作業で、これが編集を反映させる最後の過程になります。  
Pull requestsに戻って、**Merge pull request**を押します。  
その後、**Confirm merge**を押すと、変更がリポジトリ全体に反映されます。  
リポジトリに戻ってリロードすると更新時間とコミットメッセージが表示され、ファイルの中身も書き変わっています。

  

- branchの削除  
Mergeが終わった後、変更が済んだbranchは削除するとGitHubが整理されて見やすくなります。branchのところでも簡単に説明しましたが、先述のbranchの命名法を採用する場合は、featureのみMergeして削除すればいいかと思います。

  

#### <u>7.pull</u>

- `git pull origin (リモートブランチ名):(ローカルブランチ名) `：リモートリポジトリの変更をローカルリポジトリの任意のブランチに反映させる。  
他のメンバーが加えた変更を自分が作業するのに使うこともあると思いますので、これは人の更新の度に行うことをおススメします。

  

---

## 最後に

GitHubは使えるようになると楽しいと思います。  

ぜひ使えるようになってほしいです。

  

---

## 便利なGitHubの機能あれこれ

必須では無いけどこれ使えるようになるとGitHubをもっと上手く使えるという機能たちをご紹介します。  
[GitHubを最強のToDo管理ツールにする](https://qiita.com/o_ob/items/fd45fba2a9af0ce963c3)