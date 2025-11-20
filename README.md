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

## Usage

クローラーを起動する。

```bash
docker compose up
```

RabbitMQからメッセージを受信してクロールを開始する。MQに投入するメッセージは以下の形式。

```
{
"start_url": "https://race.netkeiba.com/top/race_list_sub.html?kaisai_date=20230318",
"AWS_S3_FEED_URL": "s3://horse-racing/feed/calendar/calendar_20230318.json",
"RECACHE_RACE": "True",
"RECACHE_DATA": "False"
}
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
