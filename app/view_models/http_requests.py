from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class HTTPRequestMeta(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    remote_addr: str | None = None
    remote_port: int | None = None
    user_agent: str | None = None
    accept: str | None = None
    accept_language: str | None = None
    accept_encoding: str | None = None
    connection: str | None = None
    referer: str | None = None
    origin: str | None = None
    content_type: str | None = None
    content_length: int | None = None
    sec_ch_ua: str | None = None
    sec_ch_ua_platform: str | None = None
    sec_ch_ua_mobile: str | None = None
    sec_fetch_site: str | None = None
    sec_fetch_mode: str | None = None
    sec_fetch_dest: str | None = None
    raw_request_line: str = ""
    raw_headers: dict[str, str] = Field(default_factory=dict)


class HTTPRequest(BaseModel):
    method: HTTPMethod
    path: str
    http_version: str
    host: str | None = None
    headers: Dict[str, str] = Field(default_factory=dict)
    query_params: Dict[str, List[str]] = Field(default_factory=dict)
    body: str = ""
    raw: str = ""
    meta: HTTPRequestMeta = Field(default_factory=HTTPRequestMeta)
  