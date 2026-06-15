from typing import Optional, Dict, Any
from urllib.parse import parse_qs, urlsplit
from view_models import HTTPRequest, HTTPRequestMeta, HTTPMethod
from core import BigLogger

logger = BigLogger(__name__)


class HTTPParser:

    @staticmethod
    def _parse_headers(header_lines: list[str]) -> Dict[str, str]:
        headers: Dict[str, str] = {}

        for line in header_lines:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        return headers

    @staticmethod
    @logger.error_decorator()
    def parse_request(request: bytes) -> HTTPRequest:
        try:
            raw_request_str = request.decode('utf-8', errors='replace')
            head, _, body = raw_request_str.partition("\r\n\r\n")
            request_lines = [line for line in head.split("\r\n") if line]

            if not request_lines:
                raise ValueError("Empty HTTP request")

            request_line = request_lines[0]
            try:
                method_str, target, http_version = request_line.split(" ", 2)
                
            except ValueError as exc:
                raise ValueError(f"Malformed request line: {request_line}") from exc

            method = HTTPMethod(method_str)
            headers = HTTPParser._parse_headers(request_lines[1:])
            parsed_url = urlsplit(target)
            query_params = parse_qs(parsed_url.query, keep_blank_values=True)

            content_length_raw = headers.get("content-length")
            content_length = int(content_length_raw) if content_length_raw and content_length_raw.isdigit() else None

            meta = HTTPRequestMeta(
                user_agent=headers.get("user-agent"),
                accept=headers.get("accept"),
                accept_language=headers.get("accept-language"),
                accept_encoding=headers.get("accept-encoding"),
                connection=headers.get("connection"),
                referer=headers.get("referer"),
                origin=headers.get("origin"),
                content_type=headers.get("content-type"),
                content_length=content_length,
                sec_ch_ua=headers.get("sec-ch-ua"),
                sec_ch_ua_platform=headers.get("sec-ch-ua-platform"),
                sec_ch_ua_mobile=headers.get("sec-ch-ua-mobile"),
                sec_fetch_site=headers.get("sec-fetch-site"),
                sec_fetch_mode=headers.get("sec-fetch-mode"),
                sec_fetch_dest=headers.get("sec-fetch-dest"),
                raw_request_line=request_line,
                raw_headers=headers,
            )

            return HTTPRequest(
                method=method,
                path=parsed_url.path or "/",
                http_version=http_version,
                host=headers.get("host"),
                headers=headers,
                query_params=query_params,
                body=body,
                raw=raw_request_str,
                meta=meta,
            )

        except Exception as e:
            raise ValueError(f"Failed to parse HTTP request: {str(e)}")
