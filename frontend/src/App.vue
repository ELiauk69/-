<template>
  <div class="page">
    <!-- 左侧面板 -->
    <div class="left-panel">
      <div class="logo-card">
        <h1>🏗️ AI Safety Inspection</h1>
        <p>YOLO 智能工地安全检测平台</p>
      </div>

      <div class="upload-card">
        <h2>📤 上传检测图片</h2>
        
        <label class="upload-box" @dragover.prevent @drop.prevent="handleDrop">
          <input 
            type="file" 
            @change="handleFileSelect" 
            accept="image/*" 
            hidden 
            ref="fileInput"
          />
          <div class="upload-content" @click="$refs.fileInput.click()">
            <span>📸 点击或拖拽图片到此处</span>
            <p>支持 JPG、PNG 格式</p>
          </div>
        </label>

        <div v-if="imageUrl" class="image-area">
          <img :src="imageUrl" class="preview" alt="预览图片" />
          <div v-if="isLoading" class="loading-overlay">
            <div class="spinner"></div>
            <span>AI 分析中...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧面板 -->
    <div class="right-panel">
      <div class="status-card">
        <h2>🟢 检测状态</h2>
        <div class="status-item">
          <span>⛑️ 安全帽检测</span>
          <span class="success">● Active</span>
        </div>
        <div class="status-item">
          <span>🦺 反光衣检测</span>
          <span class="success">● Active</span>
        </div>
        <div class="status-item">
          <span>⚠️ 风险分析引擎</span>
          <span class="warning">● Monitoring</span>
        </div>
      </div>

      <div class="result-card" v-if="detectionResult">
        <h2>📊 检测结果</h2>
        <div class="result-box" :class="riskClass">
          <div class="result-header">
            <strong>{{ detectionResult.filename }}</strong>
            <span class="badge" :class="riskBadgeClass">
              {{ riskText }}
            </span>
          </div>
          
          <div class="detection-stats">
            <div class="stat-row">
              <span>👥 检测人数</span>
              <strong>{{ detectionResult.detections?.person_count || 0 }} 人</strong>
            </div>
            <div class="stat-row">
              <span>⛑️ 安全帽</span>
              <span :class="detectionResult.detections?.helmet_detected ? 'text-success' : 'text-danger'">
                {{ detectionResult.detections?.helmet_detected ? '✓ 已检测到' : '✗ 未检测到' }}
              </span>
            </div>
            <div class="stat-row">
              <span>🦺 反光衣</span>
              <span :class="detectionResult.detections?.vest_detected ? 'text-success' : 'text-danger'">
                {{ detectionResult.detections?.vest_detected ? '✓ 已检测到' : '✗ 未检测到' }}
              </span>
            </div>
          </div>

          <div v-if="detectionResult.risk_analysis?.risks?.length" class="risks-section">
            <div class="risks-title">⚠️ 安全隐患</div>
            <ul>
              <li v-for="risk in detectionResult.risk_analysis.risks" :key="risk">{{ risk }}</li>
            </ul>
          </div>

          <div class="summary-section">
            <div class="summary-text">{{ detectionResult.result_summary }}</div>
            <div class="timestamp">🕐 {{ detectionResult.timestamp }}</div>
          </div>
        </div>
      </div>

      <div class="statistics-card">
        <h2>📈 系统统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <h3>98.5%</h3>
            <p>检测准确率</p>
          </div>
          <div class="stat-item">
            <h3>0.8s</h3>
            <p>平均响应</p>
          </div>
          <div class="stat-item">
            <h3>24/7</h3>
            <p>实时监控</p>
          </div>
          <div class="stat-item">
            <h3>YOLO</h3>
            <p>AI 引擎</p>
          </div>
        </div>
        <button class="clear-btn" @click="clearResult" v-if="detectionResult">
          清空结果
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const imageUrl = ref('')
const detectionResult = ref(null)
const isLoading = ref(false)

// 风险等级样式
const riskClass = ref('')
const riskBadgeClass = ref('')
const riskText = ref('')

const updateRiskStyles = (level) => {
  switch(level) {
    case 'HIGH':
      riskClass.value = 'risk-high'
      riskBadgeClass.value = 'badge-high'
      riskText.value = '🔴 高风险'
      break
    case 'MEDIUM':
      riskClass.value = 'risk-medium'
      riskBadgeClass.value = 'badge-medium'
      riskText.value = '🟡 中风险'
      break
    case 'SAFE':
      riskClass.value = 'risk-safe'
      riskBadgeClass.value = 'badge-safe'
      riskText.value = '🟢 安全'
      break
    default:
      riskClass.value = ''
      riskBadgeClass.value = ''
      riskText.value = '未知'
  }
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (file) await processFile(file)
}

const handleDrop = async (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    await processFile(file)
  }
}

const processFile = async (file) => {
  // 预览
  imageUrl.value = URL.createObjectURL(file)
  detectionResult.value = null
  isLoading.value = true

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await axios.post('/api/detect', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 30000
    })
    detectionResult.value = response.data
    updateRiskStyles(response.data.risk_analysis?.level)
  } catch (error) {
    console.error(error)
    detectionResult.value = {
      filename: file.name,
      timestamp: new Date().toLocaleString(),
      detections: { person_count: 0, helmet_detected: false, vest_detected: false },
      risk_analysis: { level: 'ERROR', risks: ['服务连接失败'], summary: '' },
      result_summary: '❌ AI 服务连接失败\n请确保后端服务已启动: cd backend && python app.py'
    }
    updateRiskStyles('ERROR')
  } finally {
    isLoading.value = false
    // 清空 input 以便再次上传同一文件
    if (fileInput.value) fileInput.value.value = ''
  }
}

const clearResult = () => {
  detectionResult.value = null
  imageUrl.value = ''
}
</script>

<style scoped>
.page {
  display: flex;
  min-height: 100vh;
  padding: 30px;
  gap: 30px;
  color: white;
  max-width: 1600px;
  margin: 0 auto;
}

.left-panel {
  flex: 1;
  min-width: 0;
}

.right-panel {
  width: 450px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.logo-card, .upload-card, .status-card, .result-card, .statistics-card {
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 28px;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.logo-card {
  background: linear-gradient(135deg, #1e40af, #6d28d9);
  border: none;
  margin-bottom: 20px;
}

.logo-card h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

.logo-card p {
  opacity: 0.85;
}

.upload-card h2, .status-card h2, .result-card h2, .statistics-card h2 {
  font-size: 20px;
  margin-bottom: 16px;
}

.upload-box {
  border: 2px dashed #3b82f6;
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(15, 23, 42, 0.5);
}

.upload-box:hover {
  background: #1e3a8a;
  border-color: #60a5fa;
}

.upload-content {
  text-align: center;
}

.upload-content span {
  display: inline-block;
  padding: 12px 24px;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 40px;
  font-size: 18px;
}

.upload-content p {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 12px;
}

.image-area {
  margin-top: 20px;
  position: relative;
}

.preview {
  width: 100%;
  border-radius: 16px;
  border: 2px solid #3b82f6;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #3b82f6;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.status-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.status-item:last-child {
  border-bottom: none;
}

.success { color: #22c55e; font-weight: 600; }
.warning { color: #f59e0b; }
.text-success { color: #22c55e; }
.text-danger { color: #ef4444; }

.result-box {
  margin-top: 16px;
  background: #0f172a;
  padding: 20px;
  border-radius: 16px;
  font-size: 14px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-high { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
.badge-medium { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
.badge-safe { background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid #22c55e; }

.risk-high { border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.1); }
.risk-medium { border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.1); }
.risk-safe { border-left: 4px solid #22c55e; background: rgba(34, 197, 94, 0.1); }

.detection-stats {
  margin-bottom: 16px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.risks-section {
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 12px;
}

.risks-title {
  color: #f59e0b;
  margin-bottom: 8px;
  font-weight: 600;
}

.risks-section ul {
  margin-left: 20px;
}

.summary-section {
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-text {
  margin-bottom: 8px;
  line-height: 1.5;
}

.timestamp {
  font-size: 11px;
  opacity: 0.6;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.stat-item {
  background: rgba(15, 23, 42, 0.8);
  padding: 16px;
  border-radius: 16px;
  text-align: center;
}

.stat-item h3 {
  font-size: 26px;
  color: #60a5fa;
  margin-bottom: 8px;
}

.stat-item p {
  font-size: 12px;
  opacity: 0.7;
}

.clear-btn {
  width: 100%;
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid #ef4444;
  padding: 10px;
  border-radius: 12px;
  color: #ef4444;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: rgba(239, 68, 68, 0.4);
}

@media (max-width: 900px) {
  .page {
    flex-direction: column;
    padding: 20px;
  }
  .right-panel {
    width: 100%;
  }
}
</style>
