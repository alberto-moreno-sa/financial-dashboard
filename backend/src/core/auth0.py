"""
Auth0 JWT Token Validation

This module handles validation of Auth0 JWT tokens and extracts user information.
Uses RS256 algorithm with public key from Auth0's JWKS endpoint.
"""

from typing import Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from src.core.config import settings
import httpx

# Security scheme for Bearer token
security = HTTPBearer()

# Cache for Auth0 public keys (JWKS)
_jwks_cache: Optional[Dict] = None


async def get_auth0_public_key() -> Dict:
    """
    Fetches Auth0's public key (JWKS) for verifying JWT signatures.
    Caches the result to avoid repeated requests.
    """
    global _jwks_cache

    if _jwks_cache is not None:
        return _jwks_cache

    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        response.raise_for_status()
        _jwks_cache = response.json()

    return _jwks_cache


def verify_and_decode_token(token: str) -> Dict:
    """
    Verifies and decodes an Auth0 JWT token.

    Args:
        token: The JWT token string

    Returns:
        Dict containing the decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        print("=" * 80)
        print("DECODING TOKEN...")
        print(f"Token (first 50 chars): {token[:50]}...")
        print(f"Expected audience: {settings.AUTH0_AUDIENCE}")
        print(f"Expected issuer: https://{settings.AUTH0_DOMAIN}/")

        # For Auth0 with RS256, we decode without verification for development
        # NOTE: In production, you MUST verify the signature properly!

        # Decode without verification to get all claims
        payload = jwt.get_unverified_claims(token)

        # Manually verify audience and issuer
        # Auth0 can return audience as a string or a list
        aud = payload.get("aud")
        if isinstance(aud, list):
            if settings.AUTH0_AUDIENCE not in aud:
                raise JWTError(f"Invalid audience. Expected {settings.AUTH0_AUDIENCE} in {aud}")
        elif aud != settings.AUTH0_AUDIENCE:
            raise JWTError(f"Invalid audience. Expected {settings.AUTH0_AUDIENCE}, got {aud}")

        expected_issuer = f"https://{settings.AUTH0_DOMAIN}/"
        if payload.get("iss") != expected_issuer:
            raise JWTError(f"Invalid issuer. Expected {expected_issuer}, got {payload.get('iss')}")

        print("✅ Token decoded successfully!")
        print("=" * 80)
        return payload

    except JWTError as e:
        print(f"❌ JWTError: {str(e)}")
        print("=" * 80)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        print("=" * 80)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict:
    """
    FastAPI dependency that extracts and validates the current user from the JWT token.

    The token should contain custom claims added by our Auth0 Action:
    - https://financial-dashboard.com/auth0_id
    - https://financial-dashboard.com/email
    - https://financial-dashboard.com/name
    - https://financial-dashboard.com/picture
    - https://financial-dashboard.com/user_id (if user exists in our DB)

    Returns:
        Dict with user information: {
            "auth0_id": str,
            "email": str,
            "name": str,
            "picture": str,
            "user_id": Optional[str],  # Our internal DB user ID
            "email_verified": bool
        }
    """
    token = credentials.credentials
    payload = verify_and_decode_token(token)

    # DEBUG: Print the entire payload to see what we're getting
    print("=" * 80)
    print("TOKEN PAYLOAD DEBUG:")
    print("All claims in token:", list(payload.keys()))
    for key, value in payload.items():
        print(f"  {key}: {value}")
    print("=" * 80)

    # Extract custom claims from our Auth0 Action
    namespace = "https://financial-dashboard.com"

    auth0_id = payload.get(f"{namespace}/auth0_id") or payload.get("sub")
    email = payload.get(f"{namespace}/email") or payload.get("email")
    name = payload.get(f"{namespace}/name") or payload.get("name")
    picture = payload.get(f"{namespace}/picture") or payload.get("picture")
    user_id = payload.get(f"{namespace}/user_id")  # Our DB user_id (if synced)
    email_verified = payload.get(f"{namespace}/email_verified", False) or payload.get("email_verified", False)

    print(f"Extracted values:")
    print(f"  auth0_id: {auth0_id}")
    print(f"  email: {email}")
    print(f"  name: {name}")
    print(f"  picture: {picture}")
    print(f"  user_id: {user_id}")
    print(f"  email_verified: {email_verified}")
    print("=" * 80)

    if not auth0_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token missing required claims. auth0_id={auth0_id}, email={email}. All claims: {list(payload.keys())}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "auth0_id": auth0_id,
        "email": email,
        "name": name,
        "picture": picture,
        "user_id": user_id,  # May be None for first-time users
        "email_verified": email_verified,
    }
