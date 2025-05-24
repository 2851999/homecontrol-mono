

class DuplicateRecordError(Exception):
    """Raised when attempting to insert a database record which has a duplicate unique key already in existence"""