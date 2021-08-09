
import uuid

def is_uuid(str):
    try:
        uuid.UUID(str)
        return True
    except:
        return False
