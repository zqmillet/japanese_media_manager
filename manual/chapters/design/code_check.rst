静态检查
========

jMM 采用 3 种静态检测工具, 分别是:

- pylint: 是一个 Python 代码分析工具, 它分析 Python 代码中的错误, 查找不符合代码风格标准(PEP8)和有潜在问题的代码.
- flake8: 是多种检测工具的集合, 在本项目中, 是作为 pylint 的补充, 有些时候, 可以检测出一些 pylint 检测不到的问题.
- mypy: 是 Python 的静态类型检查工具.

本项目 100% 遵守 PEP8 的标准, 且通过 mypy 的静态类型检查, 尽可能的保证代码中不存在低级逻辑错误.

当前版本静态检查结果为:

- |pylint_badge|
- |flake8_badge|
- |mypy_badge|

.. |pylint_badge| image:: https://github.com/zqmillet/japanese_media_manager/actions/workflows/pylint.yml/badge.svg
.. |flake8_badge| image:: https://github.com/zqmillet/japanese_media_manager/actions/workflows/flake8.yml/badge.svg
.. |mypy_badge| image:: https://github.com/zqmillet/japanese_media_manager/actions/workflows/mypy.yml/badge.svg
