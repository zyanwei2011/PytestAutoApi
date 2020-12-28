1.pytest.ini文件：解决测试用例打标后运行警告问题（@pytest.mark.smoke  PytestUnknownMarkWarning）,当存在警告时，可在该文件进行配置

2. 运行参数配置
addopts =
    -v  -s                                                 # 输出运行及调试信息,-q参数可简化控制台运行
    -m edit                                                # 过滤运行的用例，不过滤时注释即可以
    --env=test                                             # 设置运行环境
    -n=1                                                   # 设置多核运行
    --alluredir=./Outputs/report_data                      # allure生成的数据文件路径
    --reruns=1                                             # 失败重运行次数
    --html=./Outputs/reports.html --self-contained-html    # 普通格式报告路径