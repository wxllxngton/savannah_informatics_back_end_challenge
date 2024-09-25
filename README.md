# savannah_informatics_back_end_challenge

Savannah Informatics Screening Test

## API Service Documentation

## Overview

This Django-based API service hosted on Render(<a href="https://savannah-informatics-back-end-challenge.onrender.com">Link here</a>) provides endpoints for managing customers and orders. It integrates with Supabase for database operations and Africa's Talking for SMS notifications. The service uses Auth0 for authentication and authorization.

## Project Structure

-   `views.py`: Contains the API views for handling requests.
-   `models/`: Contains the models for interacting with Supabase and Africa's Talking.
-   `helpers/`: Contains helper functions for generating messages.
-   `settings.py`: Django settings configuration.
-   `urls.py`: URL routing configuration.
-   `.env`: Environment variables for configuration.
-   `utils.py`: Utility functions for authentication and token handling.
-   `wsgi.py`: WSGI configuration for deployment.
-   `manage.py`: Django's command-line utility for administrative tasks.
-   `requirements.txt`: List of dependencies for the project.

## Dependencies

The project uses the following dependencies, managed by Poetry:

-   `Django`: Web framework.
-   `djangorestframework`: Toolkit for building Web APIs.
-   `supabase`: Client for interacting with Supabase.
-   `africastalking`: Client for interacting with Africa's Talking.
-   `python-dotenv`: For loading environment variables.
-   `Authlib`: For handling authentication with Auth0.

## Environment Variables

The following environment variables are required:

-   `SERVICE_DOMAIN`: The domain of the service.
-   `SUPABASE_URL`: The URL for the Supabase instance.
-   `SUPABASE_KEY`: The API key for Supabase.
-   `AT_USERNAME`: Africa's Talking username.
-   `AT_KEY`: Africa's Talking API key.
-   `AUTH0_API_IDENTIFIER`: Auth0 API identifier.
-   `AUTH0_CLIENT_ID`: Auth0 client ID.
-   `AUTH0_CLIENT_SECRET`: Auth0 client secret.
-   `AUTH0_DOMAIN`: Auth0 domain.

## API Endpoints

-   `GET /`: Index endpoint.
-   `GET /api/`: API documentation endpoint.
-   `GET /api/customers/`: Endpoint for managing customers.
-   `GET /api/orders/`: Endpoint for managing orders.

## Running the Service

To run the service locally, use the following command:

```bash
$pip install poetry
$poetry shell
$poetry install
$(cd .api/ && poetry run python manage.py runserver)
```
