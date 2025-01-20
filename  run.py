if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)

# https://blog.logrocket.com/deploying-fastapi-applications-to-vercel/