# FastAPI Application

This is a FastAPI application with SMS functionality using Africa's Talking API.

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:Clemo97/customer-fast-api.git
   cd customer-fast-api
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

3. Open your web browser and navigate to `https://customer-fast-api.onrender.com/login` to access the API.

## Getting an Access Token

1. Visit `https://customer-fast-api.onrender.com/login` to get authenticated in order to receive your `access token`.

![Access Token](https://raw.githubusercontent.com/Clemo97/customer-fast-api/refs/heads/main/images/accessToken.png)

2. Use acess token in postman to interact with /api/customers and /api/orders endpoints

    ```
    curl --location 'https://customer-fast-api.onrender.com/api/customers/2' \
    --header 'Authorization: Bearer <Access Token>' \
    --header 'Content-Type: application/json'
    ```

    curl command to make orders

    ```
    curl --location 'https://customer-fast-api.onrender.com/api/orders?customer_id=1' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <Access Token>' \
    --data '{
    "item": "Pork Sausages",
    "amount": 609.00}'
    ```

3. SMS is sent using africas talking API when an order is made.

![SMS](/home/clement/Documents/FOSS/chat-fast-api/images/sms.png)

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: `https://customer-fast-api.onrender.com/docs`
- ReDoc: `https://customer-fast-api.onrender.com/redoc`

![SMS](/home/clement/Documents/FOSS/chat-fast-api/images/sms.png)

## Testing

To run the tests, use the following command:

```
pytest
```

![Tests](/home/clement/Documents/FOSS/chat-fast-api/images/tests.png)


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
