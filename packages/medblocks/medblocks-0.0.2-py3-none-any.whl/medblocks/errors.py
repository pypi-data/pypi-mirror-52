class LoginError(Exception):
    """Raises when user is not stored in Client"""
    pass

class MedBlocksAPIError(Exception):
    pass

class PermissionError(Exception):
    pass