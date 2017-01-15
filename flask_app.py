from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

#################################

app = Flask(__name__)
app.config["DEBUG"] = True

# DB CONFIG
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Nexus",
    password="MMdatabas3!",
    hostname="Nexus.mysql.pythonanywhere-services.com",
    databasename="Nexus$ordered_items",
    )

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

########## DB SETUP ##########

class patItem(db.Model):

    __tablename__ = "patTesting"

    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(50))
    item = db.Column(db.String(50))
    asset = db.Column(db.String(50))
    testType = db.Column(db.String(20))
    result = db.Column(db.String(50))
    tagNumber = db.Column(db.String(20))
    testPeriod = db.Column(db.String(20))
    tagExpiry = db.Column(db.String(50))
    notes = db.Column(db.String(300))

class ItemOrdered(db.Model):

    __tablename__ = "ordered"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    supplier = db.Column(db.String(50))
    item = db.Column(db.String(50))
    newUsed = db.Column(db.String(20))
    site = db.Column(db.String(50))
    reason = db.Column(db.String(100))
    requester = db.Column(db.String(20))

class ItemReceived(db.Model):

    __tablename__ = "received"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    supplier = db.Column(db.String(50))
    item = db.Column(db.String(50))
    newUsed = db.Column(db.String(20))
    site = db.Column(db.String(50))
    reason = db.Column(db.String(100))
    requester = db.Column(db.String(20))

class ItemDispatched(db.Model):

    __tablename__ = "dispatched"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    supplier = db.Column(db.String(50))
    item = db.Column(db.String(50))
    newUsed = db.Column(db.String(20))
    site = db.Column(db.String(50))
    reason = db.Column(db.String(100))
    requester = db.Column(db.String(20))


########## SITE INDEX ##########
@app.route("/")
def main():
	return render_template('index.html')

##########

@app.route("/ordered_items", methods=["GET", "POST"])
def ordered_items():
    if request.method == "GET":
        return render_template('ordered_items.html', ordered=ItemOrdered.query.all())
    else:
        item = ItemOrdered(
            date=request.form["date"],
            supplier=request.form["supplier"],
            item=request.form["item"],
            newUsed=request.form["new/used"],
            site=request.form["site"],
            reason=request.form["reason"],
            requester=request.form["requester"],
            )
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('ordered_items'))

##########

@app.route("/received_items", methods=["GET", "POST"])
def received_items():
    if request.method == "GET":
        return render_template('received_items.html', received=ItemReceived.query.all())

    item = ItemReceived(
        date=request.form["date"],
        supplier=request.form["supplier"],
        item=request.form["item"],
        newUsed=request.form["new/used"],
        site=request.form["site"],
        reason=request.form["reason"],
        requester=request.form["requester"],
        )

    db.session.add(item)
    db.session.commit()

    return redirect(url_for('received_items'))

##########

@app.route("/dispatched_items", methods=["GET", "POST"])
def dispatched_items():
    if request.method == "GET":
        return render_template('dispatched_items.html', dispatched=ItemDispatched.query.all())

    item = ItemDispatched(
        date=request.form["date"],
        supplier=request.form["supplier"],
        item=request.form["item"],
        newUsed=request.form["new/used"],
        site=request.form["site"],
        reason=request.form["reason"],
        requester=request.form["requester"],
        )
    db.session.add(item)
    db.session.commit()

    return redirect(url_for('dispatched_items'))

#################################
# PAT Testing

@app.route("/test/<siteName>", methods=["GET", "POST"])
def siteView(siteName):
    if request.method == "GET":
        return render_template('site_view.html', list=patItem.query.filter_by(site=siteName).all(), title=siteName)
    else:
        item = patItem(
        site=request.form["site"],
        item=request.form["item"],
        asset=request.form["asset"],
        testType=request.form["testType"],
        result=request.form["passFail"],
        tagNumber=request.form["tagNumber"],
        testPeriod=request.form["testPeriod"],
        tagExpiry=request.form["expiryDate"],
        notes=request.form["notes"],
        )
    db.session.add(item)
    db.session.commit()
    site = request.form["site"]

    return redirect(url_for('siteView', siteName=site))

@app.route("/deletePat/<id>", methods=["POST", "GET"])
def deletePat(id):
    entry = patItem.query.get(id)
    site = entry.site
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('siteView', siteName=site))

##########

@app.route("/deleteOrdered/<id>", methods=["POST", "GET"])
def deleteOrdered(id):
    entry = ItemOrdered.query.get(id)
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('ordered_items'))

@app.route("/deleteReceived/<id>", methods=["POST", "GET"])
def deleteReceived(id):
    entry = ItemReceived.query.get(id)
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('received_items'))

@app.route("/deleteDispatched/<id>", methods=["POST", "GET"])
def deleteDispatched(id):
    entry = ItemDispatched.query.get(id)
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('dispatched_items'))



#################################



