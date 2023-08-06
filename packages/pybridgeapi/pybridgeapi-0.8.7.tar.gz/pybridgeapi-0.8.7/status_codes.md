STATUS CODES

All responses use standard HTTP status codes.

Usually, codes in the 2xx range indicate success, codes in the 4xx range are for client-related failures, and 5xx codes are for Bankin-related issues (these are rare).

    200 OK Successful request.
    201 Created New resource created.
    202 Accepted The request has been accepted for processing, but the processing has not been completed.
    204 No Content Resource deleted.
    400 Bad Request The request is malformed. Check the parameters or the syntax.
    401 Unauthorized Couldn’t authenticate the request.
    403 Forbidden The request is not allowed.
    404 Not Found No such resource.
    409 Conflict The resource already exists.
    415 Unsupported media type The resource requires Content-Type: application/json header and a JSON body.
    422 Unprocessable entity The provided JSON is not valid.
    429 Too Many Requests Too many requests hit the API too quickly. See Rate limiting.
    500 Internal Server Error Something went wrong on our end (these are rare).

