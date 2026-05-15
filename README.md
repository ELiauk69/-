# AI 工地安全检测系统

基于 YOLO 的 AI 施工安全巡检平台。

## 功能特性

- 安全帽检测
- 反光衣/安全背心检测
- 施工人员检测
- 图片上传
- AI 风险分析
- 检测结果可视化

## 技术栈

### 前端
- Vue3
- Element Plus
- Axios

### 后端
- Spring Boot
- MyBatis
- MySQL

### AI 服务
- Flask
- YOLOv5
- OpenCV

## 系统工作流程

图片上传  
    ↓  
AI 检测  
    ↓  
风险分析  
    ↓  
数据库存储  
    ↓  
前端可视化

## 系统架构

Vue 前端  
    ↓  
SpringBoot 后端  
    ↓  
Flask AI 服务  
    ↓  
YOLO 检测模型

## 未来改进方向

- 多智能体调度
- 实时视频检测
- 云端部署
- 自动生成安全报告
