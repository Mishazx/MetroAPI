from MetroAPI import app, DEBUG, IP, PORT

if __name__ == '__main__':
    app.run(debug=DEBUG, host=IP, port=PORT)
