"""
Middle ware for authorization for users before they access specific resources
"""
from typing import Tuple
from core.utils.constants import COOKIE_NAME
from core.utils.api_errors import (
    ApiError,
    ApiResponse,
)
from core.context import Context
from backendskilledhq.settings import SECRET_KEY
import jwt


class JWTMiddleware:
    """ """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def _get_decoded_token(self, token) -> Tuple[dict, ApiError]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithm="HS256", options={
                                 "verify_exp": False})
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, ApiError("session_expired")
        except jwt.DecodeError:
            return None, ApiError("token_decode_error")
        except jwt.InvalidTokenError as e:
            return None, ApiError("invalid_token")
        except Exception as e:
            return None, ApiError("invalid_token")

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        try:
            ctx = Context()
            ctx.set_request_body(request)
            token = request.COOKIES.get(
                COOKIE_NAME, None) or request.POST.get(COOKIE_NAME, None)
            if token:
                decoded_token, err = self._get_decoded_token(token)
                if err:
                    err.delete_cookie(COOKIE_NAME)
                    return err

                ctx.set_user_credentials(decoded_token)

                MAX_AGE = 24 * 60 * 60  # one day
                response = ApiResponse(None)

                response.delete_cookie(COOKIE_NAME)
                response.set_cookie(COOKIE_NAME, value=token,
                                    max_age=MAX_AGE, samesite="Strict")
            request.context = ctx

        except Exception as e:
            return ApiError(e)
