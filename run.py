import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.api:app", reload=True)
    # uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)
