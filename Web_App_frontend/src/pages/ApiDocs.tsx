import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Code, Zap, Shield, Globe } from 'lucide-react';

const ApiDocs: React.FC = () => {
  const navigate = useNavigate();

  const endpoints = [
    {
      method: 'GET',
      path: '/api/models',
      description: 'Get list of available AI models',
      response: 'Returns model information, performance metrics, and availability status'
    },
    {
      method: 'POST',
      path: '/api/predict',
      description: 'Perform object detection on uploaded image',
      response: 'Returns detection results with bounding boxes, confidence scores, and class labels'
    },
    {
      method: 'GET',
      path: '/api/health',
      description: 'Check API health and model status',
      response: 'Returns system status and loaded model information'
    },
    {
      method: 'POST',
      path: '/api/predict/{model_id}',
      description: 'Use specific model for prediction',
      response: 'Returns detection results using the specified model'
    }
  ];

  const models = [
    {
      id: 'flagship',
      name: 'Flagship Model',
      accuracy: '73.21%',
      classes: 3,
      description: 'Main production model optimized for reliability'
    },
    {
      id: 'perfect_90plus',
      name: 'Perfect 90%+ Model',
      accuracy: '90%+',
      classes: 7,
      description: 'Ultra-high accuracy model for critical applications'
    },
    {
      id: 'backup_model',
      name: 'Backup Model',
      accuracy: '70%+',
      classes: 3,
      description: 'Reliable fallback model for continuous operation'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button 
              onClick={() => navigate('/')}
              variant="ghost" 
              size="sm"
              className="text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
            <Button 
              onClick={() => navigate('/demo')}
              variant="outline" 
              size="sm"
            >
              Try Live Demo
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center space-x-3">
            <Code className="h-10 w-10 text-blue-600" />
            <span>API Documentation</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Integrate Duality AI's powerful object detection capabilities into your applications with our RESTful API.
          </p>
        </div>

        {/* Quick Start */}
        <Card className="mb-8 border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-blue-800">
              <Zap className="h-5 w-5" />
              <span>Quick Start</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-blue-800 mb-2">Base URL</h4>
                <code className="bg-white px-3 py-1 rounded border text-sm">http://localhost:8000</code>
              </div>
              <div>
                <h4 className="font-semibold text-blue-800 mb-2">Example Request</h4>
                <pre className="bg-white p-4 rounded border text-sm overflow-x-auto">
{`curl -X POST http://localhost:8000/api/predict \\
  -F "image=@your-image.jpg" \\
  -F "model_id=flagship" \\
  -F "confidence=0.5"`}
                </pre>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* API Endpoints */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">API Endpoints</h2>
          <div className="space-y-4">
            {endpoints.map((endpoint, idx) => (
              <Card key={idx} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg flex items-center space-x-3">
                      <Badge 
                        variant={endpoint.method === 'GET' ? 'default' : 'secondary'}
                        className={endpoint.method === 'GET' ? 'bg-green-600' : 'bg-blue-600'}
                      >
                        {endpoint.method}
                      </Badge>
                      <code className="text-sm font-mono">{endpoint.path}</code>
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600 mb-2">
                    {endpoint.description}
                  </CardDescription>
                  <p className="text-sm text-gray-500">
                    <strong>Response:</strong> {endpoint.response}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Available Models */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Models</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {models.map((model, idx) => (
              <Card key={idx} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle className="text-lg">{model.name}</CardTitle>
                  <div className="flex space-x-2">
                    <Badge variant="outline">{model.accuracy} mAP50</Badge>
                    <Badge variant="secondary">{model.classes} classes</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600">
                    {model.description}
                  </CardDescription>
                  <div className="mt-3">
                    <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                      model_id: "{model.id}"
                    </code>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Response Format */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Globe className="h-5 w-5" />
              <span>Response Format</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
{`{
  "success": true,
  "model_used": "flagship",
  "model_name": "FINAL_SELECTED_MODEL",
  "image_size": [640, 480],
  "detections": [
    {
      "bbox": [100, 150, 200, 250],
      "confidence": 0.85,
      "class_id": 0,
      "class_name": "fire_extinguisher"
    }
  ],
  "detection_count": 1,
  "confidence_threshold": 0.5,
  "timestamp": "2025-12-28T00:00:00Z"
}`}
            </pre>
          </CardContent>
        </Card>

        {/* Security & Rate Limits */}
        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-yellow-800">
              <Shield className="h-5 w-5" />
              <span>Security & Limits</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-yellow-700">
              <li>• Maximum image size: 10MB</li>
              <li>• Supported formats: JPG, PNG, WEBP</li>
              <li>• Rate limit: 100 requests per minute</li>
              <li>• CORS enabled for web applications</li>
              <li>• No authentication required for development</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ApiDocs;