# 🚀 DUALITY AI - Full Stack Startup Guide

This guide explains how to run the complete DUALITY AI application stack without Docker.

## 📋 Prerequisites

### Required Software
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning/updates)

### Required Python Packages
```bash
pip install flask flask-cors ultralytics pillow torch numpy requests
```

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for models and dependencies
- **GPU**: Optional (CUDA-compatible for faster inference)

## 🎯 Quick Start Options

### Option 1: Full Stack (Recommended)
Starts all services with monitoring and health checks:

```bash
# Windows
python run_full_stack.py

# Linux/Mac
python3 run_full_stack.py
```

### Option 2: Simple Start
Minimal startup for development:

```bash
# Windows
python start.py

# Linux/Mac  
python3 start.py
```

### Option 3: Platform Scripts
Use the provided platform-specific scripts:

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

## 🔧 Advanced Options

### Include Mobile Development
Start with React Native Metro bundler:

```bash
python run_full_stack.py --mobile
```

### Headless Mode
Start without opening browser automatically:

```bash
python run_full_stack.py --no-browser
```

## 🌐 Service URLs

Once started, the following services will be available:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web application |
| **Model API** | http://localhost:8000 | AI model inference API |
| **Web Backend** | http://localhost:8001 | Web application backend |
| **Mobile Metro** | http://localhost:8081 | React Native bundler (if enabled) |

## 📊 Health Checks

Check if services are running:

- Model API: http://localhost:8000/api/health
- Web Backend: http://localhost:8001/api/health
- Frontend: Check console output for Vite dev server URL

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
If you get port conflicts:
1. Check what's using the port: `netstat -ano | findstr :8000`
2. Kill the process or use different ports
3. Restart the application

#### Missing Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd Web_App_frontend
npm install
```

#### Model Files Not Found
Ensure model files exist in:
- `models/weights/FINAL_SELECTED_MODEL.pt`
- `models/weights/best.pt`

If missing, train models first or download pre-trained weights.

#### Frontend Build Issues
```bash
cd Web_App_frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Performance Issues

#### Slow Model Loading
- Ensure adequate RAM (8GB+)
- Use GPU acceleration if available
- Close other resource-intensive applications

#### Frontend Slow to Load
- Check Node.js version (16+ recommended)
- Clear browser cache
- Disable browser extensions

## 🔄 Development Workflow

### Making Changes

1. **Backend Changes**: 
   - Edit files in `src/` or `app/`
   - Restart with `Ctrl+C` and rerun startup script

2. **Frontend Changes**:
   - Edit files in `Web_App_frontend/src/`
   - Hot reload should work automatically

3. **Model Changes**:
   - Update model files in `models/weights/`
   - Restart Model API service

### Testing

```bash
# Test Model API
curl http://localhost:8000/api/health

# Test Web Backend  
curl http://localhost:8001/api/health

# Test Frontend
# Open browser to http://localhost:3000
```

## 📱 Mobile Development

### Prerequisites for Mobile
- **Android Studio** (for Android development)
- **Xcode** (for iOS development, Mac only)
- **React Native CLI**: `npm install -g react-native-cli`

### Starting Mobile Development
```bash
# Start with mobile support
python run_full_stack.py --mobile

# In another terminal, run on device
cd mobile
npx react-native run-android  # or run-ios
```

## 🚀 Production Deployment

For production deployment, see:
- `DEPLOYMENT.md` - Production deployment guide
- `FRONTEND_DEPLOYMENT.md` - Frontend-specific deployment
- `render.yaml` - Render.com configuration

## 📞 Support

### Getting Help
1. Check console output for error messages
2. Verify all prerequisites are installed
3. Check the troubleshooting section above
4. Review log files in the console output

### Logs and Debugging
The startup script provides detailed logging:
- `[TIMESTAMP] COMPONENT: MESSAGE`
- Monitor for error messages and warnings
- Use `--no-browser` flag to see all console output

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ All dependency checks pass
- ✅ All services show "ready" status
- ✅ Browser opens to the frontend automatically
- ✅ You can upload images and get detection results
- ✅ Health check endpoints return 200 OK

---

**Happy coding! 🚀**