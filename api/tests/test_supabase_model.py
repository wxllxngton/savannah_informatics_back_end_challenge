import unittest
from models.supabase_model import SupabaseModel

class TestSupabaseModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by initializing SupabaseModel and
        inserting a new customer record to use across all test methods.
        """
        self.supabase_model = SupabaseModel()
        # Create new customer payload for testing purposes
        self.new_customer_payload = {
            "customerfname": "Example",
            "customerlname": "Name",
            "customerphoneno": 254744449999
        }
        # Insert a new customer record and store the response for further tests
        self.new_customer_response = self.supabase_model.insert_record('customers', self.new_customer_payload)

    def test_query_records(self):
        """
        Test querying records from the 'customers' table using a filter
        based on the newly created customer ID.
        """
        filters = {
            "customerid": ("eq", self.new_customer_response[0]['customerid']),
        }
        response = self.supabase_model.query_records('customers', filters)
        self.assertEqual(response[0]['customerid'], self.new_customer_response[0]['customerid'])

    def test_insert_record(self):
        """
        Test inserting a new customer record into the 'customers' table.
        Verify that the inserted first name matches the provided payload.
        """
        payload = {
            "customerfname": "Example",
            "customerlname": "Name",
            "customerphoneno": 254744449999
        }
        response = self.supabase_model.insert_record('customers', payload)
        customer_first_name = response[0]['customerfname']
        self.assertEqual(customer_first_name, payload['customerfname'])

    def test_update_record(self):
        """
        Test updating the last name of the newly created customer and
        verify that the update is successful.
        """
        update_record_payload = {
            "customerlname": 'Updatedname'
        }
        update_record_filters = {
            "customerid": ("eq", self.new_customer_response[0]["customerid"]),
        }
        update_record_response = self.supabase_model.update_record('customers', update_record_payload, update_record_filters)
        self.assertEqual(update_record_response[0]['customerlname'], update_record_payload['customerlname'])

    def test_upsert_record(self):
        """
        Test upserting (inserting or updating) the last name of the customer
        and verify the upsert operation was successful.
        """
        upsert_record_payload = {
            "customerlname": 'Upsertedname'
        }
        upsert_record_filters = {
            "customerid": ("eq", self.new_customer_response[0]["customerid"]),
        }
        upsert_record_response = self.supabase_model.upsert_record('customers', upsert_record_payload, upsert_record_filters)
        self.assertEqual(upsert_record_response[0]['customerlname'], upsert_record_payload['customerlname'])

    def test_delete_record(self):
        """
        Test deleting the newly created customer record and verify
        that the customer ID matches the expected value.
        """
        filters = {
            "customerid": ("eq", self.new_customer_response[0]["customerid"]),
        }
        delete_record_response = self.supabase_model.delete_record('customers', filters)
        self.assertEqual(delete_record_response[0]['customerid'], self.new_customer_response[0]['customerid'])


if __name__ == "__main__":
    unittest.main()
