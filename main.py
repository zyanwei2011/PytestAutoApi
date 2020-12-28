import os
from Config.file_path import report_data_path, report_dir


if __name__ == '__main__':
    os.system('pytest -s -m add --env=test --alluredir={} --clean-alluredir'.format(report_data_path))
    # 在线查看报告
    os.system("allure generate {} -o {} --clean".format(report_data_path, report_dir))



