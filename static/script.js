document.addEventListener('DOMContentLoaded', function() {
    // Load events when page loads
    loadEvents();

    // Handle event form submission
    const form = document.getElementById('eventForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formMode = document.getElementById('formMode').textContent;
        if (formMode === 'Create Mode') {
            createEvent();
        } else {
            // Extract event ID from the form's data attribute
            const eventId = form.dataset.eventId;
            updateEvent(eventId);
        }
    });
});

// Create a new event
async function createEvent() {
    const eventData = {
        name: document.getElementById('eventName').value,
        location: document.getElementById('location').value,
        date: document.getElementById('eventDate').value,
        event_type: document.getElementById('eventType').value,
        category: document.getElementById('eventCategory').value
    };

    try {
        const response = await fetch('/events/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        });

        if (response.ok) {
            const event = await response.json();
            loadEvents();
            resetForm();
            showAlert('Event created successfully!', 'success');
        } else {
            showAlert('Failed to create event', 'danger');
        }
    } catch (error) {
        showAlert('Error creating event', 'danger');
    }
}

// Reset form to create mode
function resetForm() {
    const form = document.getElementById('eventForm');
    form.reset();
    form.removeAttribute('data-event-id');
    document.getElementById('formMode').textContent = 'Create Mode';
    document.getElementById('formMode').className = 'badge bg-primary';
    form.querySelector('button[type="submit"]').textContent = 'Create Event';
}

// Load all events
async function loadEvents() {
    try {
        const response = await fetch('/events/');
        const events = await response.json();
        displayEvents(events);
    } catch (error) {
        showAlert('Error loading events', 'danger');
    }
}

// Display events in the list
function displayEvents(events) {
    const eventList = document.getElementById('eventList');
    eventList.innerHTML = '';

    events.forEach(event => {
        const eventDate = new Date(event.date);
        const eventItem = document.createElement('div');
        eventItem.className = 'list-group-item';
        eventItem.dataset.date = event.date;
        eventItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h6 class="mb-1">${event.name}</h6>
                    <small class="text-muted">${event.location} - ${eventDate.toLocaleString()}</small>
                    <br>
                    <small class="text-muted">
                        <span class="badge bg-info">${event.category}</span>
                        <span class="badge bg-secondary">${event.event_type}</span>
                    </small>
                </div>
                <div>
                    <button class="btn btn-sm btn-primary me-2" onclick="checkWeather(${event.id})">
                        <i class="bi bi-cloud-sun"></i> Weather
                    </button>
                    <button class="btn btn-sm btn-warning me-2" onclick="editEvent(${event.id})">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-info me-2" onclick="viewWeatherHistory(${event.id})">
                        <i class="bi bi-clock-history"></i> History
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteEvent(${event.id})">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </div>
            </div>
        `;
        eventList.appendChild(eventItem);
    });
}

// Check weather for an event
async function checkWeather(eventId) {
    const weatherAnalysis = document.getElementById('weatherAnalysis');
    weatherAnalysis.innerHTML = '<div class="spinner"></div>';

    try {
        const response = await fetch(`/events/${eventId}/suitability`);
        const data = await response.json();
        
        const ratingClass = data.suitability_score.rating.toLowerCase();
        let weatherHtml = `
            <div class="weather-card">
                <h4>Weather Analysis</h4>
                <div class="weather-details">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="weather-info">
                                <h5>Temperature</h5>
                                <p class="temperature">${data.weather_data.main.temp}°C</p>
                            </div>
                            <div class="weather-info">
                                <h5>Conditions</h5>
                                <p>${data.weather_data.weather[0].description}</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="weather-info">
                                <h5>Humidity</h5>
                                <p>${data.weather_data.main.humidity}%</p>
                            </div>
                            <div class="weather-info">
                                <h5>Wind Speed</h5>
                                <p>${data.weather_data.wind.speed} m/s</p>
                            </div>
                        </div>
                    </div>
                    <div class="weather-score rating-${ratingClass}">
                        Suitability Score: ${data.suitability_score.score}/100
                    </div>
                    <div class="weather-remarks">
                        ${data.suitability_score.remarks}
                    </div>
                </div>
            </div>
        `;

        // Add alternative dates button if weather is poor
        if (data.suitability_score.rating.toLowerCase() === 'poor') {
            weatherHtml += `
                <div class="text-center mt-3">
                    <button class="btn btn-info" onclick="getAlternativeDates(${eventId})">
                        Get Alternative Dates
                    </button>
                </div>
            `;
        }

        weatherAnalysis.innerHTML = weatherHtml;
    } catch (error) {
        console.error('Weather check error:', error);
        weatherAnalysis.innerHTML = '<div class="alert alert-danger">Error checking weather</div>';
    }
}

// Get alternative dates
async function getAlternativeDates(eventId) {
    const weatherAnalysis = document.getElementById('weatherAnalysis');
    const currentContent = weatherAnalysis.innerHTML;
    weatherAnalysis.innerHTML = currentContent + '<div class="spinner"></div>';

    try {
        const response = await fetch(`/events/${eventId}/alternatives`);
        const alternatives = await response.json();
        
        let alternativesHtml = `
            <div class="weather-card mt-3">
                <h4>Alternative Dates</h4>
                <div class="list-group">
        `;

        alternatives.forEach(alt => {
            const date = new Date(alt.date).toLocaleDateString();
            const ratingClass = alt.rating.toLowerCase();
            alternativesHtml += `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${date}</h6>
                            <small class="text-muted">
                                Temperature: ${alt.temperature}°C<br>
                                Conditions: ${alt.conditions}<br>
                                ${alt.remarks}
                            </small>
                        </div>
                        <div class="weather-score rating-${ratingClass}">
                            ${alt.score}/100
                        </div>
                    </div>
                </div>
            `;
        });

        alternativesHtml += `
                </div>
            </div>
        `;

        weatherAnalysis.innerHTML = currentContent + alternativesHtml;
    } catch (error) {
        weatherAnalysis.innerHTML = currentContent + '<div class="alert alert-danger">Error getting alternative dates</div>';
    }
}

// Delete an event
async function deleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event?')) {
        try {
            const response = await fetch(`/events/${eventId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                loadEvents();
                showAlert('Event deleted successfully', 'success');
            } else {
                showAlert('Failed to delete event', 'danger');
            }
        } catch (error) {
            showAlert('Error deleting event', 'danger');
        }
    }
}

// Edit an event
async function editEvent(eventId) {
    try {
        const response = await fetch(`/events/${eventId}`);
        const event = await response.json();
        
        // Format date for datetime-local input
        const eventDate = new Date(event.date);
        const formattedDate = eventDate.toISOString().slice(0, 16);
        
        // Populate form with event data
        const form = document.getElementById('eventForm');
        form.dataset.eventId = eventId;  // Store event ID in form's data attribute
        document.getElementById('eventName').value = event.name;
        document.getElementById('location').value = event.location;
        document.getElementById('eventDate').value = formattedDate;
        document.getElementById('eventType').value = event.event_type;
        document.getElementById('eventCategory').value = event.category;
        
        // Update UI
        document.getElementById('formMode').textContent = 'Edit Mode';
        document.getElementById('formMode').className = 'badge bg-warning';
        form.querySelector('button[type="submit"]').textContent = 'Update Event';
        
        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showAlert('Error loading event data', 'danger');
    }
}

// Update an event
async function updateEvent(eventId) {
    const eventData = {
        name: document.getElementById('eventName').value,
        location: document.getElementById('location').value,
        date: document.getElementById('eventDate').value,
        event_type: document.getElementById('eventType').value,
        category: document.getElementById('eventCategory').value
    };

    try {
        const response = await fetch(`/events/${eventId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        });

        if (response.ok) {
            loadEvents();
            resetForm();
            showAlert('Event updated successfully!', 'success');
        } else {
            showAlert('Failed to update event', 'danger');
        }
    } catch (error) {
        showAlert('Error updating event', 'danger');
    }
}

// View weather history
async function viewWeatherHistory(eventId) {
    const weatherAnalysis = document.getElementById('weatherAnalysis');
    weatherAnalysis.innerHTML = '<div class="spinner"></div>';

    try {
        const response = await fetch(`/events/${eventId}/weather-history`);
        const history = await response.json();
        
        let historyHtml = `
            <div class="weather-card">
                <h4>Weather History</h4>
                <div class="list-group">
        `;

        history.forEach(record => {
            const date = new Date(record.date).toLocaleString();
            const ratingClass = record.rating.toLowerCase();
            historyHtml += `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${date}</h6>
                            <small class="text-muted">${record.remarks}</small>
                        </div>
                        <div class="weather-score rating-${ratingClass}">
                            ${record.score}/100
                        </div>
                    </div>
                </div>
            `;
        });

        historyHtml += `
                </div>
            </div>
        `;

        weatherAnalysis.innerHTML = historyHtml;
    } catch (error) {
        weatherAnalysis.innerHTML = '<div class="alert alert-danger">Error loading weather history</div>';
    }
}

// Filter events
function filterEvents(filter) {
    const eventList = document.getElementById('eventList');
    const events = Array.from(eventList.children);
    const now = new Date();

    events.forEach(event => {
        const eventDate = new Date(event.dataset.date);
        switch (filter) {
            case 'upcoming':
                event.style.display = eventDate > now ? '' : 'none';
                break;
            case 'past':
                event.style.display = eventDate < now ? '' : 'none';
                break;
            default: // 'all'
                event.style.display = '';
        }
    });
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
} 