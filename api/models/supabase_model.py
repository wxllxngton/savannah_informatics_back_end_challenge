import os
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabaseModel:
    """
    A class to interact with the Supabase client, loading credentials
    from an environment file (.env) in the root directory.
    """

    def __init__(self):
        """
        Initializes the SupabaseModel by loading environment variables
        and creating a Supabase client.
        """
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
        url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL or key missing in the environment variables.")
        self.supabase: Client = create_client(url, key)

    def insert_record(self, table_name, payload):
        """
        Inserts a new record into a table.
        """
        try:
            response = self.supabase.table(table_name).insert(payload).execute()
            return response
        except Exception as e:
            print(f"Error inserting record: {e}")
            raise


    def update_record(self, table_name, payload, filters=None):
        """
        Updates records in a table based on filters.
        """
        return self._apply_filters(self.supabase.table(table_name).update(payload), filters).execute()

    def upsert_record(self, table_name, payload, filters=None):
        """
        Upserts a record in a table based on filters.
        """
        return self._apply_filters(self.supabase.table(table_name).upsert(payload), filters).execute()

    def delete_record(self, table_name, filters=None):
        """
        Deletes records in a table based on filters.
        """
        return self._apply_filters(self.supabase.table(table_name).delete(), filters).execute()

    def query_records(self, table_name, filters=None):
        """
        Queries records from a table based on filters.
        """
        return self._apply_filters(self.supabase.table(table_name).select("*"), filters).execute()

    def _apply_filters(self, query, filters):
        """
        Applies the given filters to a Supabase query.
        Supported operators: eq, neq, gt, gte, lt, lte, like, ilike, in, contains.
        """
        if filters:
            for column, (operator, value) in filters.items():
                query = getattr(query, operator)(column, value)
        return query


