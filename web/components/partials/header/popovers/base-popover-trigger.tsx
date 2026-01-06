import { Button } from "@/components/ui/button";
import { ReactNode } from "react";

export function BasePopoverTrigger({className, children}: {className?: string, children?: ReactNode}) {
  return (
    <Button variant="default" className={`${className} min-h-[40] px-2  ml-1 bg-primary-300 hover:bg-primary-500 text-background hover:text-background flex flex-row gap-1 font-normal! cursor-pointer`}>
      {children}
    </Button>
  );
}
