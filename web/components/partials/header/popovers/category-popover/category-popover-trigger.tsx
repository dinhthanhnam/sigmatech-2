"use client";

import { Button } from "@/components/ui/button";
import { ChevronDown, LucideBlocks } from "lucide-react";
import { BasePopoverTrigger } from "../base-popover-trigger";
import { useAppStore } from "@/store/store";

export function CategoryPopoverTrigger() {
  const toggleCategoryPopover = useAppStore(
    (s) => s.toggleCategoryPopover
  );

  return (
    <BasePopoverTrigger 
      onClick={toggleCategoryPopover}
      children={
        <>
          <LucideBlocks className="size-5" strokeWidth={1.7}/>
          <span>Danh mục</span>
          <ChevronDown className="size-5"/>
        </>
      }
    />    
  );
}