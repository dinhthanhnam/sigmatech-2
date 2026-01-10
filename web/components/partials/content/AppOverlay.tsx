import {ReactNode} from "react";

export function AppOverlay() {
  return (
    <div className={`w-full h-full inset-0 z-10 bg-black/30 backdrop-blur-sm`}>
    </div>
  );
}