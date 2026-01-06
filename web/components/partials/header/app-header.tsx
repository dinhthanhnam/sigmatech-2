import Marquee from "@/components/partials/header/marquee";
import Logo from "@/components/partials/header/logo";

export default function AppHeader() {
  return (
    <header className="app-header">
      <div className={`common-container flex flex-col`}>
        <Marquee />
        <div className={`flex flex-row w-full py-2`}>
          <Logo />
        </div>
      </div>
    </header>
  );
}