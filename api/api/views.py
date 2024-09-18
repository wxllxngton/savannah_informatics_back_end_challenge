from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.supabase_model import SupabaseModel
from models.africastalking_model import AfricastalkingModel
from helpers.helpers import generate_africastalking_message, flatten_query_dict

# Initialize the SupabaseModel
supabase_model = SupabaseModel()

# Initialize the AfricastalkingModel
africastalking_model = AfricastalkingModel()

# Class-based view for handling customer requests
class CustomerView(APIView):

    def get(self, request):
        """
        GET request to retrieve customer data from Supabase.
        """
        try:
            # Fetch all customer data from the 'customers' table
            data = supabase_model.query_records('customers')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        POST request to add a new customer.
        """
        try:
            # Insert customer data into the 'customers' table
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
                    If successful, the updated data is returned.
        """
        try:
            # Extract data from the request
            new_customer_data = request.data

            # Ensure that 'customerid' is present in the data
            if "customerid" not in new_customer_data:
                response = {"error": "Missing customerid!"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Apply filters using the 'customerid' for identifying the record to update
            filters = {'customerid': ('eq', new_customer_data.pop("customerid"))}

            # Call the SupabaseModel to update the record in the 'customers' table
            response = supabase_model.update_record('customers', new_customer_data, filters)

            # Return the update operation result
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            # Return an internal server error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Class-based view for handling order requests
class OrderView(APIView):

    def get(self, request):
        """
        GET request to retrieve order data from Supabase.
        """
        try:
            # Fetch all order data from the 'orders' table
            data = supabase_model.query_records('orders')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        POST request to add a new order.
        """
        try:
            # Insert order data into the 'orders' table
            order_data = request.data
            response = supabase_model.insert_record('orders', order_data)
            customer_data = supabase_model.query_records('customers', {"customerid": ("eq", order_data["customerid"])})

            if not customer_data:
                return Response({"error": "Customer not found!"}, status=status.HTTP_400_BAD_REQUEST)

            # Set AT data
            at_data = {
                "message": generate_africastalking_message(response[0], customer_data[0]),
                "recipients": [f"+{customer_data[0]['customerphoneno']}"],
            }

            # Send recipient confirmation sms
            africastalking_model.send_sms(message=at_data["message"], recipients=at_data["recipients"])

            # Load AT data into response
            response[0]["message"] = at_data["message"]
            response[0]["recipients"] = at_data["recipients"]
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


