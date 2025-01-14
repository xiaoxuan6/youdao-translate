import json

from flask import Flask, jsonify, request

from translate import Translate

app = Flask(__name__)


def response(code: int, msg: str, data=''):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data
    })


@app.route('/')
def main():
    return response(200, 'Welcome to youdao translate')


@app.route('/api/translate', methods=['GET'])
def translate():
    return response(500, 'method [get] not allow')


@app.route('/api/translate', methods=['POST'])
def translate_data():
    try:
        try:
            decoded_data = request.data.decode('utf-8')
        except UnicodeDecodeError as e:
            return response(400, 'Invalid UTF-8 encoding')

        try:
            received_data = json.loads(decoded_data)
        except json.JSONDecodeError as e:
            return response(400, 'Invalid JSON format')

        # 检查 JSON 数据是否包含键 'text'，并且 'text' 不能为空
        if not received_data or 'text' not in received_data or not received_data['text']:
            return response(500, 'params text not empty')

        t = Translate()
        result = t.run(received_data['text'])
        if result:
            return response(200, 'ok', result)
        else:
            return response(500, '翻译失败')
    except Exception as e:
        return response(500, str(e))


@app.errorhandler(404)
def page_not_found(e):
    return response(500, f'route [{request.path}] not found')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8888)
