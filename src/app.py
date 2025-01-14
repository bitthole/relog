from flask import Flask, request

import sys
import logging
import requests

# 1) Configure the logger to output to stdout
logger = logging.getLogger("uwsgi-request-logger")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def application(environ, start_response):
    """
    A simple WSGI application that logs the full request to stdout:
      - HTTP method
      - Path
      - Headers (extracted from environ keys starting with 'HTTP_')
      - Request body (read from wsgi.input)
    """
    # 2) Capture request details from WSGI environ
    
    request_method = environ.get("REQUEST_METHOD", "")
    path_info = environ.get("PATH_INFO", "")
    
    # Collect headers (HTTP_*) from environ
    headers = {}
    for key, value in environ.items():
        if key.startswith("HTTP_"):
            header_name = key[5:].replace("_", "-").title()
            headers[header_name] = value
    
    if "CONTENT_TYPE" in environ:
        headers["Content-Type"] = environ["CONTENT_TYPE"]
    if "CONTENT_LENGTH" in environ:
        headers["Content-Length"] = environ["CONTENT_LENGTH"]
    
    # Read request body
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0
    request_body = environ["wsgi.input"].read(request_body_size).decode("utf-8", errors="replace")
    
    # 3) Log the request details
    logger.info(
        "Request Method: %s | Path: %s | Headers: %s | Body: %s",
        request_method, path_info, headers, request_body
    )
    
    # 4) Send a basic response
    status = "200 OK"
    response_headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, response_headers)
    
    return [b"Hello from WSGI + stdout logging!\n"]

