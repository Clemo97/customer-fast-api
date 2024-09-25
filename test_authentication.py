import pytest
from authentication import verify_token, get_token_from_code
from jose import jwt
from unittest.mock import patch

# Mock JWT data for testing
def mock_decode_token(token, public_key, algorithms, audience, issuer):
    # Simulate a valid payload decoded from the token
    return {"sub": "auth0|12345", "aud": audience}

@patch('authentication.jwt.decode', side_effect=mock_decode_token)
def test_verify_token(mock_decode):
    # Example token (the actual value doesn't matter due to mocking)
    token = "valid.jwt.token"
    result = verify_token(token)
    
    assert result["sub"] == "auth0|12345"

@patch('authentication.requests.post')
def test_get_token_from_code(mock_post):
    # Mock the response from the Auth0 token endpoint
    mock_post.return_value.json.return_value = {
        "access_token": "access_token_value",
        "id_token": "id_token_value"
    }

    # Test with a mock authorization code
    result = get_token_from_code("mock_code")
    
    assert result["access_token"] == "access_token_value"
    assert result["id_token"] == "id_token_value"
