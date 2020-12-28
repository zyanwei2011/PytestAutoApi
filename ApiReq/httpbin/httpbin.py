from Common.http_request import Request



class HttpBin:

    var_dict = {}

    @staticmethod
    def request_http_get(a=123, b=456):
        """
        get 请求
        :param a:
        :param b:
        :return:
        """
        httpbin_get_request = Request("httpbin", 'httpbin_get', a=a, b=b)
        httpbin_get_result = httpbin_get_request.send_request()
        return httpbin_get_result


if __name__ == '__main__':
    r = HttpBin().request_http_get()
    print(r)
