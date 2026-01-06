import {ReactNode} from "react";

export default function AppContent({children}: {children: ReactNode}) {
  return (
    <main id={`app-content`} className={`app-content`}>
      <div className={`common-container`}>
        {children}
      </div>
    </main>
  );
}