class RequestData:
    def __init__(self, data=None, params=None, headers=None, cookies=None):
        self.data = data
        self.params = params
        self.headers = headers
        self.cookies = cookies
