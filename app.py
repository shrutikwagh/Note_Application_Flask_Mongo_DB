from flask import request,Flask,render_template,redirect
import datetime
from bson import ObjectId

from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.flaskCrashCourse
col = db.notes

# app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskCrashCourse"
# mongo = PyMongo(app)

@app.route('/')
def home():
    notes=db.notes.find()
    return render_template('pages/home.html',notes=notes)


@app.route("/add-note", methods=['GET','POST'])
def addNote():
    if(request.method == "GET"):

        return render_template("pages/add-note.html",homeIsActive=False,addNoteIsActive=True)

    elif (request.method == "POST"):

        print(request.form)
        # get the fields data

        title = request.form['title']
        description = request.form['description']
        createdAt = datetime.datetime.now()
        # save the record to the database
        # mongo.db.notes.insert({"title":title,"description":description,"createdAt":createdAt})
        db.notes.insert_one({
            "title": title,
            "description":description,
            "createdAt": createdAt
        })

        # redirect to home page
        return redirect("/")


@app.route('/edit-note', methods=['GET','POST'])
def editNote():

    if request.method == "GET":

        # get the id of the note to edit
        noteId = request.args.get('form')
        print(noteId,'note_id')

        # get the note details from the db
        note = dict(db.notes.find_one({"_id":ObjectId(noteId)}))

        # direct to edit note page
        return render_template('pages/edit-note.html',note=note)

    elif request.method == "POST":

        #get the data of the note
        noteId = request.form['_id']
        title = request.form['title']
        description = request.form['description']

        # update the data in the db
        db.notes.update_one({"_id":ObjectId(noteId)},{"$set":{"title":title,"description":description}})

        # redirect to home page
        return redirect("/")



@app.route('/delete-note', methods=['POST'])
def deleteNote():

    # get the id of the note to delete
    noteId = request.form['_id']

    # delete from the database
    db.notes.delete_one({ "_id": ObjectId(noteId)})

    # redirect to home page
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
