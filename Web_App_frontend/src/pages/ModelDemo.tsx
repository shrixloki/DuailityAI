import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import ModelSelector from '@/components/ModelSelector';
import ImageUpload from '@/components/ImageUpload';
import { Brain, Target, Zap, Shield, Info, ArrowLeft, Home } from 'lucide-react';

const ModelDemo: React.FC = () => {
  const navigate = useNavigate();
  const [selectedModel, setSelectedModel] = useState('flagship');
  const apiUrl = 'http://localhost:8000'; // Backend API URL

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
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center space-x-3">
          <Brain className="h-10 w-10 text-blue-600" />
          <span>VISTA-S AI Detection</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Advanced AI-powered safety equipment detection system for space station environments.
          Choose from our flagship models optimized for different performance characteristics.
        </p>
      </div>

      {/* Model Information Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="border-blue-200 bg-blue-50">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-blue-800">
              <Shield className="h-5 w-5" />
              <span>Production Model</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-blue-700 mb-2">
              Stable, tested, and fully compliant with all Duality AI gates
            </p>
            <div className="flex space-x-2">
              <Badge variant="default" className="bg-blue-600">73.21% mAP50</Badge>
              <Badge variant="outline" className="border-blue-300">Production Ready</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="border-green-200 bg-green-50">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-green-800">
              <Target className="h-5 w-5" />
              <span>Ultra Accuracy</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-green-700 mb-2">
              Optimized for maximum accuracy with 90%+ mAP50 performance
            </p>
            <div className="flex space-x-2">
              <Badge variant="default" className="bg-green-600">90%+ mAP50</Badge>
              <Badge variant="outline" className="border-green-300">Training</Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-200 bg-purple-50">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-purple-800">
              <Zap className="h-5 w-5" />
              <span>Ultra Recall</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-purple-700 mb-2">
              Maximum detection sensitivity with 90% recall for critical safety
            </p>
            <div className="flex space-x-2">
              <Badge variant="default" className="bg-purple-600">90% Recall</Badge>
              <Badge variant="outline" className="border-purple-300">Training</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Interface */}
      <Tabs defaultValue="detection" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="detection" className="flex items-center space-x-2">
            <Zap className="h-4 w-4" />
            <span>AI Detection</span>
          </TabsTrigger>
          <TabsTrigger value="models" className="flex items-center space-x-2">
            <Brain className="h-4 w-4" />
            <span>Model Selection</span>
          </TabsTrigger>
          <TabsTrigger value="info" className="flex items-center space-x-2">
            <Info className="h-4 w-4" />
            <span>Information</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="detection" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Model Selector - Sidebar */}
            <div className="lg:col-span-1">
              <ModelSelector
                selectedModel={selectedModel}
                onModelChange={setSelectedModel}
                apiUrl={apiUrl}
              />
            </div>
            
            {/* Image Upload - Main Area */}
            <div className="lg:col-span-2">
              <ImageUpload
                selectedModel={selectedModel}
                apiUrl={apiUrl}
              />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="models" className="space-y-6">
          <ModelSelector
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
            apiUrl={apiUrl}
          />
        </TabsContent>

        <TabsContent value="info" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Safety Equipment Classes</CardTitle>
                <CardDescription>
                  Our AI models can detect these 7 types of safety equipment
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[
                    'OxygenTank', 'NitrogenTank', 'FirstAidBox', 'FireAlarm',
                    'SafetySwitchPanel', 'EmergencyPhone', 'FireExtinguisher'
                  ].map((className, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                      <span className="text-sm">{className}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Model Performance</CardTitle>
                <CardDescription>
                  Understanding the metrics
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <strong className="text-sm">mAP50:</strong>
                  <p className="text-sm text-gray-600">
                    Mean Average Precision at 50% IoU threshold. Higher is better.
                  </p>
                </div>
                <div>
                  <strong className="text-sm">Precision:</strong>
                  <p className="text-sm text-gray-600">
                    Percentage of correct detections out of all detections made.
                  </p>
                </div>
                <div>
                  <strong className="text-sm">Recall:</strong>
                  <p className="text-sm text-gray-600">
                    Percentage of actual objects that were successfully detected.
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>About VISTA-S</CardTitle>
                <CardDescription>
                  Visual Inference System for Target Assessment
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 leading-relaxed">
                  VISTA-S is an advanced AI-powered detection system designed specifically for 
                  space station environments. Our models are trained on synthetic datasets 
                  representing various safety equipment configurations and scenarios. The system 
                  provides real-time detection capabilities with high accuracy and reliability, 
                  making it suitable for critical safety applications in space environments.
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  <Badge variant="outline">YOLOv8 Architecture</Badge>
                  <Badge variant="outline">7 Safety Classes</Badge>
                  <Badge variant="outline">Real-time Detection</Badge>
                  <Badge variant="outline">Space-Optimized</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
      </div>
    </div>
  );
};

export default ModelDemo;