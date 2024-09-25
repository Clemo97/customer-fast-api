# FastAPI Application

This is a FastAPI application with SMS functionality using Africa's Talking API.

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.

2. Add the following environment variables to the `.env` file:
   ```
   AUTH0_DOMAIN=your_auth0_domain
   API_AUDIENCE=your_api_audience
   AUTH0_CLIENT_ID=your_auth0_client_id
   AUTH0_CLIENT_SECRET=your_auth0_client_secret
   CALLBACK_URL=your_callback_url
   AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
   SQLALCHEMY_DATABASE_URL=your_database_url
   ```

   Replace the placeholder values with your actual credentials and configuration.

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the FastAPI application:
   ```
   uvicorn main:app --reload
   ```

3. Open your web browser and navigate to `http://localhost:8000` to access the API.

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

![API Documentation](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Testing

To run the tests, use the following command:

```
pytest
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
