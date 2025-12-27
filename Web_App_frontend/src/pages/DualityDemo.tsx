import { Scene } from "@/components/ui/hero-section";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LucideIcon, Eye, Brain, Target, Zap, ShieldCheck, Layers } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    icon: Eye,
    title: "Computer Vision",
    description: "Advanced object detection with 90%+ accuracy.",
  },
  {
    icon: Brain,
    title: "AI-Powered",
    description: "State-of-the-art YOLO models for safety detection.",
  },
  {
    icon: Target,
    title: "Precision Detection",
    description: "Identify safety equipment with pinpoint accuracy.",
  },
  {
    icon: Zap,
    title: "Real-Time Processing",
    description: "Lightning-fast inference for instant results.",
  },
];

const DualityDemo = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-svh w-screen bg-gradient-to-br from-[#000] to-[#1A2428] text-white flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-6xl space-y-12 relative z-10">
        <div className="flex flex-col items-center text-center space-y-8">
          <Badge variant="secondary" className="backdrop-blur-sm bg-white/10 border border-white/20 text-white hover:bg-white/20 px-4 py-2 rounded-full">
            🛡️ Next Generation AI Safety Detection
          </Badge>
          
          <div className="space-y-6 flex items-center justify-center flex-col">
            <h1 className="text-3xl md:text-6xl font-semibold tracking-tight max-w-3xl">
              DUALITY AI
            </h1>
            <h2 className="text-xl md:text-2xl font-light text-neutral-300 max-w-3xl">
              Advanced Computer Vision for Safety Equipment Detection
            </h2>
            <p className="text-lg text-neutral-300 max-w-2xl">
              Powered by state-of-the-art YOLO models with 90%+ accuracy. Detect fire extinguishers, oxygen tanks, emergency equipment, and more in real-time.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 items-center">
              <Button 
                onClick={() => navigate('/demo')}
                className="text-sm px-8 py-3 rounded-xl bg-white text-black border border-white/10 shadow-none hover:bg-white/90 transition-none"
              >
                Try Live Demo
              </Button>
              <Button 
                onClick={() => navigate('/models')}
                className="text-sm px-8 py-3 rounded-xl bg-transparent text-white border border-white/20 shadow-none hover:bg-white/10 transition-none"
              >
                Explore Models
              </Button>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6 max-w-5xl mx-auto">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-4 md:p-6 h-40 md:h-48 flex flex-col justify-start items-start space-y-2 md:space-y-3"
            >
              <feature.icon size={18} className="text-white/80 md:w-5 md:h-5" />
              <h3 className="text-sm md:text-base font-medium">{feature.title}</h3>
              <p className="text-xs md:text-sm text-neutral-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
      
      <div className='absolute inset-0'>
        <Scene />
      </div>
    </div>
  );
};

export { DualityDemo };