from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
import requests
class RequestSpecs:
    Base_URL = 'http://localhost:4111/api'
    @staticmethod
    def base_header():
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def auth_headers(username:str, password:str):
        requests=LoginUserRequest
        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=requests.model_dump(),
            headers=RequestSpecs.base_header()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_header()
            headers['Authorization'] = f'Bearer {token}'
            return {
                'headers':headers,
                'base_url': RequestSpecs.Base_URL
            }
        raise Exception('Failed to login')

