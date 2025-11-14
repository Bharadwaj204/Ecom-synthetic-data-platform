#!/usr/bin/env python3
"""
Test suite for API functionality.
"""

import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

# Conditional imports to handle missing dependencies
try:
    import pytest
    from fastapi.testclient import TestClient
    from api.main import app
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    # Create mock objects for when dependencies are not available
    pytest = None
    TestClient = None
    app = None
    DEPENDENCIES_AVAILABLE = False

def test_api_root():
    """Test that API root endpoint works"""
    if not DEPENDENCIES_AVAILABLE:
        if pytest is not None:
            pytest.skip("Dependencies not available")
        else:
            return  # Skip the test manually
    
    if app is None or TestClient is None:
        if pytest is not None:
            pytest.skip("API dependencies not available")
        else:
            return  # Skip the test manually
    
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_api_health():
    """Test that API health check endpoint works"""
    if not DEPENDENCIES_AVAILABLE:
        if pytest is not None:
            pytest.skip("Dependencies not available")
        else:
            return  # Skip the test manually
    
    if app is None or TestClient is None:
        if pytest is not None:
            pytest.skip("API dependencies not available")
        else:
            return  # Skip the test manually
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    if DEPENDENCIES_AVAILABLE and pytest is not None:
        pytest.main([__file__])
    else:
        print("Skipping tests due to missing dependencies")