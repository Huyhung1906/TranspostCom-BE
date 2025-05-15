from rest_framework.response import Response
from rest_framework import status

def success_response(message, data=None, code=status.HTTP_200_OK):
    return Response({
        "message": message,
        "status": code,
        "data": data or {}
    }, status=code)

def error_response(message, errors=None, code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "message": message,
        "status": code,
        "errors": errors or {}
    }, status=code)

def unauthorized_response(message="Unauthorized."):
    return error_response(message=message, code=status.HTTP_401_UNAUTHORIZED)

def not_found_response(message="Not found."):
    return error_response(message=message, code=status.HTTP_404_NOT_FOUND)

def server_error_response(message="Internal Server Error."):
    return error_response(message=message, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
