import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import ModelDemo from "./pages/ModelDemo";
import SimpleDemo from "./pages/SimpleDemo";
import ProperDemo from "./pages/ProperDemo";
import LandingPage from "./pages/LandingPage";
import LandingPageSimple from "./pages/LandingPageSimple";
import LandingPageEnhanced from "./pages/LandingPageEnhanced";
import LandingPagePremium from "./pages/LandingPagePremium";
import NewLandingPage from "./pages/NewLandingPage";
import { DemoOne } from "./pages/DemoOne";
import { DualityDemo } from "./pages/DualityDemo";
import TestPage from "./pages/TestPage";
import ApiDocs from "./pages/ApiDocs";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<NewLandingPage />} />
          <Route path="/demo" element={<ProperDemo />} />
          <Route path="/models" element={<ModelDemo />} />
          <Route path="/api-docs" element={<ApiDocs />} />
          <Route path="/demo-one" element={<DemoOne />} />
          <Route path="/duality-3d" element={<DualityDemo />} />
          <Route path="/enhanced" element={<LandingPageEnhanced />} />
          <Route path="/premium" element={<LandingPagePremium />} />
          <Route path="/test" element={<TestPage />} />
          <Route path="/landing-simple" element={<LandingPageSimple />} />
          <Route path="/landing-3d" element={<LandingPage />} />
          <Route path="/simple" element={<SimpleDemo />} />
          <Route path="/proper" element={<ProperDemo />} />
          <Route path="/index" element={<Index />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
