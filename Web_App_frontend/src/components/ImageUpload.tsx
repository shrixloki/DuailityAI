import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Slider } from '@/components/ui/slider';
import { Upload, X, Image as ImageIcon, Zap } from 'lucide-react';

interface Detection {
  bbox: [number, number, number, number];
  confidence: number;
  class_id: number;
  class_name: string;
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

interface ImageUploadProps {
  selectedModel: string;
  apiUrl: string;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ selectedModel, apiUrl }) => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [results, setResults] = useState<PredictionResult | null>(null);
  const [confidence, setConfidence] = useState([0.5]);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setResults(null);
      setError(null);
      
      // Create preview
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

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
  };

  const runPrediction = async () => {
    console.log('🚀 runPrediction called');
    console.log('selectedImage:', selectedImage);
    console.log('selectedModel:', selectedModel);
    console.log('apiUrl:', apiUrl);
    
    if (!selectedImage) {
      console.log('❌ No image selected');
      return;
    }

    setPredicting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('model', selectedModel);
      formData.append('confidence', confidence[0].toString());

      console.log('📡 Sending request to:', `${apiUrl}/api/predict`);
      console.log('📦 FormData contents:', {
        image: selectedImage.name,
        model: selectedModel,
        confidence: confidence[0].toString()
      });

      const response = await fetch(`${apiUrl}/api/predict`, {
        method: 'POST',
        body: formData,
      });

      console.log('📨 Response status:', response.status);
      const data = await response.json();
      console.log('📨 Response data:', data);

      if (data.success) {
        setResults(data);
        console.log('✅ Prediction successful');
      } else {
        setError(data.error || 'Prediction failed');
        console.log('❌ Prediction failed:', data.error);
      }
    } catch (err) {
      const errorMsg = 'Error connecting to prediction API';
      setError(errorMsg);
      console.error('❌ Prediction error:', err);
    } finally {
      setPredicting(false);
    }
  };

  const drawDetections = () => {
    if (!results || !imagePreview) return null;

    const [imgWidth, imgHeight] = results.image_size;
    
    return (
      <div className="relative inline-block">
        <img 
          src={imagePreview} 
          alt="Prediction result"
          className="max-w-full h-auto rounded-lg"
          style={{ maxHeight: '500px' }}
        />
        
        {/* Detection overlays */}
        <svg 
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          viewBox={`0 0 ${imgWidth} ${imgHeight}`}
          preserveAspectRatio="xMidYMid meet"
        >
          {results.detections.map((detection, index) => {
            const [x1, y1, x2, y2] = detection.bbox;
            const width = x2 - x1;
            const height = y2 - y1;
            
            // Color based on class
            const colors = [
              '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
              '#FFEAA7', '#DDA0DD', '#98D8C8'
            ];
            const color = colors[detection.class_id % colors.length];
            
            return (
              <g key={index}>
                {/* Bounding box */}
                <rect
                  x={x1}
                  y={y1}
                  width={width}
                  height={height}
                  fill="none"
                  stroke={color}
                  strokeWidth="3"
                  opacity="0.8"
                />
                
                {/* Label background */}
                <rect
                  x={x1}
                  y={y1 - 25}
                  width={detection.class_name.length * 8 + 20}
                  height="25"
                  fill={color}
                  opacity="0.8"
                />
                
                {/* Label text */}
                <text
                  x={x1 + 5}
                  y={y1 - 8}
                  fill="white"
                  fontSize="14"
                  fontWeight="bold"
                >
                  {detection.class_name} ({(detection.confidence * 100).toFixed(1)}%)
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* Image Upload */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Upload className="h-5 w-5" />
            <span>Upload Image</span>
          </CardTitle>
          <CardDescription>
            Upload an image to detect safety equipment using AI
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!selectedImage ? (
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors cursor-pointer"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => document.getElementById('image-upload')?.click()}
            >
              <ImageIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-600 mb-2">
                Drop an image here or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supports JPG, PNG, and other image formats
              </p>
              <input
                id="image-upload"
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                className="hidden"
              />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Selected: {selectedImage.name}</span>
                <Button variant="outline" size="sm" onClick={clearImage}>
                  <X className="h-4 w-4 mr-1" />
                  Clear
                </Button>
              </div>
              
              {imagePreview && !results && (
                <img 
                  src={imagePreview} 
                  alt="Preview" 
                  className="max-w-full h-auto rounded-lg"
                  style={{ maxHeight: '300px' }}
                />
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Confidence Threshold */}
      {selectedImage && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Detection Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Confidence Threshold: {(confidence[0] * 100).toFixed(0)}%
                </label>
                <Slider
                  value={confidence}
                  onValueChange={setConfidence}
                  max={1}
                  min={0.1}
                  step={0.05}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Higher values show only high-confidence detections
                </p>
              </div>
              
              <Button 
                onClick={() => {
                  console.log('🔘 Button clicked!');
                  console.log('predicting:', predicting);
                  console.log('selectedModel:', selectedModel);
                  console.log('selectedImage:', selectedImage);
                  runPrediction();
                }}
                disabled={predicting || !selectedModel}
                className="w-full"
              >
                {predicting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Running Detection...
                  </>
                ) : (
                  <>
                    <Zap className="h-4 w-4 mr-2" />
                    Run AI Detection
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Card className="border-red-200">
          <CardContent className="pt-6">
            <div className="text-red-600">
              <strong>Error:</strong> {error}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {results && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Zap className="h-5 w-5 text-green-600" />
              <span>Detection Results</span>
            </CardTitle>
            <CardDescription>
              Found {results.detection_count} objects using {results.model_name}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Image with detections */}
            <div className="text-center">
              {drawDetections()}
            </div>
            
            {/* Detection summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="font-medium">Model:</span>
                <p className="text-gray-600">{results.model_name}</p>
              </div>
              <div>
                <span className="font-medium">Detections:</span>
                <p className="text-gray-600">{results.detection_count}</p>
              </div>
              <div>
                <span className="font-medium">Confidence:</span>
                <p className="text-gray-600">{(results.confidence_threshold * 100).toFixed(0)}%</p>
              </div>
              <div>
                <span className="font-medium">Image Size:</span>
                <p className="text-gray-600">{results.image_size[0]}×{results.image_size[1]}</p>
              </div>
            </div>
            
            {/* Detection details */}
            {results.detections.length > 0 && (
              <div>
                <h4 className="font-medium mb-2">Detected Objects:</h4>
                <div className="space-y-2">
                  {results.detections.map((detection, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="font-medium">{detection.class_name}</span>
                      <span className="text-sm text-gray-600">
                        {(detection.confidence * 100).toFixed(1)}% confidence
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ImageUpload;