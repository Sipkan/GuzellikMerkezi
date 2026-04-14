import uvicorn

if __name__ == "__main__":
    print("Running Merkez Beauty Center web application...")
    uvicorn.run("app.main:app", host="localhost", port=8001, reload=False)
