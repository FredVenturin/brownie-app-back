class HttpRequest:
    def __init__(self, body: dict = None, headers: dict = None, path_params: dict = None, query_params: dict = None) -> None:
        self.body = body
        self.headers = headers
        self.path_params = path_params
        self.query_params = query_params or {}