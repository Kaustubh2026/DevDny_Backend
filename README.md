# Smart Event Planner

A weather-based event planning system that helps users plan outdoor events based on weather conditions. The system provides weather analysis and alternative date suggestions for various types of events like cricket matches, weddings, and hiking trips.

## Features

- Event Management (CRUD operations)
- Weather Integration with OpenWeatherMap API
- Weather Suitability Analysis
- Alternative Date Suggestions
- Caching for Weather Data
- Comprehensive API Documentation

## Prerequisites

- Python 3.8+
- OpenWeatherMap API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-event-planner.git
cd smart-event-planner
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
venc\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

5. Add your OpenWeatherMap API key to the `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Events
- `POST /events/` - Create a new event
- `GET /events/` - List all events
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}` - Update event
- `DELETE /events/{event_id}` - Delete event

### Weather
- `GET /weather/{location}/{date}` - Get weather for location and date

### Recommendations
- `GET /events/{event_id}/suitability` - Get weather suitability analysis
- `GET /events/{event_id}/alternatives` - Get alternative date suggestions

## Example Usage

1. Create a new event:
```bash
curl -X POST "http://localhost:8000/events/" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Cricket Match",
           "location": "Mumbai",
           "date": "2024-03-16T10:00:00",
           "event_type": "cricket"
         }'
```

2. Check weather suitability:
```bash
curl "http://localhost:8000/events/1/suitability"
```

3. Get alternative dates:
```bash
curl "http://localhost:8000/events/1/alternatives"
```

## Testing

The API includes comprehensive test cases in the Postman collection. Import the `Weather Event Planner.postman_collection.json` file into Postman to run the tests.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 