from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/detect', methods=['POST'])
def detect():
    """AI 目标检测接口"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = file.filename
    
    # 模拟 YOLO 检测结果
    # 实际部署时这里替换为 YOLO 模型推理
    
    # 随机模拟检测结果 (演示用)
    has_helmet = random.choice([True, False])
    has_vest = random.choice([True, False])
    person_count = random.randint(1, 8)
    
    # 风险判断
    risks = []
    if not has_helmet:
        risks.append("⚠️ 未佩戴安全帽")
    if not has_vest:
        risks.append("⚠️ 未穿反光衣")
    
    if risks:
        risk_level = "HIGH" if len(risks) >= 2 else "MEDIUM"
        summary = f"检测到 {len(risks)} 项安全隐患"
    else:
        risk_level = "SAFE"
        summary = "所有人员 PPE 佩戴齐全 ✅"
    
    result = {
        'filename': filename,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'detections': {
            'person_count': person_count,
            'helmet_detected': has_helmet,
            'vest_detected': has_vest,
            'helmet_count': random.randint(0, person_count) if has_helmet else 0,
            'vest_count': random.randint(0, person_count) if has_vest else 0
        },
        'risk_analysis': {
            'level': risk_level,
            'risks': risks,
            'summary': summary,
            'recommendations': [
                "所有人员必须正确佩戴安全帽",
                "夜间/低可见度环境必须穿反光衣",
                "安全员需每日检查 PPE"
            ] if risks else ["继续保持良好安全习惯"]
        },
        'result_summary': f"📊 检测完成 | 共 {person_count} 人 | 安全帽: {'✓' if has_helmet else '✗'} | 反光衣: {'✓' if has_vest else '✗'} | {summary}"
    }
    
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'YOLO Detection API'})

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 AI 工地安全检测服务启动")
    print("📍 地址: http://localhost:5000")
    print("📡 检测接口: POST /detect")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
