import pytest
from TestData import common_data


def pytest_addoption(parser):
    """
    # 自定义测试环境参数
    :param parser:
    :return:
    """
    parser.addoption("--env", action="store", default="test",
                     help="env: test environment, such as production, prerelease, test. Detail refer to env.py")


@pytest.fixture(scope='session', autouse=True)
def get_env(request):
    """
    # 获取测试环境--test/product
    :return:
    """
    test_env = request.config.getoption("--env")
    setattr(common_data, 'env', test_env)
    return request.config.getoption("--env")





