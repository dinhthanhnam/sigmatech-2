import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

export function HeaderSearchInput() {
  return (
    <div className="relative flex flex-row grow bg-background text-foreground rounded-md gap-2 px-2">
      <Search className="size-5 text-muted-foreground flex self-center justify-self-center" />
      <Input
        type="text"
        placeholder="Bạn đang tìm kiếm gì?"
        className="min-h-[40] flex grow focus-visible:ring-0! p-0 border-none"
      />
    </div>
  );
}