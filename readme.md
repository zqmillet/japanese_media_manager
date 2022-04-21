# Japanese Media Manager

![license](https://img.shields.io/badge/license-MIT-green)
![pytest](https://github.com/zqmillet/japanese_media_manager/actions/workflows/pytest.yml/badge.svg)
![pylint](https://github.com/zqmillet/japanese_media_manager/actions/workflows/pylint.yml/badge.svg)
![flake8](https://github.com/zqmillet/japanese_media_manager/actions/workflows/flake8.yml/badge.svg)
![mypy](https://github.com/zqmillet/japanese_media_manager/actions/workflows/mypy.yml/badge.svg)
[![codecov](https://codecov.io/gh/zqmillet/japanese_media_manager/branch/main/graph/badge.svg?token=XV3ZZ6JX15)](https://codecov.io/gh/zqmillet/japanese_media_manager)
[![Documentation Status](https://readthedocs.org/projects/japanese-media-manager/badge/?version=latest)](https://japanese-media-manager.readthedocs.io/zh_CN/latest/?badge=latest)

Japanese Media Manager (以下简称 jMM) 是一款用于刮削十一区多媒体的命令行工具.

## 目录

<!-- vim-markdown-toc GFM -->

* [支持的在线数据库](#支持的在线数据库)
* [快速开始](#快速开始)
    * [环境需求](#环境需求)
    * [安装](#安装)
    * [使用方式](#使用方式)
* [如何贡献](#如何贡献)
* [版权说明](#版权说明)
* [鸣谢](#鸣谢)
* [ToDo](#todo)

<!-- vim-markdown-toc -->

## 支持的在线数据库

| 在线数据库 | 爬虫地址 | 单元测试 |
| --- | --- | --- |
| [JavBus](https://www.javbus.com/) | `jmm.crawlers.JavBusCrawler`   | ![javbus](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_javbus.yml/badge.svg)     |
| [JavBooks](https://jmvbt.com/)    | `jmm.crawlers.JavBooksCrawler` | ![javbooks](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_javbooks.yml/badge.svg) |
| [JavDB](https://www.javdb36.com/) | `jmm.crawlers.JavDBCrawler`    | ![javdb](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_javdb.yml/badge.svg)       |
| [AirAV](https://cn.airav.wiki/)   | `jmm.crawlers.AirAVCrawler`    | ![airav](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_airav.yml/badge.svg)       |
| [Arzon](https://www.arzon.jp/)    | `jmm.crawlers.ArzonCrawler`    | ![arzon](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_arzon.yml/badge.svg)       |
| [Avsox](https://avsox.monster/)   | `jmm.crawlers.AvsoxCrawler`    | ![avsox](https://github.com/zqmillet/japanese_media_manager/actions/workflows/crawler_avsox.yml/badge.svg)       |

## 快速开始

### 环境需求

- 操作系统: Windows, Linux, MacOS[^1].
- Python: 3.7 以及 3.7 以上版本.

### 安装

在控制台中运行以下命令.

``` bash
pip install jmm
```

安装好之后系统中增加 `jmm` 命令, 在控制台中输入 `jmm version`, 如果输出当前版本号, 则说明 jMM 安装成功.

### 使用方式

本项目的用户手册托管于 [readthedocs.org](https://readthedocs.org/), 详细使用方式详见[此链接](https://japanese-media-manager.readthedocs.io/zh_CN/latest/?badge=latest).

## 如何贡献

本项目是个人项目, 我非常欢迎大家对一起完善 jMM, 你可以通过以下方式为 jMM 添砖加瓦.

- 报告 Bug;
- 对代码进行 Review, 发现代码中的缺陷;
- 对已有的 Bug 进行修复;
- 为 jMM 添加新特性;
- 维护 jMM 的代码.

## 版权说明

本项目签署了 MIT 授权许可, 详情请参阅 [LICENSE](LICENSE) 查看详细信息.

## 鸣谢

本项目参考了 [AVDC](https://github.com/moyy996/AVDC) 以及 [Movie_Data_Capture](https://github.com/yoshiko2/Movie_Data_Capture). 它们是非常优秀的刮削工具, 给了我非常多的灵感.

## ToDo

- [ ] 支持 ``-cdx`` 格式的媒体.

[^1]: 理论上, jMM 可以运行在任何可以执行 Python3 的才做系统, 我只在这 3 个系统中测试过 jMM, 其他系统不保证可以运行.
