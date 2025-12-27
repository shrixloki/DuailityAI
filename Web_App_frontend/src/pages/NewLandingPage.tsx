import { HeroSection } from "@/components/ui/hero-section-with-smooth-bg-shader";
import { Button } from "@/components/ui/button";
import { 
  Cpu, 
  ShieldCheck, 
  Layers, 
  Zap, 
  Eye, 
  Brain, 
  Target,
  ArrowRight,
  Bot
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const features = [
  {
    icon: Eye,
    title: "Computer Vision",
    description: "90%+ accuracy detection across comprehensive safety equipment categories using advanced deep learning models.",
  },
  {
    icon: Brain,
    title: "Production AI",
    description: "Rigorously tested YOLO models with continuous learning and optimization for enterprise deployments.",
  },
  {
    icon: Target,
    title: "Equipment Detection",
    description: "Identify fire extinguishers, oxygen tanks, emergency panels, first aid stations, and safety signage.",
  },
  {
    icon: Zap,
    title: "Real-Time Processing",
    description: "Sub-100ms inference with optimized architecture for high-throughput enterprise environments.",
  },
  {
    icon: ShieldCheck,
    title: "Compliance & Audit",
    description: "Automated safety monitoring with audit trails, regulatory reporting, and system integration.",
  },
  {
    icon: Layers,
    title: "Scalable Deployment",
    description: "Cloud-native with auto-scaling, load balancing, and multi-region support for enterprise needs.",
  },
];

const models = [
  {
    name: "Enterprise Model",
    description: "Production-ready model optimized for enterprise deployments with 73.21% mAP50 and proven reliability",
    classes: 3,
    accuracy: "73.21%",
    status: "Production Ready",
    features: ["Fire Extinguisher", "Oxygen Tank", "First Aid Box"]
  },
  {
    name: "Premium Accuracy Model", 
    description: "Ultra-high precision model with 90%+ mAP50 for mission-critical safety applications and compliance requirements",
    classes: 7,
    accuracy: "90%+",
    status: "Premium",
    features: ["Oxygen Tank", "Nitrogen Tank", "First Aid Box", "Fire Alarm", "Safety Switch Panel", "Emergency Phone", "Fire Extinguisher"]
  },
  {
    name: "Standard Model",
    description: "Reliable baseline model ensuring continuous operation with consistent 70%+ accuracy for standard deployments",
    classes: 3,
    accuracy: "70%+",
    status: "Standard",
    features: ["Core Safety Equipment", "Emergency Devices", "Basic Detection"]
  }
];

const stats = [
  { label: "Detection Accuracy", value: "90%+" },
  { label: "Response Time", value: "<100ms" },
  { label: "Equipment Types", value: "7+" },
  { label: "Enterprise Clients", value: "500+" }
];

const NewLandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-screen bg-background text-foreground">
      {/* Hero Section with Smooth Background */}
      <HeroSection
        title="Enterprise AI Safety Detection for"
        highlightText="Critical Infrastructure"
        description="Industry-leading computer vision technology with 90%+ accuracy for safety equipment detection. Trusted by Fortune 500 companies to ensure workplace safety compliance and emergency preparedness."
        buttonText="Request Demo"
        onButtonClick={() => navigate('/demo')}
        colors={["#f8fafc", "#f1f5f9", "#e2e8f0", "#cbd5e1", "#94a3b8", "#64748b"]}
        distortion={0.1}
        swirl={0.1}
        speed={0.2}
        offsetX={0.02}
        titleClassName="text-slate-900 font-medium"
        descriptionClassName="text-slate-600 font-normal"
        buttonClassName="bg-slate-900 text-white hover:bg-slate-800 border-slate-900 font-medium"
        fontFamily="Inter, system-ui, sans-serif"
        fontWeight={500}
        veilOpacity="bg-white/60"
      />

      {/* Content Sections */}
      <div className="relative z-10 bg-background">
        {/* Stats Section */}
        <section className="py-24 px-8 bg-white border-b border-gray-100">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-xl font-medium text-slate-900 mb-3">Performance Metrics</h2>
              <p className="text-slate-600 max-w-2xl mx-auto text-sm">
                Proven results across enterprise deployments
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-12 max-w-4xl mx-auto">
              {stats.map((stat, idx) => (
                <div key={idx} className="text-center space-y-2">
                  <div className="text-3xl font-light text-slate-900">{stat.value}</div>
                  <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="py-24 px-8 bg-gray-50">
          <div className="max-w-6xl mx-auto space-y-16">
            <div className="text-center space-y-4">
              <h2 className="text-2xl font-medium text-slate-900">Enterprise Capabilities</h2>
              <p className="text-slate-600 max-w-2xl mx-auto text-sm">
                Comprehensive safety equipment detection with enterprise-grade reliability and compliance
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, idx) => (
                <div key={idx} className="bg-white border border-gray-200 p-8 hover:border-gray-300 transition-colors duration-200">
                  <div className="space-y-4">
                    <div className="w-8 h-8 flex items-center justify-center">
                      <feature.icon size={20} className="text-slate-600" />
                    </div>
                    <div className="space-y-2">
                      <h3 className="text-base font-medium text-slate-900">{feature.title}</h3>
                      <p className="text-slate-600 text-sm leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Models Section */}
        <section className="py-24 px-8 bg-white border-t border-gray-100">
          <div className="max-w-6xl mx-auto space-y-16">
            <div className="text-center space-y-4">
              <h2 className="text-2xl font-medium text-slate-900">Model Options</h2>
              <p className="text-slate-600 max-w-2xl mx-auto text-sm">
                Choose the appropriate model configuration for your deployment requirements
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {models.map((model, idx) => (
                <div key={idx} className="bg-white border border-gray-200 p-8 hover:border-gray-300 transition-colors duration-200 relative">
                  {model.status === "Premium" && (
                    <div className="absolute -top-2 left-8">
                      <div className="bg-slate-900 text-white text-xs font-medium px-3 py-1">
                        Premium
                      </div>
                    </div>
                  )}
                  <div className="space-y-6">
                    <div className="space-y-3">
                      <h3 className="text-lg font-medium text-slate-900">{model.name}</h3>
                      <p className="text-slate-600 text-sm leading-relaxed">
                        {model.description}
                      </p>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-center py-2 border-b border-gray-100">
                        <span className="text-sm text-slate-600">Accuracy</span>
                        <span className="text-sm font-medium text-slate-900">{model.accuracy}</span>
                      </div>
                      <div className="flex justify-between items-center py-2 border-b border-gray-100">
                        <span className="text-sm text-slate-600">Equipment Classes</span>
                        <span className="text-sm font-medium text-slate-900">{model.classes}</span>
                      </div>
                      <div className="space-y-3">
                        <span className="text-sm text-slate-600">Detection Capabilities</span>
                        <div className="flex flex-wrap gap-2">
                          {model.features.slice(0, 3).map((feature, featureIdx) => (
                            <span key={featureIdx} className="inline-flex items-center px-2 py-1 bg-gray-100 text-slate-700 text-xs">
                              {feature}
                            </span>
                          ))}
                          {model.features.length > 3 && (
                            <span className="inline-flex items-center px-2 py-1 bg-gray-100 text-slate-700 text-xs">
                              +{model.features.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 px-8 bg-gray-50 border-t border-gray-100">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="space-y-4">
              <h2 className="text-2xl font-medium text-slate-900">Get Started</h2>
              <p className="text-slate-600 max-w-2xl mx-auto text-sm">
                Schedule a demonstration to see how our AI safety detection platform can enhance your workplace safety protocols.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
              <Button 
                onClick={() => navigate('/demo')}
                className="px-8 py-3 bg-slate-900 text-white hover:bg-slate-800 transition-colors duration-200 font-medium text-sm"
                size="lg"
              >
                Request Demo
              </Button>
              <Button 
                onClick={() => navigate('/api-docs')}
                variant="outline"
                className="px-8 py-3 border-gray-300 text-slate-700 hover:bg-gray-50 transition-colors duration-200 text-sm"
                size="lg"
              >
                Documentation
              </Button>
            </div>
            
            <div className="pt-8 border-t border-gray-200">
              <p className="text-xs text-slate-500">
                Enterprise-grade security • SOC 2 Type II • 99.9% uptime SLA
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default NewLandingPage;