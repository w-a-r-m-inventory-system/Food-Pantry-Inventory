"""
GenerateSecretKey.py - program to generate a secret key.
"""

from secrets import token_urlsafe

if __name__ == '__main__':
    print(token_urlsafe(50))

# EOF
