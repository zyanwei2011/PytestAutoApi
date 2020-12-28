### 框架概述
+ 本文档接口范围为HTTP接口，适用于前后关联的业务接口和单个无关联的接口场景。暂不支持dubbo接口。
+ python3 + pytest + HTTP +  + Yaml

### 目录结构
```
├── Common          公共代码，包含数据读取、日志封装、文件转换、请求发送等公共方法封装
├── Config              配置文件，包含文件路径、数据库连接等配置项文件
├── Outputs           测试输出，包含日志、报告、截图等测试成果产物
├── ApiReq             接口逻辑处理，对单独接口请求和业务流接口请求进行封装，方便用例层调用
├── TestCase         测试用例（业务层），自动化用例脚本存放位置
├── TestData          测试数据，接口请求相关数据
├── conftest.py     测试用例前置后置文件，如登陆、退出
├── main.py           项目主文件
├── pytest.ini         pytest运行配置文件，解决测试用例打标后运行警告问题（@pytest.mark.smoke  PytestUnknownMarkWarning）,当存在警告时，可在该文件进行配置
├── Readme          项目介绍文件
└── requirements.txt         测试依赖包安装文件
```
### 数据处理
+ 登陆态处理

Cookies作为参数传入
```python
res = requests.post(url, data=data, headers=headers，cookies=Cookie)
```
cookies放在header
```python
headers = {"Cookie": Cookies, "User-Agent": "*"} 
r = requests.post(url, data=data, headers=headers)
```
使用requests.Session()方法
```python 
r = requests.Session()
# 当存在cookies时，使用r.cookies['cookie'] = Cookie,不存在cookies，使用r.request直接去登陆，登陆成功后登陆态信息即保存在r中。
res = r.post(url, data=data, headers=headers)
```
+ 接口关联处理

>+ 方法1: 接口处理层，直接将上一接口的返回作为下一个接口的入参
>+ 方法2: 将部分数据存储为全局变量或者类变量
>+ 方法3: 持久到文件或数据库中

+ 前置后置

pytest在根目录下conftest.py文件防治前置后置
```
@pytest.fixture(scope='session', autouse=True)    # 设置前置范围，该文件使用不需要引入

@pytest.mark.usefixtures('函数名')          # 不需要将前置返回结果需要作为参数传入时使用

def demo(func)：                    #当需要前置的返回作为参数时，直接在将函数名作为参数传入  
  r = func()
```
+ 参数化
```
@pytest.mark.parametrize('a, b', [(1, 2),(3, 4)])            #装饰器进行参数化

```
+ 运行

pytest支持命令行运行模式，可在pytest.ini中配置，直接点击main.py文件或命令行输入pytest运行即可

pytest支持使用pytest.main(['-m smoke',...])方式运行，但该运行方式的部分参数无法被系统sys.args方法获取，导致无法获取自定义变量。`不建议使用`。
```
-v 说明：可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等
-s 说明：控制台输出我们用例中的调式或log信息
-m ”标记“ 说明：执行特定的测试用例。我们再次修改一下我们的用例，并添加一个新的用例
-k "关键字" 说明：执行用例包含“关键字”的用例
-q 说明：简化控制台的输出
-x 说明：遇到错误时停止运行
-n m 说明：m个CPU或终端并行执行(插件pytest-xdist)
-x --maxfail=n 说明：当错误数达到n个时停止运行(pytest-rerunfailures )
--reruns 2 说明：运行失败后立即重运行n次
--reruns-delay 5 说明：每次重运行间隔n秒
```


+ 自定义命令行参数

```python
def pytest_addoption(parser):
    """
    # 自定义测试环境参数
    :param parser:
    :return:
    """
    parser.addoption("--env", action="store", default="test",
                     help="env: test environment, such as production, prerelease, test. Detail refer to env.py")

```

+ 测试报告

allure插件(略)






