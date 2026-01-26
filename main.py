import uvicorn
from app.app import create_app

PORT = 8000

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, port=PORT)
