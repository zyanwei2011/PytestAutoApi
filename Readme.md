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
