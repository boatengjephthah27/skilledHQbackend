"""
This is a wrapper for a JSON http response specific to the kehillahglobal API.
It ensures that the data retrieved is in a json format and adds all possible 
errors to the caller of a particular route

"""
from django.http import JsonResponse

class ApiResponse(JsonResponse):
    def __init__(self, data=None, error=None, error_details=[], status=200):
        response = {"data": data, "error": error, "success": not error}
        if error_details and len(error_details) > 0:
            response["error_details"] = error_details

        super().__init__(
            response,
            safe=True,
            status=status,
        )
