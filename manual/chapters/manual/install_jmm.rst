安装 jMM
========

首先安装 Python 3.7 以及以上版本, 然后利用以下命令安装 jMM.

.. bash::
   :norun:

    pip3 install jmm

安装好之后, 系统中会存在一个 ``jmm`` 命令, 可以利用 ``jmm -h`` 来查看 ``jmm`` 的命令手册.

.. bash::
   :real_cmd: {python} -m jmm -h

    jmm -h

如果出现以上提示信息, 则说明 jMM 安装成功.

.. bash::
   :real_cmd: {python} -m jmm valid-config -n star-325

    jmm valid-config -n star-325
