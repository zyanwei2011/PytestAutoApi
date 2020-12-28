import urllib3, requests, allure, json
from requests.exceptions import RequestException
from requests import Response
from Common.common_methods import func
from Common.get_api_data import GetData
from Common.logger import log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Request(object):
    def __init__(self, module, api_name, r=requests.Session(), **request_data):
        """
        初始化请求参数
        :param r:          登陆状态
        :param module:     自定义yaml文件名
        :param api_name:   自定义接口名称
        :param method: 发送方法
        optional 可选参数
        :param params: 发送参数-"GET"
        :param data: 发送表单-"POST"
        :param json: 发送json-"post"
        :param headers: 头文件
        :param cookies: 验证字典
        :param files: 上传文件,字典：类似文件的对象
        :param timeout: 等待服务器发送的时间
        :param auth: 基本/摘要/自定义HTTP身份验证
        :param allow_redirects: 允许重定向，默认为True
        :param proxies: 字典映射协议或协议和代理URL的主机名。
        :param stream: 是否立即下载响应内容。默认为“False”。
        :param verify: （可选）一个布尔值，在这种情况下，它控制是否验证服务器的TLS证书或字符串，在这种情况下，它必须是路径到一个CA包使用。默认为“True”。
        :param cert: 如果是字符串，则为ssl客户端证书文件（.pem）的路径
        :return: request响应
        """
        self.log = log
        self.r = r
        self.module = module
        self.api_name = api_name
        self.req = GetData(self.module, self.api_name)
        self.api_title = self.req.api_title
        self.header = self.req.request_header
        self.method = self.req.request_method.upper()
        self.url = self.req.request_url
        self.cookies = self.req.request_cookies
        self.data = self.req.request_data
        self.log.info("yaml文件读取参数: %s, %s, %s " % (module, api_name, self.data))
        self.log.info("测试用例层传入参数: %s, %s, %s " % (module, api_name, request_data))
        # 如果存在传参，则使用传入的参数
        if len(request_data) != 0:
            self.data = func.replace_dict_value(self.data, request_data)
        self.log.info("最终请求发送数据: %s, %s, %s, %s, %s, %s, %s " % (self.module, self.api_name, self.api_title,
                      self.url, self.header, self.method, self.data))

    def send_request(self):
        try:
            with allure.step("{}接口请求数据".format(self.api_name)):
                allure.attach(self.url, name="请求地址")
                allure.attach(self.method, name="请求方法")
                allure.attach(str(self.header), name="请求header")
                allure.attach(str(self.cookies), name="请求cookies")
                allure.attach(json.dumps(self.data, ensure_ascii=False), name="请求参数")
            # 处理文件上传数据，将文件路径转换为文件对象
            if self.data.get('files'):
                self.data['files'] = {'file': open(self.data.get('files'), 'rb+')}

            response = self.r.request(self.method, self.url, **self.data, cookies={'cookies': self.cookies},
                                      headers=self.header, verify=False)
            with allure.step("{}接口响应数据".format(self.api_name)):
                allure.attach(str(response.headers), "响应头")
                allure.attach(str(response.status_code), name="响应状态码")
                allure.attach(str(self.elapsed_time(response, fixed='ms')), name="响应时间(ms)")
                allure.attach(response.text, "响应内容")
            try:
                self.log.info("Response-json:  %s " % (response.json()))
                return response.json()
            except:
                self.log.info("Response-NonJson:  %s " % (response))
                return response
        except RequestException as e:
            self.log.exception("RequestException:  %s " % (e))
            raise e
        except Exception as e:
            self.log.exception("RequestException:  %s " % (e))
            raise e

    def elapsed_time(self, func: Response, fixed: str = 'ms'):
        """
        用时函数
        :param func: response实例
        :param fixed: 1或1000 秒或毫秒
        :return:
        """
        try:
            if fixed.lower() == 's':
                second = func.elapsed.total_seconds()
            elif fixed.lower() == 'ms':
                second = func.elapsed.total_seconds() * 1000
            else:
                raise ValueError("{} not in ['s'，'ms']".format(fixed))
            return second
        except RequestException as e:
            raise
        except Exception as e:
            raise e

