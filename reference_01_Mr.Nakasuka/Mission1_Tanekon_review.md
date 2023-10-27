# Mission1　種子島ロケットコンテスト　レビュー
ここから中須賀先生によるFUSiONに対するレビューがスタートしました。
ここではMission1の種子島ロケットコンテストにおけるPDRおよびCDRで得たレビューを系ごとにまとめます。　　
※各項目の→の後は実際にFUSiONが行おうとした対策です。参考までに。

## PDR
### 全体

- [ ] 実験は河川敷と橋で実験する。橋の欄干から機体とパラシュートを落とす。
  
- [ ] 当日何回実験できるのか確認する。ARLISSは2回(大会当日に伸ばせる)→大会本部に確認
 
- [ ] 画像送るのどれくらいかかるの？→数秒 画質を落とすなど対策が必要

- [ ] 通信途絶えたらやばくない？シングルフェイラーは危険→GPSまでの処理をオンボードでやる（ここまでは通信なしで進める）

- [ ] コーン背景の明るさにも注意。画像処理では逆光が怖い。

- [ ] スタック処理については逆走OKとか数種類用意しておく→20パターンくらい
下がるだけでなく、回るなど。バラエティ勝負、みんなたくさん用意する

- [ ] コーンの詳細情報を調べる→大会からできるだけ詳細な情報を得る

- [ ] 草の高さを代えて走行実験する


### 構体系
- [ ] 走行困難パターン(スタック対策)を10〜20個用意していく。ここが多いとかなり信頼性が高い

- [ ] 上空からの機体の落下について：3割は落下で壊れる、特に風が吹いている時は斜めから落ちるかもしれない。
横向きに速度が付いたときにバウンドして故障しやすい。
着陸時の衝撃を和らげるために、エンベロープで包んだら？→採用（飛行系の構造も更新）

- [ ] 3Dプリンタ作るならすべて3Dプリンターで作った方がいい→サンドウィッチ構造？？

- [ ] 実はマイコン部分などは構造的にあまり壊れない（ぶつからないから）
- [ ] スタビライザーは前進と後退のどちらにもあるとよい


### 駆動系
- [ ] 実際のサイズ、実際の路面状況（色んな芝生の状況）を想定して、実験を行う。
- [ ] 着陸時にタイヤに地面が与える撃力により、シャフトが曲がる(これはガチ)
- [ ] 走る時のパワー（電力）が強いことが、重要要件。これで、多少の緊急事態はカバーできる。
- [ ] 実験するときに変える条件は、ギヤの歯の高さ
- [ ] ギヤの歯のみ、材質をゴムにするのはあり、ギアの高さ調節にうってつけ
- [ ] 走行方向は両方に出来るとよい。


### 制御系
- [ ] GPSに影響を及ぼすものにはアルミを巻く・静電遮蔽（接地も忘れずに）
↑1.57GHzの1/nの電波を使うと干渉が生じる
- [ ] 轍や草むらにはまったときなどコンティンジェンシープランを10~20個用意する(いわゆるスタック対策)
- [ ] 三角関数を利用すると処理が遅くなるので1対1対応のテーブルを用意する
- [ ] ディープスリープの利用（電源系の計算次第。走行開始までの消費電力削減）
- [ ] 自分の磁気で地磁気が狂うことがある（今回は考える必要はなさそう）

### センサ系
- [ ] GPSのアンテナを安定して上向きに
- [ ] GPSは一体型なのね、別でアンテナつけた方がいいかも
- [ ] GPSの向きがコロコロ変わるとロックがかからない、落下最中にロックかけたいなら気をつけて
- [ ] GPSの目指す制度精度20m→5mくらいの方が良いんじゃない？

### 電源系
- [ ] ニクロム線かなり電力くうから考慮せよ
- [ ] バッテリー容量余裕持っておいてね

### 通信系
- [ ] 地上局に画像を送るのに何秒かかるか計算せよ。もしその通信が途絶えたら何にもならない。
　
### 画像系
- [ ] 画角にコーンが入らなかったとき、どのようなストラテジーを取るか。複数パターン用意せよ。
- [ ] 逆光などの要因で画像を取得できないこともある
- [ ] 見た方向にコーンいないかもしれないからちゃんとカメラ回してね

### 飛行系
- [ ] 30mだと落下時間は7〜8秒だろう。この間で確実にパラシュートが開くように
- [ ] 摩擦や静電気で開かなくならないよう考慮する。100均の90cm四方で良いのがある
- [ ] パラシュートの上を歩く場合もあるかも、確率的に起こったら仕方ないと考えるのもひとつの手。リスクと確率のバランス。→まずパラシュートの上を機体が走る実験をするのがよいかも
- [ ] 打ち上げ前に気圧センサー設定してね。0mの設定。
- [ ] 広がりやすい、パラシュートのしまい方を調べる
- [ ] コンベックステープの導入→使用
- [ ] 落下スピードを考えろ→流される距離と故障体制のトレードオフ
- [ ] パラシュート切断のトリガーを複数用意する

## CDR
### 全体
※種子島ロケットコンテストは当時オンラインでのプレゼン勝負となることが決定した
- [ ] プレゼン3分は短い
- [ ] ビデオ撮りしてプレゼンに入れる  
・上から落としたフェーズも必要
・轍に入ったシーンもとる
・画像処理も
・それぞれ10秒ずつ→計40秒
・うまくいったのをつなぎ合わせる

- [ ] フェールセーフ: ミッションは達成できないが、次も使えるようにする 。故障しても継続できることが大事。
フェールオペラティブ→一部の機能を停止させるなどして、ミッションを遂行する
・ISSはワンフェールセーフトゥーフェールオペラティブ

- [ ] 中須賀先生去り際の一言「優勝しろよ」

### 駆動
- [ ] ひっくり返ったときにもとに返すプログラムを入れているチームもあった
→着陸時、ひっくり返った時どうするか：前進で元に戻るか確認。戻らなそうなら、画像を　反転させてそのままの状態でラジコン操作する。
- [ ] 機体の重心を下にする
- [ ] 落ちた時の衝撃を小さくするor落ちても強いシャフトを作る（エンベロープをいじる方が　簡単）
- [ ] 草に引っかかることが動作に影響があるのかどうかの検証が必要
- [ ] 走行中の振動でネジが緩む可能性がある:  
間にばねを入れる（ばねヒンジ）  
ネジの固定を強めるために、完成直前にロックタイトをしめる
- [ ] タイヤ幅が細い程、地面に埋まりやすくなる
- [ ] ネジにしるしをつけてネジがずれていないかの確認を知る（衛星でよくやる）
- [ ] 宇宙ステーションは一個の故障でも問題なく運用できる。二つの独立した故障でも壊滅的な破壊を防ぐ（セーフモードに切り替えられる）。
  衛星が死ぬ理由はバッテリーの枯渇。セーフモードに切り替えることでバッテリー温存。地球からの対策を待つワンフェールセーフ。完全に故障する前に対策を打つ。

### 制御
- [ ] 永久磁石の影響を考慮
- [ ] 接地したアルミ箔をモーターにかぶせても磁気が防げないので意味ない
- [ ] GPSのロックがかからない時はマイコンなどを静電遮蔽すると効果がある
- [ ] 9軸の誤差の原因が電流ループの影響なのであれば、遮蔽などの対応を考慮大事!!
- [ ] スタック判定20秒はいい塩梅じゃないか

### 電源
- [ ] ニクロム線は３秒間流れるので、電流の計算をする必要がある。(2)
- [ ] 降圧の発熱が結構大きい。
- [ ] モーターへの電流ラインとマイコンへの電流ラインが同じ → OK

### 飛行
- [ ] パラシュートについては問題なし
- [ ] エンベロープが重いので肉抜きしてもいいかも
- [ ] なみなみ緩衝材をやめてプチプチ三重巻きにするなど
- [ ] パラシュート展開について再現性が大事
- [ ] パラシュート切り離し後にパラシュートを巻き込可能性(仕方ないと思えるならいい)
### 通信
- [ ] 売りにしていいくらい面白い  
通信にかかる時間、画像を取得し制御するまでにかかる時間を計測
- [ ] 何で判断して操縦するのか。カメラかな
- [ ] 遠隔で送るときはピクセル数を減らして軽くする

















