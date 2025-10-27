import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { MessageSquare, Mic, Languages, Bot, Hand, FileText, ArrowRight, Zap, Users, Globe } from "lucide-react";
import heroBackground from "@/assets/hero-bg.jpg";

const Index = () => {
  const features = [
    {
      icon: MessageSquare,
      title: "Text-to-Speech",
      description: "Transform text into natural, human-like voice with advanced AI technology."
    },
    {
      icon: Mic,
      title: "Speech-to-Text",
      description: "Real-time transcription of spoken words with exceptional accuracy."
    },
    {
      icon: Languages,
      title: "Multilingual Support",
      description: "Seamless communication across multiple Indian languages for inclusive collaboration."
    },
    {
      icon: Bot,
      title: "AI Chatbot",
      description: "Intelligent assistance during meetings with instant, context-aware responses."
    },
    {
      icon: Hand,
      title: "Sign Language Detection",
      description: "AI-powered recognition and interpretation of sign language for accessibility."
    },
    {
      icon: FileText,
      title: "Meeting Summary",
      description: "Automatically generate detailed summaries after every session."
    }
  ];

  const steps = [
    {
      icon: Zap,
      title: "Start",
      description: "Launch your meeting with a single click"
    },
    {
      icon: Users,
      title: "Communicate",
      description: "Engage with AI-powered tools and real-time features"
    },
    {
      icon: FileText,
      title: "Summarize",
      description: "Get instant meeting summaries and actionable insights"
    }
  ];

  const useCases = [
    {
      icon: Globe,
      title: "Education",
      description: "Break language barriers in online classrooms and virtual lectures"
    },
    {
      icon: Users,
      title: "Corporate Meetings",
      description: "Enhance productivity with AI-powered summaries and transcription"
    },
    {
      icon: Hand,
      title: "Accessibility",
      description: "Enable inclusive communication for hearing-impaired participants"
    }
  ];

  const launchMeeting =() =>{
    window.location.href = "http://127.0.0.1:8000/";
  }

  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url(${heroBackground})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          <div className="absolute inset-0 bg-gradient-hero opacity-90"></div>
          <div className="absolute inset-0 bg-gradient-glow animate-glow-pulse"></div>
        </div>
        
        <div className="relative z-10 container mx-auto px-4 py-20 text-center animate-fade-in">
          <div className="inline-block mb-6 px-6 py-2 rounded-full bg-primary/20 border border-primary/50 backdrop-blur-sm">
            <span className="text-primary font-medium">The Future of Communication</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fade-in-up">
            SENSE
            <span className="block mt-2 text-transparent bg-clip-text bg-gradient-to-r from-primary via-secondary to-primary">
              The New Light of Communication
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            Empowering inclusive, intelligent, and seamless meetings with AI-powered communication tools
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <Button variant="hero" size="lg" onClick={launchMeeting}>
              Start Meeting <ArrowRight className="ml-2" />
            </Button>
            {/* <Button variant="hero-outline" size="lg">
              Try Demo
            </Button> */}
          </div>
        </div>

        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-float">
          <div className="w-6 h-10 border-2 border-primary rounded-full flex items-start justify-center p-2">
            <div className="w-1.5 h-3 bg-primary rounded-full animate-pulse"></div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-24 px-4 relative">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Breaking Communication Barriers
          </h2>
          <p className="text-xl text-muted-foreground leading-relaxed">
            SENSE revolutionizes digital communication by integrating cutting-edge AI and accessibility technologies. 
            Our mission is to make every conversation seamless, inclusive, and effortless—empowering individuals and teams 
            to connect without boundaries.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-background to-muted/20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powerful Features for Everyone
            </h2>
            <p className="text-xl text-muted-foreground">
              AI-driven tools designed to enhance communication and accessibility
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card 
                  key={index}
                  className="p-8 bg-gradient-card backdrop-blur-lg border-primary/20 shadow-card hover:shadow-glow-cyan transition-all duration-300 hover:scale-105 hover:border-primary/50 group"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="mb-6 relative">
                    <div className="w-16 h-16 rounded-lg bg-primary/20 flex items-center justify-center group-hover:bg-primary/30 transition-all duration-300">
                      <Icon className="w-8 h-8 text-primary group-hover:scale-110 transition-transform duration-300" />
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Three simple steps to transform your communication
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <div key={index} className="relative">
                  <div className="text-center">
                    <div className="mb-6 relative inline-block">
                      <div className="w-20 h-20 rounded-full bg-gradient-card border-2 border-primary/50 flex items-center justify-center backdrop-blur-lg shadow-glow-cyan">
                        <Icon className="w-10 h-10 text-primary" />
                      </div>
                      <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold shadow-glow-cyan">
                        {index + 1}
                      </div>
                    </div>
                    <h3 className="text-2xl font-bold mb-3">{step.title}</h3>
                    <p className="text-muted-foreground">{step.description}</p>
                  </div>
                  
                  {index < steps.length - 1 && (
                    <div className="hidden md:block absolute top-10 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-primary/50 to-transparent"></div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-background to-muted/20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Where SENSE Shines
            </h2>
            <p className="text-xl text-muted-foreground">
              Transforming communication across industries
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {useCases.map((useCase, index) => {
              const Icon = useCase.icon;
              return (
                <Card 
                  key={index}
                  className="p-8 text-center bg-gradient-card backdrop-blur-lg border-primary/20 shadow-card hover:shadow-glow-violet transition-all duration-300 hover:scale-105 hover:border-primary/50 group"
                >
                  <div className="mb-6 flex justify-center">
                    <div className="w-16 h-16 rounded-lg bg-secondary/20 flex items-center justify-center group-hover:bg-secondary/30 transition-all duration-300">
                      <Icon className="w-8 h-8 text-secondary group-hover:scale-110 transition-transform duration-300" />
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold mb-3">{useCase.title}</h3>
                  <p className="text-muted-foreground">{useCase.description}</p>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4">
        <div className="container mx-auto max-w-4xl text-center">
          <div className="relative p-12 rounded-2xl bg-gradient-card backdrop-blur-lg border border-primary/20 shadow-glow-cyan">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your Communication?
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of users experiencing seamless, inclusive meetings
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="hero" size="lg">
                Get Started Now <ArrowRight className="ml-2" />
              </Button>
              <Button variant="hero-outline" size="lg">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-primary/20">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div className="col-span-1 md:col-span-2">
              <h3 className="text-2xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                SENSE
              </h3>
              <p className="text-muted-foreground mb-4">
                The New Light of Communication
              </p>
              <p className="text-sm text-muted-foreground">
                Empowering inclusive, intelligent, and seamless meetings.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="#" className="hover:text-primary transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Demo</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="#" className="hover:text-primary transition-colors">About</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Support</a></li>
              </ul>
            </div>
          </div>
          
          <div className="pt-8 border-t border-primary/20 text-center text-muted-foreground">
            <p>&copy; 2025 SENSE. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
