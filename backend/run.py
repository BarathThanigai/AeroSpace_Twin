#!/usr/bin/env python
"""Entry point for running AeroShield Twin backend."""

import sys
from pathlib import Path
import uvicorn

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

if __name__ == "__main__":
    print("Starting AeroShield Twin Backend...")
    print("API Documentation: http://localhost:8000/docs")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
