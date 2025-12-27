import { HeroSection } from "@/components/ui/hero-section-with-smooth-bg-shader";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LucideIcon, Cpu, ShieldCheck, Layers, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    icon: Cpu,
    title: "Performance",
    description: "Ultra-fast data processing in every situation.",
  },
  {
    icon: ShieldCheck,
    title: "Security",
    description: "Advanced protection for complete peace of mind.",
  },
  {
    icon: Layers,
    title: "Modularity",
    description: "Easy integration with existing architecture.",
  },
  {
    icon: Zap,
    title: "Responsiveness",
    description: "Instant response to every command.",
  },
];

const DemoOne = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      {/* Hero Section with Smooth Background */}
      <HeroSection 
        title="Discover minimalism and power in"
        highlightText="one place"
        description="Designed with aesthetics and performance in mind. Experience ultra-fast processing, advanced security, and intuitive design."
        buttonText="Get Started"
        onButtonClick={() => navigate('/demo')}
        colors={["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#dda0dd"]}
        distortion={1.2}
        speed={0.8}
        swirl={0.9}
        offsetX={0.15}
        titleClassName="text-white"
        descriptionClassName="text-white/90"
        buttonClassName="bg-white text-black hover:bg-white/90 border-white/20"
      />
      
      {/* Features Section */}
      <section className="py-16 px-8 bg-background">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <Badge variant="secondary" className="mb-4">
              ✨ Next Generation Tools
            </Badge>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Everything you need to build amazing applications with cutting-edge technology
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="border border-border rounded-xl p-4 md:p-6 h-40 md:h-48 flex flex-col justify-start items-start space-y-2 md:space-y-3 hover:shadow-lg transition-all duration-300"
              >
                <feature.icon size={18} className="text-primary md:w-5 md:h-5" />
                <h3 className="text-sm md:text-base font-medium">{feature.title}</h3>
                <p className="text-xs md:text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export { DemoOne };