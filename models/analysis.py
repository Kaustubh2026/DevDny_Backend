from datetime import datetime

class EventWeatherAnalysis:
    def __init__(self, id=None, event_id=None, score=None, remarks=None, created_at=None):
        self.id = id
        self.event_id = event_id
        self.score = score
        self.remarks = remarks
        self.created_at = created_at or datetime.utcnow()

    @classmethod
    def from_supabase(cls, data):
        return cls(
            id=data.get('id'),
            event_id=data.get('event_id'),
            score=data.get('score'),
            remarks=data.get('remarks'),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'score': self.score,
            'remarks': self.remarks,
            'created_at': self.created_at
        } 