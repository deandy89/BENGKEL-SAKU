# app.py
# Required Imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

# @app.route('/', methods=['GET'])
#     return jsonify({"success": True}), 200

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/list', methods=['GET'])
def read():
    """
        all_todos : Return all documents
    """
    try:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/list/<idlist>', methods=['GET'])
def readOne(idlist):
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
            todo = todo_ref.document(idlist).get()
            return jsonify(todo.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/delete/<delID>', methods=['GET', 'DELETE'])
def delete(delID):
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        todo = todo_ref.document(delID).get()
        if todo.to_dict():
            todo_ref.document(delID).delete()
            return jsonify({
                "success": True
            }), 200
        else : 
             return jsonify({
                "error": True
            }), 404
    except Exception as e:
        return f"An Error Occured: {e}"
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)