from flask import Flask, jsonify, request

app = Flask(__name__)

animals = [
    {"id": 1, "name": "dog", "age": 2},
    {"id": 2, "name": "cat", "age": 1}
    # ... und noch weitere Tier-Objekte möglich
]

@app.route("/")
def welcome():
    return "Hallo, das ist unsere erste Tier-API mit Flask"

# GET-Route, um alle Tiere anzuzeigen
@app.route("/api/animals", methods=["GET"])
def get_animals():
    return jsonify(animals), 200

# POST-Route, um ein Tier hinzuzufügen
@app.route("/api/animals", methods=["POST"])
def add_animal():
    new_animal = request.get_json() # Holen das neue Objekt aus dem Request-Objekt im Body im JSON-Format
    if not new_animal:
        return jsonify({"message": "Fehler, kein Objekt übergeben"}), 400
    animals.append(new_animal)
    return jsonify({"message": "Tier wurde erfolgreich hinzugefügt"}), 201

# DELETE-Route, um ein Tier aus der Liste zu löschen
@app.route("/api/animals/<name>", methods=["DELETE"]) # später id
def delete_animal(name):
    for animal in animals:
        if animal["name"] == name:
            animals.remove(animal)
            return jsonify({"message": "Tier wurde erfolgreich gelöscht"}), 200
    # sonst nicht gefunden
    return jsonify({"message": "Tier wurde nicht gefunden"}), 404

# PUT-Route, um ein Tier komplett zu aktualisieren
@app.route("/api/animals/<name>", methods=["PUT"]) # später id
def update_animal(name):
    updated_animal = request.get_json() # Objekt aus der Request speichern
    # Suche in Liste nach jeweiligen Objekt
    for animal in animals:
        if animal["name"] == name:
            animal.clear() # einmal die Werte des Tiers komplett löschen
            animal.update(updated_animal) # Setze die Werte von dem Objekt, was wir mitgesendet haben
            return jsonify({"message": "Tier wurde komplett aktualisiert"}), 200
    # wenn Tier in Liste nicht gefunden
    return jsonify({"message": "Tier wurde nicht gefunden"}), 404

# PATCH-Route, um vereinzelte Eigenschaften eines Tiers zu aktualisieren
@app.route("/api/animals/<name>", methods=["PATCH"])
def patch_animal(name):
    updated_animal = request.get_json() 
    for animal in animals:
        if animal["name"] == name:
            animal.update(updated_animal) # nur aktualisieren, kein Löschen und neu erstellen!
            return jsonify({"message": "Tier wurde geupdated"}), 200
    return jsonify({"message": "Tier wurde nicht gefunden"}), 404



if __name__ == "__main__":
    app.run(port=5050, debug=True)