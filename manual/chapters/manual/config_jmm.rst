配置 jMM
========

安装了 jMM 后, 可以直接使用. 如果想添加代理或者想添加第三方爬虫库, 可以对 jMM 进行进一步配置.

首先, 使用 ``jmm generate-config`` 命令产生用户自定义配置文件 ``.jmm.cfg``, 该文件会产生在你的 HOME 目录中.

.. bash::
    :real_cmd: {python} -m jmm generate-config --force

    jmm generate-jmm

默认的配置文件的格式如下所示.

.. literalinclude:: ../../../jmm/.config.yaml
