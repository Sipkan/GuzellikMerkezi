"""Run the Merkez Beauty Center web application."""
import uvicorn

if __name__ == "__main__":
    print("Running Merkez Beauty Center web application...")
    # NOTE: reload=True can spawn the worker process using a different Python
    # interpreter on Windows, which may break template rendering in some setups.
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=False)
