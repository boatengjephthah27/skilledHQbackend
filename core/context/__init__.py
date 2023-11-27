# from core.utils.common import parse_bool
from querystring_parser import parser
import json


class Context:
    """
    This contains info about a particular user and their request.
    About the user:
    * Are they logged in?

    About the request:
    * args: the body/payload that was sent in the request
    * dev? : also tells you if this request is coming from one of our dev sites

    """

    def __init__(self):
        self.args = {}
        self.user_is_logged_in = False
        self.user_id = None
        self.user_email = None
        self.is_super_admin = False
        self.is_partner = False
        self.company_id = None
        self.route = None

    def set_user_credentials(self, decoded_token):
        self.user_is_logged_in = True
        self.user_email = decoded_token.get("email", None)
        self.user_id = decoded_token.get("user_id", None)
        self.is_partner = decoded_token.get("is_partner", False)
        self.company_id = decoded_token.get("company_id", None)
        self.is_super_admin = decoded_token.get("is_super_admin", False)

    def set_request_body(self, request):
        # get the request args
        self.args = self._get_request_contents(request)
        self.route = request.path

    def get_request_body(self):
        return self.args

    def user_is_admin(self):
        return self.is_partner or self.is_super_admin

    def __str__(self):
        return str(
            {
                "args": self.args,
                "user_is_logged_in": self.user_is_logged_in,
                "user_id": self.user_id,
                "user_email": self.user_email,
                "company_id": self.company_id,
                "is_partner": self.is_partner,
                "is_super_admin": self.is_super_admin
            }
        )

    def _get_request_contents(self, request):
        try:
            if request.method != "POST":
                return request.GET.dict()

            args = {}
            if request.content_type == "application/x-www-form-urlencoded":
                args = parser.parse(request.POST.urlencode())
            elif request.content_type == "application/json":
                args = json.loads(request.body)
            elif request.content_type == "multipart/form-data":
                args = request.POST.dict()
                if request.FILES:
                    for i in request.FILES.dict():
                        args[i] = request.FILES[i]
            else:
                args = request.POST.dict()

            return args

        except Exception as e:
            return {}
