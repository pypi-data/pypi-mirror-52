from typing import Dict, Optional


class Request:
    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            path: Optional[str] = None,
            params: Optional[Dict[str, object]] = None,
            headers: Optional[Dict[str, str]] = None,
            content: Optional[str] = None
    ) -> None:
        super().__init__()
        self.host: Optional[str] = host
        self.port: Optional[int] = port
        self.path: Optional[str] = path
        self.params: Optional[Dict[str, object]] = params
        self.headers: Optional[Dict[str, str]] = headers
        self.content: Optional[str] = content

    def empty(self) -> bool:
        if self.host or self.content or self.params or self.headers or self.port or self.path:
            return False
        else:
            return True


class Response:
    def __init__(
            self,
            headers: Optional[Dict[str, str]] = None,
            content: Optional[str] = None,
            code: Optional[int] = None
    ) -> None:
        super().__init__()
        self.headers: Optional[Dict[str, str]] = headers
        self.content: Optional[str] = content
        self.code: Optional[int] = code

    def empty(self) -> bool:
        if self.code or self.headers or self.content:
            return False
        else:
            return True
