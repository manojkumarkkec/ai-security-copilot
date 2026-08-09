from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SECURITY_ENGINEER = "SECURITY_ENGINEER"
    DEVELOPER = "DEVELOPER"
    VIEWER = "VIEWER"

class VulnerabilitySeverity(str, Enum):

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class VulnerabilityStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    ACCEPTED_RISK = "ACCEPTED_RISK"
    CLOSED = "CLOSED"

class ScanStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ScannerType(str, Enum):

    WIZ = "WIZ"

    TENABLE = "TENABLE"

    UNKNOWN = "UNKNOWN"