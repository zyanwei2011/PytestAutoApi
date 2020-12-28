from Common.common_methods import func
from Common.logger import log
from Config.file_path import *
from pathlib import Path


class GetData:
    """
    获取测试数据
    """

    def __init__(self, module, api_name):
        """
        :param module: yaml file name
        :param api_name: api name in yaml file
        :return: request data
        """
        self.module = module
        self.api_name = api_name
        self.data_file_path = list(Path(data_dir).rglob('{}.yaml'.format(module)))[0]
        self.header_data = func.read_yaml(header_conf_path)
        self.env_data = GetEnvData()

    def get_api_data(self):
        file_content = func.read_yaml(self.data_file_path)
        return file_content[self.api_name]

    @property
    def api_title(self):
        return self.get_api_data().get('apiTitle')

    @property
    def api_data(self):
        api_data = self.get_api_data().get('requestData')
        return api_data

    @property
    def request_header(self):
        header_key = self.api_data.get('header')
        return self.header_data.get(header_key)

    @property
    def request_method(self):
        return self.api_data.get('method')

    @property
    def request_cookies(self):
        return self.api_data.get('cookies')

    @property
    def request_host(self):
        host = self.api_data.get('host')
        try:
            host = self.env_data.get_host.get(host)
        except:
            log.error('请检查配置文件和数据文件host配置是否正确且一致')
        return host

    @property
    def request_url(self):
        return self.request_host + self.api_data.get('route')

    @property
    def request_data(self):
        data_dict = {}
        api_data = self.api_data
        data = api_data.get('data')
        json = api_data.get('json')
        params = api_data.get('params')
        if data:
            data_dict['data'] = data
        if 'files' in api_data.keys():
            data_dict['files'] = api_data.get('files')
        if json:
            data_dict['json'] = json
        if params:
            data_dict['params'] = params
        return data_dict

    @property
    def validate_data(self):
        return self.get_api_data().get('validate')


class GetEnvData:
    """
    获取环境配置文件数据
    """

    def __init__(self):
        self.env_data = func.read_yaml(env_conf_path)

    @property
    def get_env_data(self):
        return self.env_data

    @property
    def get_host(self):
        return self.env_data.get('host')

    @property
    def get_config_account(self):
        return self.env_data.get('account')

    @property
    def get_env_header(self):
        return self.env_data.get('header')


if __name__ == '__main__':
    res = GetData("app_login", 'app_send_sms_code').request_header
    print(res)





