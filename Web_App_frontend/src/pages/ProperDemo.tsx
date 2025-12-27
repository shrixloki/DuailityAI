import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Home } from 'lucide-react';
import './ProperDemo.css';

interface Detection {
  bbox: [number, number, number, number];
  confidence: number;
  class_id: number;
  class_name: string;
}

interface Model {
  id: string;
  name: string;
  description: string;
  performance: {
    mAP50: number;
    precision: number;
    recall: number;
  };
  classes: string[];
  status: 'production' | 'training' | 'experimental';
  available: boolean;
}

interface PredictionResult {
  success: boolean;
  model_used: string;
  model_name: string;
  image_size: [number, number];
  detections: Detection[];
  detection_count: number;
  confidence_threshold: number;
  timestamp: string;
}

const ProperDemo: React.FC = () => {
  const navigate = useNavigate();
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('flagship');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [results, setResults] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confidence, setConfidence] = useState(0.5);
  const [loading, setLoading] = useState(true);

  const apiUrl = 'http://localhost:8000';

  // Fetch available models
  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      setLoading(true);
      console.log('🔍 Fetching models from API...');
      
      const response = await fetch(`${apiUrl}/api/models`);
      console.log('📥 Models response:', response.status);
      
      const data = await response.json();
      console.log('📊 Models data:', data);
      
      if (data.success) {
        console.log('✅ Models fetched successfully:', data.models.length);
        setModels(data.models);
        // Set first available model as default
        const availableModel = data.models.find((m: Model) => m.available);
        if (availableModel) {
          console.log('🎯 Setting default model:', availableModel.id);
          setSelectedModel(availableModel.id);
        }
      } else {
        console.log('❌ Failed to fetch models:', data);
        setError('Failed to fetch models');
      }
    } catch (err) {
      console.error('💥 Model fetch error:', err);
      setError('Error connecting to model API');
    } finally {
      setLoading(false);
    }
  };

  const handleImageSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setResults(null);
      setError(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setResults(null);
      setError(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const handleDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  }, []);

  const runPrediction = async () => {
    if (!selectedImage) return;

    console.log('🎯 Starting prediction...');
    setPredicting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('model', selectedModel);
      formData.append('confidence', confidence.toString());

      console.log('📤 Sending request to API...');
      console.log('Model:', selectedModel);
      console.log('Confidence:', confidence);
      console.log('Image:', selectedImage.name);

      const response = await fetch(`${apiUrl}/api/predict`, {
        method: 'POST',
        body: formData,
      });

      console.log('📥 Response received:', response.status);

      const data = await response.json();
      console.log('📊 Response data:', data);

      if (data.success) {
        console.log('✅ Prediction successful');
        setResults(data);
      } else {
        console.log('❌ Prediction failed:', data.error);
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      console.error('💥 Request error:', err);
      setError('Error connecting to prediction API');
    } finally {
      setPredicting(false);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
  };

  const getStatusBadge = (status: string, available: boolean) => {
    if (!available) return 'unavailable';
    switch (status) {
      case 'production': return 'production';
      case 'training': return 'training';
      case 'experimental': return 'experimental';
      default: return 'unknown';
    }
  };

  const selectedModelData = models.find(m => m.id === selectedModel);

  if (loading) {
    return (
      <div className="duality-app">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading DUALITY AI System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="duality-app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <Button 
              onClick={() => navigate('/')}
              variant="ghost" 
              size="sm"
              className="text-white hover:bg-white/10 mr-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
            <div className="logo-icon">🛡️</div>
            <div className="logo-text">
              <h1>DUALITY AI</h1>
              <p>Visual Inference System for Target Assessment</p>
            </div>
          </div>
          <div className="status-indicator">
            <div className="status-dot active"></div>
            <span>System Online</span>
          </div>
        </div>
      </header>

      <div className="main-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="model-selector-section">
            <h3>🎯 Model Selection</h3>
            <div className="model-dropdown">
              <select 
                value={selectedModel} 
                onChange={(e) => setSelectedModel(e.target.value)}
                className="model-select"
              >
                {models.map((model) => (
                  <option 
                    key={model.id} 
                    value={model.id}
                    disabled={!model.available}
                  >
                    {model.name} {!model.available ? '(Unavailable)' : ''}
                  </option>
                ))}
              </select>
            </div>

            {selectedModelData && (
              <div className="model-info">
                <div className="model-header">
                  <h4>{selectedModelData.name}</h4>
                  <span className={`status-badge ${getStatusBadge(selectedModelData.status, selectedModelData.available)}`}>
                    {selectedModelData.status}
                  </span>
                </div>
                <p className="model-description">{selectedModelData.description}</p>
                
                <div className="performance-metrics">
                  <h5>Performance Metrics</h5>
                  <div className="metric">
                    <span>mAP50</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill" 
                        style={{ width: `${selectedModelData.performance.mAP50 * 100}%` }}
                      ></div>
                    </div>
                    <span>{(selectedModelData.performance.mAP50 * 100).toFixed(1)}%</span>
                  </div>
                  <div className="metric">
                    <span>Precision</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill" 
                        style={{ width: `${selectedModelData.performance.precision * 100}%` }}
                      ></div>
                    </div>
                    <span>{(selectedModelData.performance.precision * 100).toFixed(1)}%</span>
                  </div>
                  <div className="metric">
                    <span>Recall</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill" 
                        style={{ width: `${selectedModelData.performance.recall * 100}%` }}
                      ></div>
                    </div>
                    <span>{(selectedModelData.performance.recall * 100).toFixed(1)}%</span>
                  </div>
                </div>

                <div className="detection-classes">
                  <h5>Detection Classes</h5>
                  <div className="classes-grid">
                    {selectedModelData.classes.map((className, index) => (
                      <span key={index} className="class-tag">
                        {className}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="confidence-section">
            <h3>⚙️ Detection Settings</h3>
            <div className="confidence-slider">
              <label>Confidence Threshold: {(confidence * 100).toFixed(0)}%</label>
              <input
                type="range"
                min="0.1"
                max="1"
                step="0.05"
                value={confidence}
                onChange={(e) => setConfidence(parseFloat(e.target.value))}
                className="slider"
              />
              <div className="slider-labels">
                <span>10%</span>
                <span>100%</span>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {/* Upload Section */}
          <section className="upload-section">
            <h2>📤 Image Upload</h2>
            {!selectedImage ? (
              <div
                className="upload-area"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById('image-upload')?.click()}
              >
                <div className="upload-icon">📷</div>
                <h3>Drop an image here or click to browse</h3>
                <p>Supports JPG, PNG, and other image formats</p>
                <input
                  id="image-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  style={{ display: 'none' }}
                />
              </div>
            ) : (
              <div className="image-preview-container">
                <div className="image-actions">
                  <span className="image-name">{selectedImage.name}</span>
                  <button onClick={clearImage} className="clear-btn">
                    ❌ Clear
                  </button>
                </div>
                <div className="image-preview">
                  {imagePreview && (
                    <img 
                      src={imagePreview} 
                      alt="Preview" 
                      className="preview-image"
                    />
                  )}
                </div>
              </div>
            )}
          </section>

          {/* Action Section */}
          {selectedImage && (
            <section className="action-section">
              <button 
                onClick={runPrediction}
                disabled={predicting || !selectedModel}
                className={`run-detection-btn ${predicting ? 'processing' : ''}`}
              >
                {predicting ? (
                  <>
                    <div className="spinner"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    🎯 Run AI Detection
                  </>
                )}
              </button>
            </section>
          )}

          {/* Error Section */}
          {error && (
            <section className="error-section">
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                <div>
                  <strong>Error:</strong> {error}
                </div>
              </div>
            </section>
          )}

          {/* Results Section */}
          {results && (
            <section className="results-section">
              <h2>✅ Detection Results</h2>
              <div className="results-header">
                <div className="result-stat">
                  <span className="stat-label">Model</span>
                  <span className="stat-value">{results.model_name}</span>
                </div>
                <div className="result-stat">
                  <span className="stat-label">Detections</span>
                  <span className="stat-value">{results.detection_count}</span>
                </div>
                <div className="result-stat">
                  <span className="stat-label">Confidence</span>
                  <span className="stat-value">{(results.confidence_threshold * 100).toFixed(0)}%</span>
                </div>
                <div className="result-stat">
                  <span className="stat-label">Image Size</span>
                  <span className="stat-value">{results.image_size[0]}×{results.image_size[1]}</span>
                </div>
              </div>

              {results.detections.length > 0 && (
                <div className="detections-list">
                  <h3>Detected Objects</h3>
                  {results.detections.map((detection, index) => (
                    <div key={index} className="detection-item">
                      <div className="detection-info">
                        <span className="detection-class">{detection.class_name}</span>
                        <span className="detection-confidence">
                          {(detection.confidence * 100).toFixed(1)}% confidence
                        </span>
                      </div>
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill" 
                          style={{ width: `${detection.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {results.detections.length === 0 && (
                <div className="no-detections">
                  <span className="no-detection-icon">🔍</span>
                  <p>No objects detected above the confidence threshold.</p>
                  <p>Try lowering the confidence threshold or using a different image.</p>
                </div>
              )}
            </section>
          )}
        </main>
      </div>
    </div>
  );
};

export default ProperDemo;