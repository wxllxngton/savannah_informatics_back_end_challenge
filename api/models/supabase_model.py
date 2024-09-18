import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabaseModel:
    """
    A class to interact with the Supabase client, loading credentials
    from an environment file (.env) in the root directory.
    Provides methods for inserting, updating, querying, and deleting records.
    """

    def __init__(self):
        """
        Initializes the SupabaseModel by loading environment variables
        from an .env file and creating a Supabase client.
        """
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
        url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL or key missing in the environment variables.")
        self.supabase: Client = create_client(url, key)

    def parse_response(self, response):
        """
        Parses the Supabase response into JSON.

        Parameters:
            response (APIResponse): The raw response from Supabase.

        Returns:
            dict: The parsed JSON response.
        """
        try:
            parsed_response = json.loads(response.json())
            return parsed_response["data"]
        except json.JSONDecodeError:
            raise ValueError("Error parsing the response JSON.")

    def insert_record(self, table_name: str, payload: dict):
        """
        Inserts a new record into the specified table.

        Parameters:
            table_name (str): The name of the table.
            payload (dict): The data to insert.

        Returns:
            dict: The response from Supabase.

        Raises:
            Exception: If there is an error during insertion.
        """
        try:
            response = self.supabase.table(table_name).insert(payload).execute()
            return self.parse_response(response)
        except Exception as e:
            raise Exception(f"Error inserting record into {table_name}: {e}")

    def update_record(self, table_name: str, payload: dict, filters=None):
        """
        Updates records in the specified table based on filters.

        Parameters:
            table_name (str): The name of the table.
            payload (dict): The data to update.
            filters (dict): The filters to apply to the update query.

        Returns:
            dict: The response from Supabase.

        Raises:
            Exception: If there is an error during the update.
        """
        try:
            query = self.supabase.table(table_name).update(payload)
            response = self._apply_filters(query, filters).execute()
            return self.parse_response(response)
        except Exception as e:
            raise Exception(f"Error updating record in {table_name}: {e}")

    def upsert_record(self, table_name: str, payload: dict, filters=None):
        """
        Upserts a record (insert or update) in the specified table based on filters.

        Parameters:
            table_name (str): The name of the table.
            payload (dict): The data to upsert.
            filters (dict): The filters to apply for upserting.

        Returns:
            dict: The response from Supabase.

        Raises:
            Exception: If there is an error during the upsert.
        """
        try:
            query = self.supabase.table(table_name).upsert(payload)
            response = self._apply_filters(query, filters).execute()
            return self.parse_response(response)
        except Exception as e:
            raise Exception(f"Error upserting record in {table_name}: {e}")

    def delete_record(self, table_name: str, filters=None):
        """
        Deletes records in the specified table based on filters.

        Parameters:
            table_name (str): The name of the table.
            filters (dict): The filters to apply to the delete query.

        Returns:
            dict: The response from Supabase.

        Raises:
            Exception: If there is an error during deletion.
        """
        try:
            query = self.supabase.table(table_name).delete()
            response = self._apply_filters(query, filters).execute()
            return self.parse_response(response)
        except Exception as e:
            raise Exception(f"Error deleting record from {table_name}: {e}")

    def query_records(self, table_name: str, filters=None):
        """
        Queries records from the specified table based on filters.

        Parameters:
            table_name (str): The name of the table.
            filters (dict): The filters to apply to the select query.

        Returns:
            dict: The queried data from Supabase.

        Raises:
            Exception: If there is an error during the query.
        """
        try:
            query = self.supabase.table(table_name).select("*")
            response = self._apply_filters(query, filters).execute()
            return self.parse_response(response)
        except Exception as e:
            raise Exception(f"Error querying records from {table_name}: {e}")

    def _apply_filters(self, query, filters: dict):
        """
        Applies the given filters to a Supabase query.

        Parameters:
            query (SupabaseQuery): The initial query object.
            filters (dict): The filters to apply, where the key is the column name and the value is a tuple (operator, value).

        Supported operators:
            'eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'like', 'ilike', 'in', 'contains'.

        Returns:
            SupabaseQuery: The query with filters applied.
        """
        if filters:
            for column, (operator, value) in filters.items():
                if hasattr(query, operator):
                    query = getattr(query, operator)(column, value)
                else:
                    raise ValueError(f"Unsupported operator '{operator}' in filter for column '{column}'")
        return query



