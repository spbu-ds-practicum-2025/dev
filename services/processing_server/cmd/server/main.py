import uvicorn
from app.api import api_app
from os import getenv

if __name__ == "__main__":
    port = int(getenv("PORT", 8101))
    uvicorn.run(api_app, host="0.0.0.0", port=port)
