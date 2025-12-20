import uvicorn
from app.api import api_app

if __name__ == "__main__":
    uvicorn.run(api_app, host="0.0.0.0", port=8081)
