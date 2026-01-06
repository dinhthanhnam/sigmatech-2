import { Button } from "@/components/ui/button";
import { ChevronDown, LucideBlocks } from "lucide-react";
import { BasePopoverTrigger } from "../base-popover-trigger";

export function CategoryPopoverTrigger() {
  return (
    <BasePopoverTrigger 
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