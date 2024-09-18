import unittest
from helpers.helpers import generate_africastalking_message

# Unit test case
class TestHelpers(unittest.TestCase):
    def test_generate_africastalking_message(self):
        """
        Test case for generating an AfricasTalking message.
        """
        # Sample customer and order data
        customer_data = {'customerfname': 'Jane', 'customerlname': 'Doe', 'customerphoneno': 254777777777}
        order_data = {'orderid': 27, 'customerid': 1, 'orderitem': 'Boards', 'orderamount': 10, 'orderstatus': 'Incomplete', 'ordertime': '2024-09-18T07:26:11.445054'}

        # Expected message
        expected_message = (
            f"Hello {customer_data['customerfname']} {customer_data['customerlname']}.\n"
            f"Your order (OrderID: {order_data['orderid']}) of {order_data['orderamount']}, "
            f"{order_data['orderitem']} is being processed."
        )

        # Assert that the generated message matches the expected message
        self.assertEqual(generate_africastalking_message(order_data, customer_data), expected_message)

    def test_generate_africastalking_message_missing_key(self):
        """
        Test case to check for missing keys in input data.
        """
        customer_data = {'customerfname': 'Jane', 'customerlname': 'Doe'}
        incomplete_order_data = {'orderid': 27, 'orderitem': 'Boards'}  # 'orderamount' is missing

        with self.assertRaises(KeyError) as context:
            generate_africastalking_message(incomplete_order_data, customer_data)

        self.assertIn('Missing key in order_data', str(context.exception))

if __name__ == '__main__':
    unittest.main()
