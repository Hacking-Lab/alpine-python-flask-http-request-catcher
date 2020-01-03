import html
import datetime
import os
import codecs
from flask import Flask, jsonify, request, redirect, url_for

print()
app = Flask(__name__)


@app.route('/<path:any>', methods=['POST'])
def catchItPOST (any):
    today = datetime.datetime.today()
    file_url = today.strftime("%Y-%m-%d") + ".log"
    with codecs.open(file_url, 'a', "utf-8") as the_file:
        the_file.write("URL: " + str(request.url) + '\n')
        the_file.write("METHOD: POST \n")
        the_file.write("IP: " + str(request.remote_addr) + '\n')
        the_file.write("Time: " + today.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        the_file.write("Headers: \n" + str(request.headers) + '\n')
        the_file.write(u"Body: \n" + str(request.get_data()) + u'\n===================================================\n')

    return jsonify(True)

@app.route('/', methods=['GET'])
def print_usage():
    message = """<html>
    <head><link rel="stylesheet" type="text/css" href="not_available.css"></head>
    <body><H1>Request Catcher</H1></body>
    This web services has only two services <br><br>
    <a href="/">This page (usage)</a><br><br>and the URL for getting the captured data <br><br>
    <a href="/debug">Reading Captured Requests</a>
    </html>"""

    return message

@app.route('/debug', methods=['GET'])
def file_downloads():
    try:
        today = datetime.datetime.today()
        file_url = today.strftime("%Y-%m-%d") + ".log"
        with codecs.open(file_url, 'r', "utf-8") as the_file:
            text = html.escape(the_file.read())
            text1 = text.replace('\n','<br>')
        return text1

    except Exception as e:
        return redirect('/')

@app.route('/<path:any>', methods=['GET'])
def catchItGET (any):
    today = datetime.datetime.today()
    file_url = today.strftime("%Y-%m-%d") + ".log"
    with codecs.open(file_url, 'a', "utf-8") as the_file:
        the_file.write("URL: " + str(request.url) + '\n')
        the_file.write("METHOD: GET \n")
        the_file.write("IP: " + str(request.remote_addr) + '\n')
        the_file.write("Time: " + today.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        the_file.write("Headers: \n" + str(request.headers) + '\n')
        the_file.write(u"QueryString: \n" + str(request.query_string) + u'\n===================================================\n')

    return jsonify(True)


app.run(host="0.0.0.0", port="80", debug=True)
