from datetime import datetime

from bson.objectid import ObjectId


class Model:
    _id: ObjectId
    active: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
