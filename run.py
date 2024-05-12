from Metro_API import flask, DEBUG, IP, PORT

if __name__ == '__main__':
    flask.run(debug=DEBUG, host=IP, port=PORT)
