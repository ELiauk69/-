from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():

    file = request.files['file']

    # 这里可以接入 YOLO 模型
    # model.predict(...)

    return jsonify({
        'result': 'Helmet detected successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)
