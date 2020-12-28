import os
from TestData.common_data import env

# 获取当前项目路径
project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 请求配置文件路径
header_conf_path = os.path.join(project_path, 'Config', 'header_conf.yaml')
env_conf_path = os.path.join(project_path, 'Config', '{}_conf.yaml'.format(env))

# 测试输出报告目录
report_data_path = os.path.join(project_path, 'Outputs', 'report_data')
report_dir = os.path.join(project_path, 'Outputs', 'reports')
# 日志文件路径
log_dir = os.path.join(project_path, 'Outputs', 'logs')

# 测试数据
data_dir = os.path.join(project_path, 'TestData')

if __name__ == '__main__':
    print(env_conf_path)
    print(log_dir)


