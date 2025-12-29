"""
Demo Authentication Bypass for Vercel Deployment
Allows viewing demo data without Auth0 configuration
"""
from fastapi import HTTPException, status, Depends
from typing import Optional


async def get_demo_user():
    """
    Return demo user for public deployment
    Used when AUTH0_DOMAIN is not configured or set to 'demo'
    """
    return {
        "auth0_id": "demo|123456789",
        "email": "demo@financial-dashboard.com",
        "name": "Demo User",
        "email_verified": True,
        "sub": "demo|123456789"
    }


def is_demo_mode(auth0_domain: Optional[str] = None) -> bool:
    """Check if running in demo mode"""
    return auth0_domain is None or auth0_domain == "demo" or auth0_domain == "demo-financial.auth0.com"
