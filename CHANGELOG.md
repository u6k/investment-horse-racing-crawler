# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.5] - 2023-07-05
### Fixed
- [#10000: KeyError: 'betting_type'エラーが出る](https://redmine.u6k.me/issues/10000)
- [#10001: TypeError: string indices must be integers^](https://redmine.u6k.me/issues/10001)

## [5.0.4] - 2023-06-20
### Fixed
- [#9979: jockey_id, trainer_idに英文字が入るとパースエラーになる](https://redmine.u6k.me/issues/9979)

## [5.0.3] - 2023-05-12
### Fixed
- [#9953: RaceInfoItemに出走日データが無い](https://redmine.u6k.me/issues/9953)
- [#9950: 騎手リンクのパースがエラーになる](https://redmine.u6k.me/issues/9950)
- [#9954: 調教師リンクのパースがエラーになる](https://redmine.u6k.me/issues/9954)
- [#9955: 存在するはずのオッズデータが無いことがある](https://redmine.u6k.me/issues/9955)

## [5.0.2] - 2023-05-06
### Fixed
- [#9949: 枠連オッズの取得がエラーになることがある](https://redmine.u6k.me/issues/9949)

## [5.0.1] - 2023-05-06
### Fixed
- [#9948: `bin/crawl.sh`の実行がパーミッション不足でエラー](https://redmine.u6k.me/issues/9948)

## [5.0.0] - 2023-05-06
### Added
- [#9911: Scrapyプロジェクトを新規構築して、カレンダーページのみスクレイピングする](https://redmine.u6k.me/issues/9911)
- [#9913: コードフォーマット、Lintチェックを実行する](https://redmine.u6k.me/issues/9913)
- [#9912: 簡単なテストを実装する](https://redmine.u6k.me/issues/9912)
- [#9914: キャッシュをS3に保存する](https://redmine.u6k.me/issues/9914)
- [#9921: tor経由でスクレイピングする](https://redmine.u6k.me/issues/9921)
- [#9916: カレンダーページを起点として、全ページをスクレイピングする](https://redmine.u6k.me/issues/9916)
- [#9915: スクレイピング結果をS3に出力する](https://redmine.u6k.me/issues/9915)

### Changed
- [#9910: パッケージ管理をPoetryに移行する](https://redmine.u6k.me/issues/9910)
- [#9923: poe installにwithoutオプションを指定する](https://redmine.u6k.me/issues/9923)

## [4.0.4] - 2021-11-20
### Fixed
- [#9258: payoff_typeに単勝、馬連が存在しない](https://redmine.u6k.me/issues/9258)

## [4.0.3] - 2021-09-30
### Changed
- DELAYを短縮した

## [4.0.2] - 2021-09-30
### Fixed
- [#9229: crawl.shに実行権限が付いていない](https://redmine.u6k.me/issues/9229)
- [#9230: RacePayoffItemのDB格納でエラーになることがある](https://redmine.u6k.me/issues/9230)

## [4.0.1] - 2021-09-28
### Fixed
- [#9228: build and pushで構築されたイメージが開発用Dockerfileを基にしている](https://redmine.u6k.me/issues/9228)

## [4.0.0] - 2021-09-27
### Added
- [#9227: 祖先馬のデータを取得する](https://redmine.u6k.me/issues/9227)
- [#8411: レース結果から、着差・上がり3ハロンを取得する](https://redmine.u6k.me/issues/8411)

### Changed
- [#9111: CIをGitHub Actionsに、コンテナレジストリをGitHub Container Registryに移行する](https://redmine.u6k.me/issues/9111)
- [#9104: クローラー仕様をlocal-horse-racingに合わせる](https://redmine.u6k.me/issues/9104)

## [3.4.2] - 2020-05-22
- Travis CIで`docker push`が失敗した
    - `after_script`でコンテナ・イメージをビルドしているが、それより先に実行される`after_success`で`docker push`をしようとしていた

## [3.4.1] - 2020-05-22
- Travis CIで`after_script`がエラーになった
    - `git clean -xdf`が権限不足で失敗したため、`sudo`を付与した

## [3.4.0] - 2020-05-22
### Changed
- [#8458: APIでレース情報を返す](https://redmine.u6k.me/issues/8458)

## [3.3.0] - 2020-05-22
### Changed
- [#8444: 引数を整理する](https://redmine.u6k.me/issues/8444)
- [#8284: 次のパース移譲は集約して行う](https://redmine.u6k.me/issues/8284)
- [#8443: 投票・清算ジョブのスケジューリングは、クローラーではなくジョブ管理側で行う](https://redmine.u6k.me/issues/8443)

## [3.2.0] - 2020-05-17
### Fixed
- [#8425: 想定した出馬表とは違うページがスクレイピングされてしまう](https://redmine.u6k.me/issues/8425)
- [#8426: 当日レースのジョブ・スケジューリングで、1レースしか登録されなかった](https://redmine.u6k.me/issues/8426)

## [3.1.0] - 2020-05-10
### Changed
- [#8394: Flaskアプリに変更して、ジョブ登録はFlaskで定義したWebAPIで受け付ける](https://redmine.u6k.me/issues/8394)
    - いろいろとFlaskアプリになりきれていなかったため

### Added
- [#8185: 毎日10:00にクロールを開始して、当日の全レース情報を取得して、投票処理を予約実行する](https://redmine.u6k.me/issues/8185)

## [3.0.1] - 2020-04-26
### Fixed
- [#8299: 本番コンテナの起動が失敗した](https://redmine.u6k.me/issues/8299)

## [3.0.0] - 2020-04-26
### Added
- [#8266: Flaskアプリに変更して、ジョブ登録はFlaskで定義したWebAPIで受け付ける](https://redmine.u6k.me/issues/8266)
- [#7878: キャッシュ有効期限をページによって変える](https://redmine.u6k.me/issues/7878)

## [2.8.0] - 2020-03-15
### Changed
- [#8040: 払い戻し、オッズ情報を、単勝・複勝以外も取得する](https://redmine.u6k.me/issues/8040)

## [2.7.0] - 2020-02-17
### Fixed
- [#7987: 人気順に"-"が入ることがある](https://redmine.u6k.me/issues/7987)
- [#7988: bracket_numberに"-"が入ることがある](https://redmine.u6k.me/issues/7988)

## [2.6.0] - 2020-02-08
### Fixed
- [#7980: 出馬表でtrainer_idが存在しない場合がある](https://redmine.u6k.me/issues/7980)
- [#7981: prize_total_moneyには小数点が入る](https://redmine.u6k.me/issues/7981)
- [#7982: breederが存在しない場合がある](https://redmine.u6k.me/issues/7982)
- [#7983: 騎手の誕生日が存在しない場合がある](https://redmine.u6k.me/issues/7983)

## [2.5.0] - 2020-02-05
### Fixed
- [#7916: 本番用コンテナに".env"が含まれているため、Dockerコンテナに設定した環境変数ではなく".env"が使われてしまう](https://redmine.u6k.me/issues/7916)
- [#7918: キャッシュあるなしログを揃える](https://redmine.u6k.me/issues/7918)
- [#7961: horseのgenderに想定外の文字列が混入している](https://redmine.u6k.me/issues/7961)
- [#7915: jockey_weightに想定外の文字列があり、変換に失敗する](https://redmine.u6k.me/issues/7915)
- [#7873: Scrapyの設定を見直す](https://redmine.u6k.me/issues/7873)
- [#7967: boto3のログを抑止する](https://redmine.u6k.me/issues/7967)
- [#7968: odds_place_max, odds_place_min, odds_winの'****'は無視する](https://redmine.u6k.me/issues/7968)
- [#7969: resultが空の場合に対応する](https://redmine.u6k.me/issues/7969)
- [#7970: arrival_timeが1分未満の場合に対応する](https://redmine.u6k.me/issues/7970)
- [#7973: RacePayoffItemに複勝の値が入らないことがある](https://redmine.u6k.me/issues/7973)
- [#7972: RacePayoffItemに変な値が入る場合がある](https://redmine.u6k.me/issues/7972)
- [#7971: RaceResultItemにoddsが含まれない場合がある](https://redmine.u6k.me/issues/7971)

### Added
- [#7962: 出馬表もパースする](https://redmine.u6k.me/issues/7962)

## [2.4.0] - 2020-01-25

### Added

- [#7882: 単勝・複勝の予測に必要なデータを収集する](https://redmine.u6k.me/issues/7882)

## [2.3.0] - 2020-01-14

### Added

- [#7872: Spiderのパース処理をテストする](https://redmine.u6k.me/issues/7872)

## [2.2.0] - 2020-01-13

### Added

- [#7876: 単勝・複勝の予測に必要なデータを収集する](https://redmine.u6k.me/issues/7876)

## [2.1.0] - 2020-01-13

### Added

- [#7874: キャッシュをS3に、出力データをDBに格納する](https://redmine.u6k.me/issues/7874)

## [2.0.0] - 2020-01-10

### Changed

- [#7851: Scrapyで最小限のページだけ収集するクローラーを再構築して、運用を再開する](https://redmine.u6k.me/issues/7851)

## [1.6.0] - 2019-05-21

### Changed

- [#7057: パースする時、どのようなデータをパースするのかログ出力する](https://redmine.u6k.me/issues/7057)

## [1.5.0] - 2019-05-10

### Added

- [#7047: オッズをパースする](https://redmine.u6k.me/issues/7047)

## [1.4.0] - 2019-05-10

### Changed

- [#7069: crawlineを最新化する](https://redmine.u6k.me/issues/7069)

## [1.3.1] - 2019-05-07

### Fixed

- [#7045: lib/investment_horse_racing/crawler/parser/entry_page.rb:61 - undefined method `strip' for nil:NilClass (NoMethodError)](https://redmine.u6k.me/issues/7045)
- [#7046: lib/investment_horse_racing/crawler/parser/result_page.rb:20 - can't convert nil into an exact number (TypeError)](https://redmine.u6k.me/issues/7046)

## [1.3.0] - 2019-05-02

### Changed

- [#7031: ロガーの名前をAPP_LOGGER_xxxに変更する](https://redmine.u6k.me/issues/7031)
- [#7021: 再ダウンロード判定から、最近ダウンロードしたから再ダウンロードしない、という条件を除去する](https://redmine.u6k.me/issues/7021)
- [#7036: horse、trainer、jockeyページをダウンロードしない](https://redmine.u6k.me/issues/7036)
- [#7033: パーサー・テストの前提条件設定で、WebMockで初期化する](https://redmine.u6k.me/issues/7033)
- [#7039: データ保存をバルク・インサートで行う](https://redmine.u6k.me/issues/7039)

## [1.2.0] - 2019-05-01

### Added

- [#7035: DBデータ保存時にデバッグ・ログを出力する](https://redmine.u6k.me/issues/7035)

## [1.1.0] - 2019-04-30

### Added

- [#6839: レース情報をDBに格納する](https://redmine.u6k.me/issues/6839)

## [1.0.0] - 2019-04-25

### Changed

- [#7002: scoring-horse-racingプロジェクトをinvestment-horse-racingプロジェクトにリネームする](https://redmine.u6k.me/issues/7002)

## [0.7.0] - 2019-03-27

### Added

- [#6840: コマンド引数にクロール開始URLを指定する](https://redmine.u6k.me/issues/6840)
- [#6843: サブコマンドのオプションに、できるだけデフォルト値を設定する](https://redmine.u6k.me/issues/6843)

## [0.6.0] - 2019-03-22

### Fixed

- [#6761: HorsePage、JockyPage、TrainerPageの再ダウンロードを、「前回ダウンロードから1ヶ月以降なら再ダウンロードする」とする](https://redmine.u6k.me/issues/6761)
- [#6854: 全ページにおいて、前回ダウンロード時刻が1日以内の場合は再ダウンロードしない、とする](https://redmine.u6k.me/issues/6854)

## [0.5.1] - 2019-03-20

### Fixed

- [#6851: crawlineの最新バージョンを適用する](https://redmine.u6k.me/issues/6851)
    - crawlコマンドを実行したところエラーになったので、対応するとともにコマンドのテストを記述しました

## [0.5.0] - 2019-03-20

### Fixed

- [#6851: crawlineの最新バージョンを適用する](https://redmine.u6k.me/issues/6851)

## [0.4.0] - 2019-03-17

### Added

- [#6841: 本番用のDockerイメージを構築する](https://redmine.u6k.me/issues/6841)

## [0.3.0] - 2019-03-11

### Added

- [#6760: トップページからすべてのページをクローリングできるようにパーサーを構築する](https://redmine.u6k.me/issues/6760)

## [0.2.0] - 2019-03-11

### Added

- [#6833: コマンドでレース・リスト・ページをクロールする](https://redmine.u6k.me/issues/6833)

## [0.1.0] - 2019-03-08

### Added

- [#6740: CLIアプリに変更する](https://redmine.u6k.me/issues/6740)
  - Railsアプリケーションとして実装していましたが、常駐プロセスにするする意味はないので、gemによるCLIアプリケーションに変更しました
- [#6735: 共通処理をcrawlineに切り出して、crawlineベースで再実装する](https://redmine.u6k.me/issues/6735)
  - クローラーごとに少しずつ異なる処理を実装していましたが、それらをcrawlineに集約して、crawlineをベースに再実装しました
- [#6829: コマンドでスケジュール・リスト・ページをクロールする](https://redmine.u6k.me/issues/6829)
