import {ReactNode} from "react";
import { AppOverlay } from "./AppOverlay";

export function AppContent({children}: {children: ReactNode}) {
  return (
    <main id={`app-content`} className={`app-content relative overflow-hidden`}>
      <div className={`common-container px-2 pt-1`}>
        {children}
      </div>
    </main>
  );
}