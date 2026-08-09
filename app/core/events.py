from enum import Enum



class SecurityEvent(str, Enum):


    SCAN_UPLOAD_STARTED = (
        "SCAN_UPLOAD_STARTED"
    )


    SCAN_PROCESS_COMPLETED = (
        "SCAN_PROCESS_COMPLETED"
    )


    SCAN_PROCESS_FAILED = (
        "SCAN_PROCESS_FAILED"
    )


    VULNERABILITY_IMPORTED = (
        "VULNERABILITY_IMPORTED"
    )


    STATUS_CHANGED = (
        "VULNERABILITY_STATUS_CHANGED"
    )


    LOGIN_SUCCESS = (
        "LOGIN_SUCCESS"
    )


    LOGIN_FAILED = (
        "LOGIN_FAILED"
    )


    TOKEN_CREATED = (
        "TOKEN_CREATED"
    )

    TOKEN_REFRESHED = (
        "TOKEN_REFRESHED"
    )

    TOKEN_VALIDATION_FAILED = (
        "TOKEN_VALIDATION_FAILED"
    )

    UNAUTHORIZED_ACCESS = (
        "UNAUTHORIZED_ACCESS"
    )

    ROLE_ACCESS_DENIED = (
        "ROLE_ACCESS_DENIED"
    )

    PASSWORD_CHANGED = (
        "PASSWORD_CHANGED"
    )

    USER_CREATED = (
        "USER_CREATED"
    )


    REFRESH_TOKEN_CREATED = (
        "REFRESH_TOKEN_CREATED"
    )

    REFRESH_TOKEN_USED = (
        "REFRESH_TOKEN_USED"
    )

    REFRESH_TOKEN_REVOKED = (
        "REFRESH_TOKEN_REVOKED"
    )

    LOGOUT_SUCCESS = (
        "LOGOUT_SUCCESS"
    )

    CHAT_COMPLETED = (
        "CHAT_COMPLETED"    
    )


    CHAT_FAILED = (
        "CHAT_FAILED"
    )