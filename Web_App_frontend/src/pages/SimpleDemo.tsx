import React, { useState } from 'react';

const SimpleDemo: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
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
  };

  const runPrediction = async () => {
    console.log('🚀 Button clicked - starting prediction');
    
    if (!selectedImage) {
      console.log('❌ No image selected');
      alert('Please select an image first!');
      return;
    }

    setPredicting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('model', 'flagship');
      formData.append('confidence', '0.5');

      console.log('📡 Sending request to: http://localhost:8000/api/predict');
      
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        body: formData,
      });

      console.log('📨 Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📨 Response data:', data);

      if (data.success) {
        setResults(data);
        console.log('✅ Prediction successful!');
      } else {
        setError(data.error || 'Prediction failed');
        console.log('❌ Prediction failed:', data.error);
      }
    } catch (err: any) {
      const errorMsg = `Error: ${err.message}`;
      setError(errorMsg);
      console.error('❌ Prediction error:', err);
    } finally {
      setPredicting(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🚀 DUALITY AI - Simple Demo</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <h2>Step 1: Upload Image</h2>
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleImageSelect}
          style={{ marginBottom: '10px' }}
        />
        
        {imagePreview && (
          <div>
            <img 
              src={imagePreview} 
              alt="Preview" 
              style={{ maxWidth: '300px', maxHeight: '300px', display: 'block', margin: '10px 0' }}
            />
          </div>
        )}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h2>Step 2: Run Detection</h2>
        <button 
          onClick={runPrediction}
          disabled={predicting || !selectedImage}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: predicting ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: predicting ? 'not-allowed' : 'pointer'
          }}
        >
          {predicting ? '🔄 Processing...' : '🎯 Run AI Detection'}
        </button>
      </div>

      {error && (
        <div style={{ 
          backgroundColor: '#ffebee', 
          color: '#c62828', 
          padding: '10px', 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {results && (
        <div style={{ 
          backgroundColor: '#e8f5e8', 
          padding: '15px', 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          <h2>✅ Detection Results</h2>
          <p><strong>Model:</strong> {results.model_name}</p>
          <p><strong>Detections Found:</strong> {results.detection_count}</p>
          <p><strong>Confidence Threshold:</strong> {(results.confidence_threshold * 100).toFixed(0)}%</p>
          
          {results.detections && results.detections.length > 0 && (
            <div>
              <h3>Detected Objects:</h3>
              <ul>
                {results.detections.map((detection: any, index: number) => (
                  <li key={index}>
                    <strong>{detection.class_name}</strong> - {(detection.confidence * 100).toFixed(1)}% confidence
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          <details style={{ marginTop: '10px' }}>
            <summary>Raw API Response</summary>
            <pre style={{ backgroundColor: '#f5f5f5', padding: '10px', overflow: 'auto' }}>
              {JSON.stringify(results, null, 2)}
            </pre>
          </details>
        </div>
      )}

      <div style={{ 
        backgroundColor: '#f0f0f0', 
        padding: '15px', 
        borderRadius: '5px',
        marginTop: '20px'
      }}>
        <h3>🔧 Debug Info</h3>
        <p><strong>API URL:</strong> http://localhost:8000</p>
        <p><strong>Image Selected:</strong> {selectedImage ? selectedImage.name : 'None'}</p>
        <p><strong>Currently Processing:</strong> {predicting ? 'Yes' : 'No'}</p>
        <p><strong>Instructions:</strong> Open browser console (F12) to see detailed logs</p>
      </div>
    </div>
  );
};

export default SimpleDemo;