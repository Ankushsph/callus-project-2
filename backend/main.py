"""FastAPI application for AI essay detection."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import AnalyzeRequest, AnalyzeResponse
from pipeline import DetectionPipeline

app = FastAPI(
    title="AI Essay Detector",
    description="Detects AI-generated content in admissions essays using measurable linguistic signals",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline (loads models once at startup)
pipeline = DetectionPipeline()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Essay Detector",
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_essay(request: AnalyzeRequest):
    """
    Analyze an essay for AI-generated content.
    
    Returns sentence-level scores with evidence for each flag.
    """
    try:
        result = pipeline.analyze(request.essay)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
def health_check():
    """Detailed health check with model status."""
    return {
        "status": "healthy",
        "models_loaded": pipeline.is_ready(),
        "analyzers": ["perplexity", "burstiness", "lexical", "pattern"]
    }
