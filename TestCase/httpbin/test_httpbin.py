from ApiReq.httpbin.httpbin import HttpBin
import pytest


@pytest.mark.parametrize('a, b', [(1, 2), (3, 4)])
def test_httpbin_get(a, b):
    httpbin_get_result = HttpBin().request_http_get(a, b)
    assert httpbin_get_result['headers']['Host'] == 'www.httpbin.org'
