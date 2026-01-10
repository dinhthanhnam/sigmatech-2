import { create } from "zustand";

type State = {
  isCategoryPopoverOpen: boolean;
  isLocationPopoverOpen: boolean;
  isOverlayActive: boolean;
};

type Actions = {
  toggleCategoryPopover: () => void;
  toggleLocationPopover: () => void;
  toggleOverlayActive: () => void;
};

export const useAppStore = create<State & Actions>((set) => ({
  isCategoryPopoverOpen: false,
  isLocationPopoverOpen: false,
  isOverlayActive: false,
  toggleCategoryPopover: () => set((s) => ({ isCategoryPopoverOpen: !s.isCategoryPopoverOpen })),
  toggleLocationPopover: () => set((s) => ({ isLocationPopoverOpen: !s.isLocationPopoverOpen })),
  toggleOverlayActive: () => set((s) => ({ isOverlayActive: !s.isOverlayActive })),
}));
