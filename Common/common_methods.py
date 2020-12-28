import _locale
import hashlib, time, yaml, json, sys, os, shutil
from datetime import datetime, timedelta


_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])


class CommonMethod:
    @staticmethod
    def hash_md5(string):
        """
        获取字符串的MD5值，即加密
        :param string:
        :return:
        """
        res = hashlib.md5(str(string).encode(encoding='UTF-8')).hexdigest()
        return res

    @staticmethod
    def timestamp():
        # 取16位微秒级时间戳
        t = str(int(time.time() * 1000000))
        return t

    @staticmethod
    def get_time(days=0, minutes=0, seconds=0, fmt='%Y-%m-%d %H:%M:%S'):
        """
        # 获取当前时间或前后的日期时间
        :param days: int   大于0时表示当前之后的第几天
        :param minutes: int   大于0时表示当前之后的第几分钟
        :param seconds: int   大于0时表示当前之后的第几秒
        :param fmt: str      时间格式，可自定义
        :return:  str  时间
        """
        t = (datetime.now() + timedelta(days=days) + timedelta(minutes=minutes) + timedelta(
            seconds=seconds)).strftime(fmt)
        return t

    @staticmethod
    def str_switch_to_time(t: str, fmt='%Y-%m-%d %H:%M:%S'):
        """
        将时间字符串转换为时间格式
        :param t: str
        :param fmt:  时间格式
        :return:
        """
        return datetime.strptime(t, fmt)

    @staticmethod
    def read_yaml(filepath):
        """
        写入yaml格式文件
        :param filepath: 文件路径+文件名
        :return:
        """
        with open(filepath, "r", encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def write_yaml(filepath, content: dict, mode='w'):
        """
        读取yaml格式文件
        :param filepath: 文件路径+文件名
        content: 写入内容, dict
        :return:
        """
        with open(filepath, mode=mode, encoding='utf-8') as nf:
            yaml.dump(content, nf, encoding='utf-8', allow_unicode=True)

    @staticmethod
    def read_json(filepath):
        """
        读取yaml格式文件
        :param filepath: 文件路径
        :return:
        """
        with open(filepath, "r", encoding='utf-8') as f:
            file_content = json.load(f)
        return file_content

    # @staticmethod
    # def read_file_by_key(file, key):
    #     """
    #     文件读取
    #     :param file:
    #     :param key:
    #     :return:
    #     """
    #     with open(file, 'r', encoding="utf-8") as f:
    #         for line in f:
    #             if key in line:
    #                 # print(line)
    #                 value = line.split('=')[1].strip()
    #     return value
    #
    # @staticmethod
    # def write_file(file, content):
    #     """
    #     # 文件写入
    #     :param file:
    #     :param content:
    #     :return:
    #     """
    #     with open(file, 'w', encoding="utf-8") as f:
    #         f.write(str(content))
    #
    # def update_file(self, file, key, value):
    #     """
    #     # 文件更新,替换文件中key=*为key=value
    #     :param file:
    #     :param key:
    #     :param value:
    #     :return:
    #     """
    #     with open(file, 'r', encoding="utf-8") as f:
    #         file_content = ''
    #         for line in f:
    #             if key in line:
    #                 line = key + ' = ' + str(value)
    #             file_content += line
    #     self.write_file(file, file_content)
    #
    # @staticmethod
    # def switch_file_to_object(filepath):
    #     """
    #     将文件转换为文件对象
    #     :param filepath: 文件路径
    #     :return:  file object
    #     """
    #     return open(filepath, 'rb+')

    @staticmethod
    def get_env():
        """
        获取输入的env命令行参数
        备注：
        :return:
        """
        command_params = sys.argv
        env = "test"
        for item in range(1, len(command_params)):
            if "env" in command_params[item]:
                env = command_params[item].split("=")[1]
        return env

    @staticmethod
    def mkdir_dir(file_dir):
        """
        创建多级目录
        :param file_dir:   多级文件目录
        """
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            return '{}路径已存在'.format(file_dir)

    @staticmethod
    def remove_dir(file_dir):
        """
        删除目标文件夹
        :param file_dir:   文件夹路径
        """
        shutil.rmtree(file_dir)

    def replace_dict_value(self, org_dict, replace_dict):
        """
        检查replace_dict中的key，如果与org_dict中的key值相同，则把org_dict中该key对应的value值替换成replace_dict中的value值
        :param org_dict: 原始字典
        :param replace_dict: 替换字典
        :return: 修改后的原始字典，key值不变，value值需从replace_dict中寻找匹配
        """
        # 如果是嵌套的字典，有可能其value是列表或者元组
        if isinstance(org_dict, (list, tuple)):
            list_temp = list()
            for i in org_dict:
                list_temp.append(self.replace_dict_value(i, replace_dict))
            return list_temp
        if isinstance(org_dict, str) and org_dict.startswith('{') and org_dict.endswith('}'):  # 此处不严谨
            org_dict = json.loads(org_dict.replace('null', '"null_re"').replace('false', '"false_re"').replace('true', '"true_re"').replace('"null"', '"null_re"').replace('"false"', '"false_re"').replace('"true"', '"true_re"').replace('\'', '\"'))
            org_dict = self.replace_dict_value(org_dict, replace_dict)
            org_dict = json.dumps(org_dict, ensure_ascii=False).replace('"null_re"', 'null').replace('"false_re"', 'false').replace('"true_re"', 'true')
            return org_dict
        if isinstance(org_dict, dict):
            for key, value in org_dict.items():
                org_dict[key] = self.replace_dict_value(value, replace_dict)
                if key in replace_dict:
                    org_dict[key] = replace_dict[key]
            return org_dict
        return org_dict

    def get_value_list_by_key(self, target_dict, target_key, resp=None):
        """
        嵌套字典中根据key查找值,返回list
        :param target_dict:
        :param target_key:
        :param resp:
        :return: list
        """
        if resp is None:
            resp = []
        if isinstance(target_dict, str) and target_dict.startswith('{') and target_dict.endswith('}'):
            if isinstance(json.loads(target_dict.replace('\'', '\"')), dict):
                target_dict = json.loads(target_dict.replace('\'', '\"'))
        if isinstance(target_dict, (list, tuple)):
            for item in target_dict:
                resp = self.get_value_list_by_key(item, target_key, resp)
        if isinstance(target_dict, dict):
            for key, value in target_dict.items():
                if key == target_key:
                    resp.append(value)
                    resp = self.get_value_list_by_key(value, target_key, resp)
                else:
                    resp = self.get_value_list_by_key(value, target_key, resp)
        return resp

    def find_dict_by_key(self, target_dict, target_key, resp=None):
        """
        嵌套字典中根据key查找值,当没找到时返回None,仅一个数值时返回该值,多个数值返回原列表
        :param target_dict:
        :param target_key:
        :param resp:
        :return:
        """
        data_list = self.get_value_list_by_key(target_dict, target_key, resp)
        if len(data_list) == 0:
            return None
        elif len(data_list) == 1:
            return data_list[0]
        else:
            return data_list


func = CommonMethod()

if __name__ == '__main__':
    r = func.timestamp()








