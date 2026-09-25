from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Helper function to find an event by ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event

    return None


# POST /events
# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Check that JSON was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    # Check that title exists
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create the new event
    new_event = Event(new_id, data["title"])

    # Add it to our list
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id>
# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    # Check if event exists
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    # Check that JSON was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    # Check that title exists
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Update the title
    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# DELETE /events/<id>
# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    # Check if event exists
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the list
    events.remove(event)

    return jsonify({
        "message": "Event deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)