from datetime import datetime

class WeatherData:
    def __init__(self, id=None, event_id=None, temperature=None, wind_speed=None, precipitation=None, condition=None, timestamp=None):
        self.id = id
        self.event_id = event_id
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.condition = condition
        self.timestamp = timestamp or datetime.utcnow()

    @classmethod
    def from_supabase(cls, data):
        return cls(
            id=data.get('id'),
            event_id=data.get('event_id'),
            temperature=data.get('temperature'),
            wind_speed=data.get('wind_speed'),
            precipitation=data.get('precipitation'),
            condition=data.get('condition'),
            timestamp=data.get('timestamp')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'temperature': self.temperature,
            'wind_speed': self.wind_speed,
            'precipitation': self.precipitation,
            'condition': self.condition,
            'timestamp': self.timestamp
        } 