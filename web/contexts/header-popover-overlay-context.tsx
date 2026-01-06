"use client";

import { createContext, Dispatch, ReactNode, SetStateAction, useContext, useState } from "react";

export type HeaderPopoverOverlayContextType = {
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
}

const HeaderPopoverOverlayContext = createContext<HeaderPopoverOverlayContextType | undefined>(undefined);

export function HeaderPopoverOverlayProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <HeaderPopoverOverlayContext.Provider value={{ isOpen, setIsOpen }}>
      {children}
    </HeaderPopoverOverlayContext.Provider>
  );
}

export function useHeaderPopoverOverlayContext() {
  const context = useContext(HeaderPopoverOverlayContext);
  if (!context) {
    throw new Error("useHeaderPopoverOverlayContext must be used within a HeaderPopoverOverlayProvider");
  }
  return context;
}