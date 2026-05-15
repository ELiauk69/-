<template>
  <div class="page">

    <!-- 左侧 -->
    <div class="left-panel">

      <div class="logo-card">
        <h1>AI Safety Inspection</h1>
        <p>Construction Site Detection Platform</p>
      </div>

      <div class="upload-card">

        <h2>Upload Detection Image</h2>

        <label class="upload-box">
          <input type="file" @change="uploadImage" hidden />
          <div class="upload-content">
            <span>Click Or Drag Image</span>
          </div>
        </label>

        <div v-if="imageUrl" class="image-area">
          <img :src="imageUrl" class="preview" />
        </div>

      </div>

    </div>

    <!-- 右侧 -->
    <div class="right-panel">

      <div class="status-card">
        <h2>AI Detection Status</h2>

        <div class="status-item">
          <span>Helmet Detection</span>
          <span class="success">Active</span>
        </div>

        <div class="status-item">
          <span>Safety Vest Detection</span>
          <span class="success">Active</span>
        </div>

        <div class="status-item">
          <span>Risk Analysis</span>
          <span class="warning">Monitoring</span>
        </div>
      </div>

      <div class="result-card" v-if="result">

        <h2>Detection Result</h2>

        <div class="result-box">
          {{ result }}
        </div>

      </div>

      <div class="statistics-card">

        <h2>System Statistics</h2>

        <div class="statistics-grid">

          <div class="stat-item">
            <h3>98%</h3>
            <p>Detection Accuracy</p>
          </div>

          <div class="stat-item">
            <h3>1.2s</h3>
            <p>Average Response</p>
          </div>

          <div class="stat-item">
            <h3>24/7</h3>
            <p>Monitoring</p>
          </div>

          <div class="stat-item">
            <h3>AI</h3>
            <p>YOLO Engine</p>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const imageUrl = ref('')
const result = ref('')

const uploadImage = async (event) => {

  const file = event.target.files[0]

  imageUrl.value = URL.createObjectURL(file)

  const formData = new FormData()
  formData.append('file', file)

  try {

    const response = await axios.post(
      'http://localhost:5000/detect',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    result.value = response.data.result

  } catch (e) {

    result.value = 'AI service connection failed'

  }
}
</script>

<style>

*{
  margin:0;
  padding:0;
  box-sizing:border-box;
}

body{
  background:#0f172a;
  font-family:Arial;
}

.page{
  display:flex;
  min-height:100vh;
  padding:30px;
  gap:30px;
  color:white;
}

.left-panel{
  flex:1;
}

.right-panel{
  width:420px;
  display:flex;
  flex-direction:column;
  gap:20px;
}

.logo-card{
  background:linear-gradient(135deg,#2563eb,#7c3aed);
  padding:30px;
  border-radius:20px;
  margin-bottom:20px;
  box-shadow:0 10px 30px rgba(0,0,0,0.3);
}

.logo-card h1{
  font-size:38px;
  margin-bottom:10px;
}

.logo-card p{
  opacity:0.8;
}

.upload-card{
  background:#1e293b;
  padding:30px;
  border-radius:20px;
}

.upload-box{
  border:2px dashed #3b82f6;
  height:260px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:20px;
  cursor:pointer;
  transition:0.3s;
  margin-top:20px;
}

.upload-box:hover{
  background:#172554;
}

.upload-content{
  font-size:22px;
  color:#93c5fd;
}

.image-area{
  margin-top:25px;
}

.preview{
  width:100%;
  border-radius:20px;
}

.status-card,
.result-card,
.statistics-card{
  background:#1e293b;
  padding:25px;
  border-radius:20px;
}

.status-item{
  display:flex;
  justify-content:space-between;
  margin-top:18px;
}

.success{
  color:#22c55e;
}

.warning{
  color:#f59e0b;
}

.result-box{
  margin-top:20px;
  background:#0f172a;
  padding:20px;
  border-radius:15px;
  color:#38bdf8;
  font-size:18px;
}

.statistics-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:15px;
  margin-top:20px;
}

.stat-item{
  background:#0f172a;
  padding:20px;
  border-radius:15px;
  text-align:center;
}

.stat-item h3{
  font-size:28px;
  color:#60a5fa;
  margin-bottom:10px;
}

.stat-item p{
  opacity:0.7;
}

</style>
