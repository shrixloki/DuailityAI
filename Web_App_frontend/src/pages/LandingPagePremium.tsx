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
  Bot,
  Activity,
  Scan
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
    features: ["Fire Extinguisher", "Oxygen Tank", "First Aid Box"],
    color: "from-blue-500 to-cyan-500"
  },
  {
    name: "Perfect 90%+ Model", 
    description: "Ultra-high accuracy model with 90%+ mAP50 for critical applications",
    classes: 7,
    accuracy: "90%+",
    status: "Premium",
    features: ["Oxygen Tank", "Nitrogen Tank", "First Aid Box", "Fire Alarm", "Safety Switch Panel", "Emergency Phone", "Fire Extinguisher"],
    color: "from-purple-500 to-pink-500"
  },
  {
    name: "Backup Model",
    description: "Reliable fallback model ensuring continuous operation",
    classes: 3,
    accuracy: "70%+",
    status: "Stable",
    features: ["Core Safety Equipment", "Emergency Devices", "Basic Detection"],
    color: "from-green-500 to-emerald-500"
  }
];

const stats = [
  { label: "Detection Accuracy", value: "90%+", icon: Target },
  { label: "Processing Speed", value: "<100ms", icon: Zap },
  { label: "Equipment Classes", value: "7+", icon: Layers },
  { label: "Model Variants", value: "3", icon: Bot }
];

const LandingPagePremium = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-screen bg-gradient-to-br from-[#000] to-[#1A2428] text-white relative overflow-hidden">
      {/* Advanced Animated Background */}
      <div className="absolute inset-0">
        {/* Flowing Geometric Shapes - CSS Only */}
        <div className="absolute inset-0">
          {/* Large flowing shapes */}
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-lg opacity-10"
              style={{
                width: `${60 + Math.random() * 40}px`,
                height: `${20 + Math.random() * 10}px`,
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                background: `linear-gradient(45deg, rgba(59, 130, 246, 0.3), rgba(147, 51, 234, 0.3))`,
                transform: `rotate(${Math.random() * 360}deg)`,
                animation: `float ${3 + Math.random() * 2}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`
              }}
            />
          ))}
          
          {/* Medium flowing shapes */}
          {[...Array(20)].map((_, i) => (
            <div
              key={`med-${i}`}
              className="absolute rounded opacity-8"
              style={{
                width: `${30 + Math.random() * 20}px`,
                height: `${10 + Math.random() * 5}px`,
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                background: `linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(59, 130, 246, 0.2))`,
                transform: `rotate(${Math.random() * 360}deg)`,
                animation: `float ${2 + Math.random() * 3}s ease-in-out infinite reverse`,
                animationDelay: `${Math.random() * 3}s`
              }}
            />
          ))}
          
          {/* Small flowing shapes */}
          {[...Array(30)].map((_, i) => (
            <div
              key={`small-${i}`}
              className="absolute rounded-full opacity-6"
              style={{
                width: `${10 + Math.random() * 15}px`,
                height: `${10 + Math.random() * 15}px`,
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                background: `radial-gradient(circle, rgba(147, 51, 234, 0.3), rgba(59, 130, 246, 0.1))`,
                animation: `pulse ${1.5 + Math.random() * 2}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`
              }}
            />
          ))}
        </div>
        
        {/* Gradient Orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 rounded-full blur-3xl animate-pulse delay-2000"></div>
        
        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-5" style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px'
        }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Hero Section */}
        <div className="w-full max-w-7xl mx-auto space-y-16 px-8 py-16">
          <div className="flex flex-col items-center text-center space-y-8">
            <Badge variant="secondary" className="backdrop-blur-sm bg-white/10 border border-white/20 text-white hover:bg-white/20 px-6 py-3 rounded-full text-sm animate-pulse">
              <Sparkles className="w-4 h-4 mr-2" />
              Next Generation AI Safety Detection
            </Badge>
            
            <div className="space-y-6 flex items-center justify-center flex-col">
              <div className="relative">
                <h1 className="text-4xl md:text-7xl font-bold tracking-tight max-w-5xl bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent">
                  DUALITY AI
                </h1>
                <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-xl rounded-full animate-pulse"></div>
              </div>
              
              <p className="text-xl md:text-2xl text-neutral-300 max-w-3xl font-light">
                Advanced Computer Vision for Safety Equipment Detection
              </p>
              <p className="text-lg text-neutral-400 max-w-2xl">
                Powered by state-of-the-art YOLO models with 90%+ accuracy. Detect fire extinguishers, oxygen tanks, emergency equipment, and more in real-time.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 items-center pt-4">
                <Button 
                  onClick={() => navigate('/demo')}
                  className="text-sm px-8 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 font-medium"
                >
                  <Scan className="w-4 h-4 mr-2" />
                  Try Live Demo
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
                <Button 
                  onClick={() => navigate('/models')}
                  className="text-sm px-8 py-3 rounded-xl bg-transparent text-white border border-white/20 shadow-none hover:bg-white/10 hover:scale-105 transition-all duration-300"
                >
                  Explore Models
                </Button>
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center space-y-3 group">
                <div className="mx-auto w-12 h-12 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <stat.icon className="w-6 h-6 text-white/80" />
                </div>
                <div className="text-2xl md:text-3xl font-bold text-white">{stat.value}</div>
                <div className="text-sm text-neutral-400">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Features Grid */}
          <div className="space-y-8">
            <div className="text-center space-y-4">
              <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                Powerful Features
              </h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                Built for safety professionals who demand accuracy, speed, and reliability
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
              {features.map((feature, idx) => (
                <Card key={idx} className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 hover:scale-105 transition-all duration-300 group">
                  <CardHeader className="space-y-3">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <feature.icon size={24} className="text-white/80" />
                    </div>
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
              <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                AI Models
              </h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                Choose the perfect model for your safety detection needs
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
              {models.map((model, idx) => (
                <Card key={idx} className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 hover:scale-105 transition-all duration-300 relative overflow-hidden group">
                  {model.status === "Premium" && (
                    <div className="absolute top-4 right-4">
                      <Badge className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black text-xs animate-pulse">
                        Premium
                      </Badge>
                    </div>
                  )}
                  
                  {/* Gradient Border Effect */}
                  <div className={`absolute inset-0 bg-gradient-to-r ${model.color} opacity-0 group-hover:opacity-20 transition-opacity duration-300 rounded-xl`}></div>
                  
                  <CardHeader className="space-y-3 relative z-10">
                    <div className="flex items-center gap-2">
                      <div className={`w-8 h-8 bg-gradient-to-r ${model.color} rounded-lg flex items-center justify-center`}>
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                      <CardTitle className="text-lg font-semibold text-white">{model.name}</CardTitle>
                    </div>
                    <CardDescription className="text-neutral-400 text-sm">
                      {model.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4 relative z-10">
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
            <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Ready to Get Started?
            </h2>
            <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
              Experience the power of AI-driven safety equipment detection. Upload an image and see our models in action.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
              <Button 
                onClick={() => navigate('/demo')}
                className="text-base px-10 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 font-medium"
              >
                <Activity className="w-5 h-5 mr-2" />
                Start Detection Demo
                <Zap className="w-5 h-5 ml-2" />
              </Button>
              <Button 
                onClick={() => navigate('/api-docs')}
                className="text-base px-10 py-4 rounded-xl bg-transparent text-white border border-white/20 shadow-none hover:bg-white/10 hover:scale-105 transition-all duration-300"
              >
                View API Documentation
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPagePremium;