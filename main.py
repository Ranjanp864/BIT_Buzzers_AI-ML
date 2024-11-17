from flask import Flask,render_template,request,jsonify
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "pythoncourse123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)
df1 = pd.read_csv("linkedin_data_with_names.csv")
df2 = pd.read_csv("instagram_data_with_names.csv")
df3 = pd.read_csv("facebook_data_with_names.csv")

user_ids1 = df1["LinkedIn User ID"].tolist()
user_ids2 = df2["Instagram User ID"].tolist()
user_ids3 = df3["Facebook User ID"].tolist()

notifications = []


class Form(db.Model) :
    user_id = db.Column(db.String(20),primary_key=True)
    platform = db.Column(db.String(80))
    Last_Updated_Post_Time = db.Column(db.String(80))
    Last_Updated_Comment_Time = db.Column(db.String(80))



@app.route("/",)
def home() :
    return render_template("home.html")


@app.route("/linkedincontacts",)
def linkedin_contacts() :
    return render_template("key_contacts1.html")

@app.route("/instagramcontacts",)
def instagram_contacts() :
    return render_template("key_contacts2.html")

@app.route("/facebookcontacts",)
def facebook_contacts() :
    return render_template("key_contacts3.html")

@app.route("/newposts1",)
def linkedin_posts() :
    return render_template("newposts1.html")


@app.route("/database", methods=["GET", "POST"])
def databases():
    if request.method == "POST":
        User_ID = request.form["user_id"]
        platform = None
        last_updated_post_time = None
        last_updated_comment_time = None

        # Check the platform for LinkedIn
        if User_ID in user_ids1:
            platform = "LinkedIn"
            last_updated_post_time = df1[df1["LinkedIn User ID"] == User_ID][
                "Last Updated Post Time"].iloc[0]
            last_updated_comment_time = \
            df1[df1["LinkedIn User ID"] == User_ID][
                "Last Updated Comment Time"].iloc[0]

        # Check the platform for Instagram
        elif User_ID in user_ids2:
            platform = "Instagram"
            last_updated_post_time = df2[df2["Instagram User ID"] == User_ID][
                "Last Updated Post Time"].iloc[0]
            last_updated_comment_time = \
            df2[df2["Instagram User ID"] == User_ID][
                "Last Updated Comment Time"].iloc[0]

        # Check the platform for Facebook
        elif User_ID in user_ids3:
            platform = "Facebook"
            last_updated_post_time = df3[df3["Facebook User ID"] == User_ID][
                "Last Updated Post Time"].iloc[0]
            last_updated_comment_time = \
            df3[df3["Facebook User ID"] == User_ID][
                "Last Updated Comment Time"].iloc[0]

        # Check if user ID already exists in the database
        existing_form = Form.query.filter_by(user_id=User_ID).first()

        if existing_form:
            # If the user already exists, update the existing record
            existing_form.platform = platform
            existing_form.Last_Updated_Post_Time = last_updated_post_time
            existing_form.Last_Updated_Comment_Time = last_updated_comment_time
            db.session.commit()
            return "Data updated successfully!"
        else:
            if platform and last_updated_post_time and last_updated_comment_time:
                form = Form(user_id=User_ID, platform=platform,
                            Last_Updated_Post_Time=last_updated_post_time,
                            Last_Updated_Comment_Time=last_updated_comment_time)
                db.session.add(form)
                db.session.commit()
                return "Data saved successfully!"
            else:
                return "User ID not found or data is incomplete.", 404

    return render_template(
        "home.html")  # If it's a GET request, render the form


@app.route('/suggest1', methods=['GET'])
def suggest1():
    query = request.args.get('query', '').lower()
    suggestions = [uid for uid in user_ids1 if query in uid.lower()]
    return jsonify(suggestions)

@app.route('/suggest2', methods=['GET'])
def suggest2():
    query = request.args.get('query', '').lower()
    suggestions = [uid for uid in user_ids2 if query in uid.lower()]
    return jsonify(suggestions)

@app.route('/suggest3', methods=['GET'])
def suggest3():
    query = request.args.get('query', '').lower()
    suggestions = [uid for uid in user_ids3 if query in uid.lower()]
    return jsonify(suggestions)


@app.route("/database2", methods=["GET", "POST"])
def databases2():
    if request.method == "POST":
        User_ID = request.form["user_id"]
        # Fetch all records and extract the 'user_id' column
        user_ids = [form.user_id for form in Form.query.all()]
        if User_ID in user_ids:
            message = "New Post from "+User_ID
            notifications.append(message)
            return render_template("home.html", notifications=notifications)
    return render_template("home.html", notifications=[])



if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
        app.run(debug=True,port=5000)