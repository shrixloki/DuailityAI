import { Scene } from "@/components/ui/hero-section";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  Cpu, 
  ShieldCheck, 
  Layers, 
  Zap, 
  Eye, 
  Brain, 
  Target, 
  Gauge,
  CheckCircle,
  ArrowRight,
  Sparkles,
  Bot
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const features = [
  {
    icon: Eye,
    title: "Computer Vision",
    description: "Advanced object detection with 90%+ accuracy across multiple safety equipment categories.",
  },
  {
    icon: Brain,
    title: "AI-Powered",
    description: "State-of-the-art YOLO models trained on comprehensive safety equipment datasets.",
  },
  {
    icon: Target,
    title: "Precision Detection",
    description: "Identify fire extinguishers, oxygen tanks, safety panels, and emergency equipment.",
  },
  {
    icon: Zap,
    title: "Real-Time Processing",
    description: "Lightning-fast inference with optimized model architecture for instant results.",
  },
  {
    icon: ShieldCheck,
    title: "Safety Compliance",
    description: "Ensure workplace safety standards with automated equipment verification.",
  },
  {
    icon: Layers,
    title: "Multi-Model Support",
    description: "Choose from flagship, backup, or specialized models based on your needs.",
  },
];

const models = [
  {
    name: "Flagship Model",
    description: "Main production model with 73.21% mAP50 and 65.98% recall",
    classes: 3,
    accuracy: "73.21%",
    status: "Production Ready",
    features: ["Fire Extinguisher", "Oxygen Tank", "First Aid Box"]
  },
  {
    name: "Perfect 90%+ Model", 
    description: "Ultra-high accuracy model with 90%+ mAP50 for critical applications",
    classes: 7,
    accuracy: "90%+",
    status: "Premium",
    features: ["Oxygen Tank", "Nitrogen Tank", "First Aid Box", "Fire Alarm", "Safety Switch Panel", "Emergency Phone", "Fire Extinguisher"]
  },
  {
    name: "Backup Model",
    description: "Reliable fallback model ensuring continuous operation",
    classes: 3,
    accuracy: "70%+",
    status: "Stable",
    features: ["Core Safety Equipment", "Emergency Devices", "Basic Detection"]
  }
];

const stats = [
  { label: "Detection Accuracy", value: "90%+" },
  { label: "Processing Speed", value: "<100ms" },
  { label: "Equipment Classes", value: "7+" },
  { label: "Model Variants", value: "3" }
];

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-screen bg-gradient-to-br from-[#000] to-[#1A2428] text-white flex flex-col items-center justify-center relative overflow-hidden">
      {/* Hero Section */}
      <div className="w-full max-w-7xl space-y-16 relative z-10 px-8 py-16">
        <div className="flex flex-col items-center text-center space-y-8">
          <Badge variant="secondary" className="backdrop-blur-sm bg-white/10 border border-white/20 text-white hover:bg-white/20 px-6 py-3 rounded-full text-sm">
            <Sparkles className="w-4 h-4 mr-2" />
            Next Generation AI Safety Detection
          </Badge>
          
          <div className="space-y-6 flex items-center justify-center flex-col">
            <h1 className="text-4xl md:text-7xl font-bold tracking-tight max-w-5xl bg-gradient-to-r from-white via-white to-gray-300 bg-clip-text text-transparent">
              DUALITY AI
            </h1>
            <p className="text-xl md:text-2xl text-neutral-300 max-w-3xl font-light">
              Advanced Computer Vision for Safety Equipment Detection
            </p>
            <p className="text-lg text-neutral-400 max-w-2xl">
              Powered by state-of-the-art YOLO models with 90%+ accuracy. Detect fire extinguishers, oxygen tanks, emergency equipment, and more in real-time.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 items-center pt-4">
              <Button 
                onClick={() => navigate('/demo')}
                className="text-sm px-8 py-3 rounded-xl bg-white text-black border border-white/10 shadow-none hover:bg-white/90 transition-all duration-300 font-medium"
              >
                Try Live Demo
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
              <Button 
                onClick={() => navigate('/models')}
                className="text-sm px-8 py-3 rounded-xl bg-transparent text-white border border-white/20 shadow-none hover:bg-white/10 transition-all duration-300"
              >
                Explore Models
              </Button>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
          {stats.map((stat, idx) => (
            <div key={idx} className="text-center space-y-2">
              <div className="text-2xl md:text-3xl font-bold text-white">{stat.value}</div>
              <div className="text-sm text-neutral-400">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold">Powerful Features</h2>
            <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
              Built for safety professionals who demand accuracy, speed, and reliability
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {features.map((feature, idx) => (
              <Card key={idx} className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300">
                <CardHeader className="space-y-3">
                  <feature.icon size={24} className="text-white/80" />
                  <CardTitle className="text-lg font-semibold text-white">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-neutral-400 text-sm leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Models Section */}
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold">AI Models</h2>
            <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
              Choose the perfect model for your safety detection needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {models.map((model, idx) => (
              <Card key={idx} className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all duration-300 relative overflow-hidden">
                {model.status === "Premium" && (
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black text-xs">
                      Premium
                    </Badge>
                  </div>
                )}
                <CardHeader className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Bot className="w-5 h-5 text-white/80" />
                    <CardTitle className="text-lg font-semibold text-white">{model.name}</CardTitle>
                  </div>
                  <CardDescription className="text-neutral-400 text-sm">
                    {model.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-400">Accuracy</span>
                    <span className="text-lg font-bold text-green-400">{model.accuracy}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-400">Classes</span>
                    <span className="text-sm font-medium text-white">{model.classes} equipment types</span>
                  </div>
                  <div className="space-y-2">
                    <span className="text-sm text-neutral-400">Detection Capabilities:</span>
                    <div className="flex flex-wrap gap-1">
                      {model.features.slice(0, 3).map((feature, featureIdx) => (
                        <Badge key={featureIdx} variant="outline" className="text-xs border-white/20 text-white/80">
                          {feature}
                        </Badge>
                      ))}
                      {model.features.length > 3 && (
                        <Badge variant="outline" className="text-xs border-white/20 text-white/80">
                          +{model.features.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center space-y-6 py-16">
          <h2 className="text-3xl md:text-4xl font-bold">Ready to Get Started?</h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Experience the power of AI-driven safety equipment detection. Upload an image and see our models in action.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
            <Button 
              onClick={() => navigate('/demo')}
              className="text-base px-10 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 font-medium"
            >
              Start Detection Demo
              <Zap className="w-5 h-5 ml-2" />
            </Button>
            <Button 
              onClick={() => navigate('/api-docs')}
              className="text-base px-10 py-4 rounded-xl bg-transparent text-white border border-white/20 shadow-none hover:bg-white/10 transition-all duration-300"
            >
              View API Documentation
            </Button>
          </div>
        </div>
      </div>

      {/* Background 3D Scene */}
      <div className='absolute inset-0 opacity-30'>
        <Scene />
      </div>
    </div>
  );
};

export default LandingPage;