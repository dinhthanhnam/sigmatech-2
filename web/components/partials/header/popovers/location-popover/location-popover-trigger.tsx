import { Button } from "@/components/ui/button";
import { ChevronDown, LucideMapPin } from "lucide-react";
import { BasePopoverTrigger } from "../base-popover-trigger";

export function LocationPopoverTrigger() {
  return (
    <BasePopoverTrigger 
      children={
        <>
          <LucideMapPin className="size-5" strokeWidth={1.7}/>
          <span>Vị trí</span>
          <ChevronDown className="size-5"/>
        </>
      }
    />
  );
}