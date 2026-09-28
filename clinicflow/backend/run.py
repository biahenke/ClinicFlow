#!/usr/bin/env python
import uvicorn
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
