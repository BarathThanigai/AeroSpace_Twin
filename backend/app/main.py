import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# import sys
# from pathlib import Path

# Add app to path
# sys.path.insert(0, str(Path(__file__).parent))

from app.data.stream import initialize_stream, get_stream
from app.ml.anomaly_detector import initialize_detector
from app.ml.threat_classifier import initialize_classifier
from app.ml.model_trainer import train_isolation_forest
from app.core.digital_twin import initialize_twin, get_twin
from app.core.incident_manager import initialize_manager
from app.core.recommendation_engine import initialize_engine
from app.api.endpoints import router
from app.utils.logger import get_logger
from app.config import CONFIG_DIR, MODEL_PATH, SCALER_PATH

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup and shutdown."""
    logger.info("Starting AeroShield Twin backend...")

    try:
        # Initialize all components
        logger.info("Initializing components...")

        # 1. Train or load anomaly detection model
        if not MODEL_PATH.exists():
            logger.info("Model not found. Training Isolation Forest...")
            MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            train_isolation_forest(
                num_samples=1500,
                model_path=str(MODEL_PATH),
                scaler_path=str(SCALER_PATH),
            )
        else:
            logger.info("Loading pre-trained model...")

        detector = initialize_detector(str(MODEL_PATH), str(SCALER_PATH))
        logger.info(f"✓ Anomaly detector initialized (trained={detector.is_trained})")

        # 2. Initialize threat classifier
        threat_rules_path = CONFIG_DIR / "threat_rules.json"
        classifier = initialize_classifier(str(threat_rules_path))
        logger.info("✓ Threat classifier initialized")

        # 3. Initialize recommendation engine
        mitigations_path = CONFIG_DIR / "mitigations.json"
        impact_rules_path = CONFIG_DIR / "impact_rules.json"
        engine = initialize_engine(str(mitigations_path), str(impact_rules_path))
        logger.info("✓ Recommendation engine initialized")

        # 4. Initialize digital twin
        twin = initialize_twin()
        logger.info("✓ Digital twin initialized")

        # 5. Initialize incident manager
        manager = initialize_manager()
        logger.info("✓ Incident manager initialized")

        # 6. Initialize data stream
        stream = initialize_stream(update_interval=1.5)
        logger.info("✓ Data stream initialized")

        # 7. Start streaming task
        async def run_stream():
            await stream.stream()

        # Register digital twin as listener
        async def update_twin(aircraft):
            twin.update_state(aircraft)

        stream.register_listener("digital_twin", update_twin)

        # Start stream in background
        stream_task = asyncio.create_task(run_stream())
        logger.info("✓ Stream started")

        logger.info("✓✓✓ AeroShield Twin backend initialized successfully!")

        yield

        # Shutdown
        logger.info("Shutting down AeroShield Twin backend...")
        stream.stop()
        if not stream_task.done():
            stream_task.cancel()
            try:
                await stream_task
            except asyncio.CancelledError:
                pass
        logger.info("✓ Shutdown complete")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


# Create FastAPI app
app = FastAPI(
    title="AeroShield Twin",
    description="AI-powered cybersecurity digital twin for aircraft systems",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to AeroShield Twin",
        "docs": "/docs",
        "version": "1.0.0",
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
