import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle, Clock, Zap, Target, Shield } from 'lucide-react';

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

interface ModelSelectorProps {
  selectedModel: string;
  onModelChange: (modelId: string) => void;
  apiUrl: string;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ 
  selectedModel, 
  onModelChange, 
  apiUrl 
}) => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${apiUrl}/api/models`);
      const data = await response.json();
      
      if (data.success) {
        setModels(data.models);
      } else {
        setError('Failed to fetch models');
      }
    } catch (err) {
      setError('Error connecting to model API');
      console.error('Model fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string, available: boolean) => {
    if (!available) return <AlertCircle className="h-4 w-4 text-red-500" />;
    
    switch (status) {
      case 'production':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'training':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case 'experimental':
        return <Zap className="h-4 w-4 text-blue-500" />;
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusBadge = (status: string, available: boolean) => {
    if (!available) {
      return <Badge variant="destructive">Unavailable</Badge>;
    }
    
    switch (status) {
      case 'production':
        return <Badge variant="default" className="bg-green-500">Production</Badge>;
      case 'training':
        return <Badge variant="secondary">Training</Badge>;
      case 'experimental':
        return <Badge variant="outline">Experimental</Badge>;
      default:
        return <Badge variant="secondary">Unknown</Badge>;
    }
  };

  const getModelIcon = (modelId: string) => {
    switch (modelId) {
      case 'flagship':
        return <Shield className="h-5 w-5 text-blue-600" />;
      case 'ultra_accuracy':
        return <Target className="h-5 w-5 text-green-600" />;
      case 'ultra_recall':
        return <Zap className="h-5 w-5 text-purple-600" />;
      default:
        return <CheckCircle className="h-5 w-5 text-gray-600" />;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Loading Models...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span>Fetching available models...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-red-600">Error Loading Models</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-500">{error}</p>
          <button 
            onClick={fetchModels}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </CardContent>
      </Card>
    );
  }

  const selectedModelData = models.find(m => m.id === selectedModel);

  return (
    <div className="space-y-4">
      {/* Model Selector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Target className="h-5 w-5" />
            <span>Select AI Model</span>
          </CardTitle>
          <CardDescription>
            Choose from our flagship models optimized for different use cases
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Select value={selectedModel} onValueChange={onModelChange}>
            <SelectTrigger>
              <SelectValue placeholder="Select a model" />
            </SelectTrigger>
            <SelectContent>
              {models.map((model) => (
                <SelectItem 
                  key={model.id} 
                  value={model.id}
                  disabled={!model.available}
                >
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(model.status, model.available)}
                    <span>{model.name}</span>
                    {getStatusBadge(model.status, model.available)}
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {/* Selected Model Details */}
      {selectedModelData && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              {getModelIcon(selectedModelData.id)}
              <span>{selectedModelData.name}</span>
              {getStatusBadge(selectedModelData.status, selectedModelData.available)}
            </CardTitle>
            <CardDescription>
              {selectedModelData.description}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Performance Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm font-medium">mAP50</span>
                  <span className="text-sm text-gray-600">
                    {(selectedModelData.performance.mAP50 * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress 
                  value={selectedModelData.performance.mAP50 * 100} 
                  className="h-2"
                />
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Precision</span>
                  <span className="text-sm text-gray-600">
                    {(selectedModelData.performance.precision * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress 
                  value={selectedModelData.performance.precision * 100} 
                  className="h-2"
                />
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Recall</span>
                  <span className="text-sm text-gray-600">
                    {(selectedModelData.performance.recall * 100).toFixed(1)}%
                  </span>
                </div>
                <Progress 
                  value={selectedModelData.performance.recall * 100} 
                  className="h-2"
                />
              </div>
            </div>

            {/* Detection Classes */}
            <div>
              <h4 className="text-sm font-medium mb-2">Detection Classes</h4>
              <div className="flex flex-wrap gap-2">
                {selectedModelData.classes.map((className, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    {className}
                  </Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ModelSelector;