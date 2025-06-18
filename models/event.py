from datetime import datetime

class Event:
    def __init__(self, id=None, name=None, location=None, date=None, event_type=None, category=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.event_type = event_type
        self.category = category
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def from_supabase(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            location=data.get('location'),
            date=data.get('date'),
            event_type=data.get('event_type'),
            category=data.get('category'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'event_type': self.event_type,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 