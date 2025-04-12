# 中央競馬データ・クローラー _(investment-horse-racing-crawler)_

[![build](https://github.com/u6k/investment-horse-racing-crawler/actions/workflows/build.yml/badge.svg)](https://github.com/u6k/investment-horse-racing-crawler/actions/workflows/build.yml)
[![license](https://img.shields.io/github/license/u6k/investment-horse-racing-crawler.svg)](https://github.com/u6k/investment-horse-racing-crawler/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/u6k/investment-horse-racing-crawler.svg)](https://github.com/u6k/investment-horse-racing-crawler/releases)
[![WebSite](https://img.shields.io/website-up-down-green-red/https/shields.io.svg?label=u6k.Redmine)](https://redmine.u6k.me/projects/investment-horse-racing-crawler)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> 競馬投資に使用するデータ(中央競馬データ)を収集する

## Install

Dockerを使用します。

```
$ docker version
Client:
 Version:           18.09.5
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        e8ff056dbc
 Built:             Thu Apr 11 04:44:28 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.5
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.8
  Git commit:       e8ff056
  Built:            Thu Apr 11 04:10:53 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```

`docker pull`します。

```
docker pull ghcr.io/u6k/horse-racing-crawler
```

前提

- S3 (またはS3互換ストレージ)
- RabbitMQ

コンポーネント構成、環境変数などは[docker-compose.yml](https://github.com/u6k/investment-horse-racing-crawler/blob/main/compose.yml)を参照してください。

## Usage

待ち受けを開始する。環境変数でS3接続やRabbitMQ接続を設定する。

```
docker run --rm ghcr.io/u6k/horse-racing-crawler
```

キューに次のようなJSONデータを投入すると、クロールを開始する。`start_url`はクロール開始URL、それ以外はクロールプロセスへの環境変数を指定する。

開発はDev Containerで行う。

Lintチェックを実行する。

```
poe lint
```

フォーマッターを実行する。

```
poe fix
```

## Other

最新の情報は、[Wiki - investment-horse-racing-crawler - u6k.Redmine](https://redmine.u6k.me/projects/investment-horse-racing-crawler/wiki/Wiki)を参照してください。

## Maintainer

- u6k
    - [Twitter](https://twitter.com/u6k_yu1)
    - [GitHub](https://github.com/u6k)
    - [Blog](https://blog.u6k.me/)

## Contributing

当プロジェクトに興味を持っていただき、ありがとうございます。[既存のチケット](https://redmine.u6k.me/projects/investment-horse-racing-crawler/issues/)をご覧ください。

当プロジェクトは、[Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct)に準拠します。

## License

[MIT License](https://github.com/u6k/investment-horse-racing-crawler/blob/master/LICENSE)
