单元测试
========

jMM 有完善的单元测试用例, 保证在持续迭代过程中不引入 BUG. jMM 使用的测试框架为 pytest, 且测试用例代码覆盖度 100%.

首先安装 jMM 测试所依赖的库.

.. bash::
   :norun:

   pip3 install -r testcases/requirements.txt

然后你可以使用如下命执行 jMM 的单元测试用例.

.. bash::
   :norun:

   pytest testcases


当前版本单元测试结果为:

- 是否通过单元测试: |pytest_badge|
- 代码覆盖度: |codecov_badge|

.. |pytest_badge| image:: https://github.com/zqmillet/japanese_media_manager/actions/workflows/pytest.yml/badge.svg
.. |codecov_badge| image:: https://codecov.io/gh/zqmillet/japanese_media_manager/branch/main/graph/badge.svg?token=XV3ZZ6JX15
