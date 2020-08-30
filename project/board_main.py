from flask import Flask, render_template, url_for
from pymongo import MongoClient
from youtube import get_vid
from get_wise import get_Wise

# from STU_Notice import get_stu_notices

app = Flask(__name__)

@app.route("/")
def home():
    wise_saying = get_Wise()
    return render_template('home.html',wise_saying = wise_saying)


@app.route('/board', methods=['GET','POST'])
def Scrapping_notices():
    client = MongoClient()
    db = client.Board_DB
    col1 = db.CSE_Notice_Collection.find()
    col2 = db.EMP_Collection.find()
    col3 = db.INFO_IND_Collection.find()
    col4 = db.SSS_Collection.find()
    return render_template('board_main.html', scp_notices=col1, scp_pusanits=col3, scp_emps=col2, scp_smarts=col4,) # scp_stu_notices = stu_notices



@app.route("/motivation")
def mot():
    client = MongoClient()
    db = client.Board_DB
    col5 = db.Youtube_Collection.find()
    return render_template('youtube.html',videos = col5)

@app.route("/job")
def job():
    client = MongoClient()
    db = client.Board_DB
    col6 = db.Youtube_Collection2.find()
    return render_template('youtube.html',videos = col6)

@app.route("/coding")
def code():
    client = MongoClient()
    db = client.Board_DB
    col7 = db.Youtube_Collection3.find()
    return render_template('youtube.html',videos = col7)



if __name__ == '__main__':
    app.run()
