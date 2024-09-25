from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from models.supabase_model import SupabaseModel
from models.africastalking_model import AfricastalkingModel
from helpers.helpers import generate_africastalking_message
from django.http import HttpResponseRedirect
import jwt
from functools import wraps
from django.http import JsonResponse

# Initialize the SupabaseModel
supabase_model = SupabaseModel()

# Initialize the AfricastalkingModel
africastalking_model = AfricastalkingModel()


def get_token_auth_header(request):
    """
    Extract the Access Token from the Authorization Header.

    Parameters:
        request: The incoming HTTP request.

    Returns:
        token (str): The access token extracted from the Authorization header.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if not auth:
        raise ValueError("Authorization header is missing.")

    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Authorization header must be a Bearer token.")

    return parts[1]


def requires_scope(required_scope):
    """
    Verifies if the required scope is present in the access token.

    Parameters:
        required_scope (str): The required scope to access the resource.

    Returns:
        function: A decorated function with scope checking.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = get_token_auth_header(args[0])
                decoded = jwt.decode(token, verify=False)
                token_scopes = decoded.get("scope", "").split()

                if required_scope in token_scopes:
                    return f(*args, **kwargs)

                response = JsonResponse({'message': 'You don\'t have access to this resource'})
                response.status_code = 403
                return response
            except Exception as e:
                response = JsonResponse({'error': str(e)})
                response.status_code = 403
                return response
        return decorated
    return decorator


# Class-based view for handling index requests
class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        GET request to redirect users to the API Documentation.

        Returns:
            HttpResponseRedirect: Redirects users to the API documentation URL.
        """
        try:
            # URL to redirect to
            redirect_url = "https://documenter.getpostman.com/view/21896699/2sAXqv4LN1"

            # Redirect the user to the specified URL
            return HttpResponseRedirect(redirect_url)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Class-based view for handling customer requests
class CustomerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        GET request to retrieve customer data from Supabase.

        Returns:
            Response: JSON data of all customers.
        """
        try:
            data = supabase_model.query_records('customers')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        POST request to add a new customer.

        Parameters:
            request: The incoming HTTP request with customer data.

        Returns:
            Response: JSON response with the result of the customer creation.
        """
        try:
            customer_data = request.data
            response = supabase_model.insert_record('customers', customer_data)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """
        PATCH request to update a customer record.

        Parameters:
            request (Request): The request object containing the data to update.

        Returns:
            Response: A JSON response with the result of the update operation.
                      If 'customerid' is missing, an error message is returned.
        """
        try:
            new_customer_data = request.data

            if "customerid" not in new_customer_data:
                return Response({"error": "Missing customerid!"}, status=status.HTTP_400_BAD_REQUEST)

            filters = {'customerid': ('eq', new_customer_data.pop("customerid"))}
            response = supabase_model.update_record('customers', new_customer_data, filters)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CustomerView(APIView):
#     @requires_scope('read:customers')
#     def get(self, request):
#         """
#         GET request to retrieve customer data from Supabase.

#         Returns:
#             Response: JSON data of all customers.
#         """
#         try:
#             data = supabase_model.query_records('customers')
#             return Response(data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @requires_scope('write:customer')
#     def post(self, request):
#         """
#         POST request to add a new customer.

#         Parameters:
#             request: The incoming HTTP request with customer data.

#         Returns:
#             Response: JSON response with the result of the customer creation.
#         """
#         try:
#             customer_data = request.data
#             response = supabase_model.insert_record('customers', customer_data)
#             return Response(response, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @requires_scope('write:customer')
#     def patch(self, request):
#         """
#         PATCH request to update a customer record.

#         Parameters:
#             request (Request): The request object containing the data to update.

#         Returns:
#             Response: A JSON response with the result of the update operation.
#                       If 'customerid' is missing, an error message is returned.
#         """
#         try:
#             new_customer_data = request.data

#             if "customerid" not in new_customer_data:
#                 return Response({"error": "Missing customerid!"}, status=status.HTTP_400_BAD_REQUEST)

#             filters = {'customerid': ('eq', new_customer_data.pop("customerid"))}
#             response = supabase_model.update_record('customers', new_customer_data, filters)

#             return Response(response, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Class-based view for handling order requests
class OrderView(APIView):
    @requires_scope('read:orders')
    def get(self, request):
        """
        GET request to retrieve order data from Supabase.

        Returns:
            Response: JSON data of all orders.
        """
        try:
            data = supabase_model.query_records('orders')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @requires_scope('write:order')
    def post(self, request):
        """
        POST request to add a new order and notify the customer via SMS.

        Parameters:
            request: The incoming HTTP request with order data.

        Returns:
            Response: JSON response with the result of the order creation and SMS notification.
        """
        try:
            order_data = request.data
            response = supabase_model.insert_record('orders', order_data)

            customer_data = supabase_model.query_records('customers', {"customerid": ("eq", order_data["customerid"])})
            if not customer_data:
                return Response({"error": "Customer not found!"}, status=status.HTTP_400_BAD_REQUEST)

            at_data = {
                "message": generate_africastalking_message(response[0], customer_data[0]),
                "recipients": [f"+{customer_data[0]['customerphoneno']}"],
            }

            africastalking_model.send_sms(message=at_data["message"], recipients=at_data["recipients"])

            response[0]["message"] = at_data["message"]
            response[0]["recipients"] = at_data["recipients"]
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
