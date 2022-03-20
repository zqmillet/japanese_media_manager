系统架构
========

jMM 的系统架构图如下所示.

.. tikz:: jMM 系统架构图

    \node[rectangle, fill=block, minimum width=14.5cm, minimum height=2.5cm, anchor=base, rounded corners] (utilities) at (3, 1.5 + 0) {};
    \node[rectangle, fill=block, minimum width=14.5cm, minimum height=2.5cm, anchor=base, rounded corners] (crawlers)  at (3, 1.5 + 3) {};
    \node[rectangle, fill=block, minimum width=14.5cm, minimum height=1.5cm, anchor=base, rounded corners] (router)    at (3, 1.0 + 6) {};
    \node[rectangle, fill=block, minimum width=14.5cm, minimum height=1.5cm, anchor=base, rounded corners] (io)        at (3, 1.0 + 8) {};
    \node[rectangle, fill=block, minimum width=14.5cm, minimum height=1.5cm, anchor=base, rounded corners] (cli)       at (3, 1.0 + 10) {};

    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (configuration)   at (0, 1.0 + 0) {Configuration};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (base_crawler)    at (4, 1.0 + 0) {BaseCrawler};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (translator)      at (0, 2.0 + 0) {Translator};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (session)         at (4, 2.0 + 0) {Session};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (image_processor) at (8, 2.0 + 0) {ImageProcessor};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (javdb)           at (0, 1.0 + 3) {JavDB};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (javbus)          at (4, 1.0 + 3) {JavBus};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (javbooks)        at (8, 1.0 + 3) {JavBooks};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (airav)           at (0, 2.0 + 3) {AirAV};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (arzon)           at (4, 2.0 + 3) {Arzon};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (avsox)           at (8, 2.0 + 3) {Avsox};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (routing_rule)    at (0, 1.0 + 6) {RoutingRule};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (crawler_group)   at (4, 1.0 + 6) {CrawlerGroup};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (media_finder)    at (0, 1.0 + 8) {MediaFinder};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (file_manager)    at (4, 1.0 + 8) {FileManager};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (media_finder)    at (0, 1.0 + 10) {generate-config};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (file_manager)    at (4, 1.0 + 10) {valid-config};
    \node[rectangle, fill=crawler, minimum width=3.5cm, minimum height=0.8cm, anchor=base] (file_manager)    at (8, 1.0 + 10) {scape};

    \node[font=\bf, minimum width = 2.3cm, anchor=base] at ([xshift=1.2cm]utilities.west) {Utilities};
    \node[font=\bf, minimum width = 2.3cm, anchor=base] at ([xshift=1.2cm]crawlers.west)  {Crawlers};
    \node[font=\bf, minimum width = 2.3cm, anchor=base] at ([xshift=1.2cm]router.west)    {Router};
    \node[font=\bf, minimum width = 2.3cm, anchor=base] at ([xshift=1.2cm]io.west)        {IO};
    \node[font=\bf, minimum width = 2.3cm, anchor=base] at ([xshift=1.2cm]cli.west)       {CLI};

整个系统架构分为 5 层, 分别是:

- CLI 层, 即 Command-Line Interface 命令行界面, 负责与用户进行指令交互, 在这一层提供了非常多的用户指令:

  - ``generate-config`` 用于配置 jMM.
  - ``valid-config`` 用于验证 jMM 配置.
  - ``scape`` 用于媒体刮削.

- IO 层, 提供文件的遍历, 复制, 重命名等功能.

  - :py:obj:`MediaFinder` 提供媒体文件发现功能.
  - :py:obj:`FileManager` 提供文件重命名, 转移等功能.

- Router 层, 根据番号进行路由, 将刮削的任务委托给不同的爬虫.

  - :py:obj:`RoutingRule` 管理路由规则, 将番号委托给不同的爬虫组完成刮削.
  - :py:obj:`CrawlerGroup` 将多个爬虫组合成一个爬虫组, 可以将刮削的元数据进行自动合并.

- Crawler 层, 提供 JavDB, JavBus, Arzon 等主流媒体资料在线数据库的爬虫.
- Utilities 层, 基础层, 提供系统所需的各种基础功能.

  - :py:obj:`BaseCrawler` 为所有爬虫的基类, 其定义了爬虫的行为以及接口. 如果你想爬取其他在线数据库网站, 你可以继承 :py:obj:`BaseCrawler` 并开发自己的爬虫, 并交给 Router 层来管理这些爬虫.
  - :py:obj:`Translator` 是百度翻译服务的 OOP 抽象, 用于将日语翻译成中文.
  - :py:obj:`Session` 为请求回话管理, 提供了 HTTP/HTTPS 代理, 错误重试, QPS 限制等一系列功能.
  - :py:obj:`ImageProcessor` 为图像处理单元, 提供 fanart 转 poster, 人脸识别等功能.
  - :py:obj:`Configuration` 为配置管理器, 用于系统默认配置以及用户自定义配置的管理与解析.

当使用 jMM 进行电影刮削时:

- 初始化 :py:obj:`MediaFinder` 并对指定的目录进行扫描, 获取所有待刮削的影片.
- 针对每一个影片:

  - 利用 :py:obj:`NumberExtractor` 模块从文件名中抽取番号.
  - 将番号交给 :py:obj:`Router` 进行路由, :py:obj:`Router` 针对自身的每个路由规则:

    - 判断番号与规则是否匹配, 如果不匹配采用继续匹配下一条路由规则.
    - 如果匹配, 则将番号委托给该条规则对应的爬虫组 :py:obj:`CrawlerGroup` 进行元数据获取, :py:obj:`CrawlerGroup` 将番号依次交给爬虫:

      - 爬虫获取该番号的元数据.
      - 判断是否完成爬取, 如果缺少字段, 继续交给下一个爬虫进行爬取, 如果所有字段都获取完毕, 则退出爬取过程.
    - 如果所有的规则都不匹配, 则抛出异常, 通知调用者无法找到影片的元数据.
  - 获取元数据, 将元数据委托给 :py:obj:`FileManager`,  :py:obj:`FileManager` 将元数据以及媒体文件按照 Infuse, Plex 等主流播放器格式进行存储.
  - 如果获取元数据失败, 则将失败信息写入日志.
