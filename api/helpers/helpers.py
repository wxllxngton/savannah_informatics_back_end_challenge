def generate_africastalking_message(order_data: dict, customer_data: dict) -> str:
    """
    Generates a message for the customer based on their order details.

    Parameters:
        order_data (dict): A dictionary containing order details. Expected keys:
            - orderid (int): The ID of the order.
            - orderamount (float): The amount of the order.
            - orderitem (str): The name of the item ordered.
        customer_data (dict): A dictionary containing customer details. Expected keys:
            - customerfname (str): The first name of the customer.
            - customerlname (str): The last name of the customer.

    Returns:
        str: A formatted message for the customer.

    Raises:
        KeyError: If any required keys are missing from the input dictionaries.
    """
    try:
        print("Customer data in helpers: ")
        print(customer_data)
        print("Order data in helpers: ")
        print(order_data)
        message = (
            f"Hello {customer_data['customerfname']} {customer_data['customerlname']}.\n"
            f"Your order (OrderID: {order_data['orderid']}) of {order_data['orderamount']}, "
            f"{order_data['orderitem']} is being processed."
        )
        return message
    except KeyError as e:
        raise KeyError(f"Missing key in input data: {e}")

