"""
GenerateSecretKey.py - program to generate a secret key.
"""

from secrets import token_urlsafe

print(token_urlsafe(50))

# EOF
