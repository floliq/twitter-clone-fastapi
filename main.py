import uvicorn
from app.app import create_app

PORT = 8000
app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)
