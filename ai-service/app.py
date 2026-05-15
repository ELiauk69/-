from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # 模拟 YOLO 检测结果
    has_helmet = random.choice([True, False])
    has_vest = random.choice([True, False])
    person_count = random.randint(1, 8)
    
    risks = []
    if not has_helmet:
        risks.append("未佩戴安全帽")
    if not has_vest:
        risks.append("未穿反光衣")
    
    if risks:
        risk_level = "HIGH" if len(risks) >= 2 else "MEDIUM"
        summary = f"检测到 {len(risks)} 项安全隐患"
    else:
        risk_level = "SAFE"
        summary = "所有人员 PPE 佩戴齐全"
    
    result = {
        'filename': file.filename,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'detections': {
            'person_count': person_count,
            'helmet_detected': has_helmet,
            'vest_detected': has_vest
        },
        'risk_analysis': {
            'level': risk_level,
            'risks': risks,
            'summary': summary
        },
        'result_summary': f"共 {person_count} 人 | 安全帽: {'✓' if has_helmet else '✗'} | 反光衣: {'✓' if has_vest else '✗'} | {summary}"
    }
    
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 AI 服务启动: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
