import HeroSection from '../components/HeroSection';
import ScreenshotSection from '../components/ScreenshotSection';
import FeaturesSection from '../components/FeaturesSection';
import AtsSection from '../components/AtsSection';
import ClaudeSkillsSection from '../components/ClaudeSkillsSection';
import CtaSection from '../components/CtaSection';

export default function Home() {
  return (
    <main className="flex flex-col items-center">
      <HeroSection />
      <ScreenshotSection />
      <FeaturesSection />
      <AtsSection />
      <ClaudeSkillsSection />
      <CtaSection />
    </main>
  );
}