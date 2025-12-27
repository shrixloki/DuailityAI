# DualityAI - Vercel Deployment Guide

## Overview
DualityAI is an AI-powered room clutter detection system with a React frontend and Python Flask backend.

## Project Structure
```
├── Web_App_frontend/          # React + TypeScript frontend
├── api/                       # Python Flask API for Vercel
├── src/                       # Original Python source code
├── mobile/                    # React Native mobile app
└── vercel.json               # Vercel deployment configuration
```

## Deployment to Vercel

### Prerequisites
1. GitHub account with this repository
2. Vercel account connected to GitHub

### Steps
1. **Connect Repository to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import from GitHub: `shrixloki/DuailityAI`

2. **Configure Build Settings**
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: `cd Web_App_frontend && npm run build`
   - Output Directory: `Web_App_frontend/dist`

3. **Environment Variables** (if needed)
   - Add any required environment variables in Vercel dashboard

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically build and deploy both frontend and API

## API Endpoints

### Health Check
```
GET /api/health
```

### Object Detection
```
POST /api/detect
Content-Type: multipart/form-data
Body: image file
```

### Available Models
```
GET /api/models
```

## Frontend Features
- Modern React UI with TypeScript
- Multiple landing page designs
- Image upload and detection demo
- Responsive design with Tailwind CSS
- Component library with shadcn/ui

## Local Development

### Frontend
```bash
cd Web_App_frontend
npm install
npm run dev
```

### API (Local Testing)
```bash
cd api
pip install -r requirements.txt
python index.py
```

## Notes
- The deployed API uses mock responses for demonstration
- For production, integrate with actual ML model hosting service
- Large ML models are not suitable for Vercel's serverless functions
- Consider using external services like Hugging Face, AWS SageMaker, or Google Cloud AI Platform for model inference

## Repository
https://github.com/shrixloki/DuailityAI