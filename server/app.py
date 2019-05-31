from eve import Eve

app = Eve()

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/api/session')
def session():
    return "{}"

if __name__ == '__main__':
    app.run()
