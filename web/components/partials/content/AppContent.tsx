import {ReactNode} from "react";

export function AppContent({children}: {children: ReactNode}) {
  return (
    <main id={`app-content`} className={`app-content`}>
      <div className={`common-container`}>
        {children}
      </div>
    </main>
  );
}