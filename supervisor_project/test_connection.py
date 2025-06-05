import requests

def test_connection():
    try:
        # Test basic server response first
        base_response = requests.get('http://127.0.0.1:5000/')
        print(f"Server base status: {base_response.status_code}")
        
        # Test machine endpoint with API key
        headers = {'X-API-KEY': 'secure-key-123'}  # Must match your API_KEYS in supervisor.py
        response = requests.get('http://127.0.0.1:5000/api/machines/M1', headers=headers)
        
        print(f"API Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Critical error: {str(e)}")

if __name__ == '__main__':
    test_connection()