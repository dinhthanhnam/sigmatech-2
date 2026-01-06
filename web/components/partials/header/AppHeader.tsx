import Marquee from "./marquee";
import Logo from "./logo";
import { CategoryPopoverTrigger, LocationPopoverTrigger } from "./popovers";
import { LoginButton } from "./buttons";
import { HeaderSearchInput } from "./search-input";

const HeaderLayout = {
  Root: "common-container flex flex-col",
  Main: "flex flex-row w-full py-2 gap-2",
};
export function AppHeader() {
  return (
    <header className="app-header">
      <div className={HeaderLayout.Root}>
        <Marquee />
        <div className={HeaderLayout.Main}>
          <Logo />
          <CategoryPopoverTrigger />
          <LocationPopoverTrigger />
          <HeaderSearchInput />
          <LoginButton />
        </div>
      </div>
    </header>
  );
}