"""
Definition of the different Kehillah Error Types
"""
from core.utils.api_responses import ApiResponse


class ApiError(ApiResponse):
    def __init__(self, msg="unknown_error", error_details=[], status=400):
        self.msg = msg
        self.status = status
        self.error_details = error_details
        super().__init__(error=msg, error_details=error_details, status=200)

    def __str__(self):
        return self.msg


class NotAuthorizedError(ApiError):
    def __init__(self):
        super().__init__("permission_denied", status=403)


class InvalidResourceError(ApiError):
    def __init__(self):
        super().__init__("invalid_resource", status=404)


class ServerError(ApiError):
    def __init__(self):
        super().__init__("server_error", status=500)

class ValidationError(ApiError):
    def __init__(self, err_msg, error_details=[]):
        super().__init__(str(err_msg), error_details=error_details, status=200)
