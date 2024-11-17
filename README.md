# Pearl Hacks Web APIs 

## Tech Stack

- **Backend Framework**: FastAPI
- **Cloud Storage**: Firebase Storage
- **Deployment**: Fly.io
- **Environment Management**: Python `venv`, Docker

## File Structure

```
┣.github
┃ ┗ workflows       # GitHub Actions workflow configurations
┣ apis              # API endpoints and business logic
┣ models            # Data models and schemas
┣ routes            # Route handlers and endpoints
┣ .dockerignore     # Docker ignore file
┣ .gitignore        # Git ignore file
┣ Dockerfile        # Docker configuration
┣ init.py           # Python package initializer
┣ fly.toml          # Fly.io configuration
┣ main.py           # Application entry point
┗ requirements.txt  # Python dependencies
```

## Getting Started

### Docker Instructions

Build Docker and Run Docker Container

```bash
docker build -t myapp .
docker run -p 8000:8000 myapp
```

### Deployment to Fly.io

1. Install Fly.io CLI

```bash
curl -L https://fly.io/install.sh | sh
```

2. Authenticate with Fly.io

```bash
flyctl auth login
```

3. Create and Configure Fly.io App
   
```bash
flyctl launch
```

4. Deploy to Fly.io
```bash
flyctl deploy
```

5. Verify Application Logs

```bash
flyctl logs
```

### Run Unit Test

1. Create a main.py file with this code
   
```python
import requests

def test_api_endpoint():
    app_url = "https://google-sheets-api-pearl-hacks.fly.dev"
    route = "/sheet/faqs"
    endpoint = f"{app_url}{route}"
    
    try:
        response = requests.get(endpoint)
        # Check if request was successful
        response.raise_for_status()
        
        # Print status code
        print(f"Status Code: {response.status_code}")
        
        # Print headers
        print(f"Content-Type: {response.headers.get('content-type')}")
        
        # Print JSON response
        data = response.json()
        print("Response Data:", data)
        
        return data
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting to the server: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except ValueError as val_err:
        print(f"Error parsing JSON response: {val_err}")

if __name__ == "__main__":
    test_api_endpoint()
```

2. Create Python virtual environment

```bash
python -m venv venv
```
  
3. Activate Python virtual environment

For Mac/Linux:
```bash
source venv/bin/activate
```

For Windows:
```bash
.\venv\Scripts\activate
```
4. Run test file

```bash
python main.py
```
