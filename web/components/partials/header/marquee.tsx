"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

export default function Marquee() {
  const [hide, setHide] = useState(false);

  useEffect(() => {
    const el = document.getElementById("app-content");
    if (!el) return;

    const onScroll = () => {
      setHide(el.scrollTop > 60);
    };

    el.addEventListener("scroll", onScroll);
    return () => el.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div
      className={`
      transition-all duration-200 ease-in-out text-xs relative select-none overflow-hidden
      ${hide ? "opacity-0 h-0" : "opacity-100 h-4.5"}
    `}
    >
      <div className={`flex items-center gap-4 overflow-hidden`}>
        <div className={`relative flex-1 overflow-hidden`}>
          <div className={`animate-scroll-left-infinite gap-6 inline-flex whitespace-nowrap`}>
            <span>This is 1st long long marquee</span>
            <span>This is 2nd long long marquee</span>
            <span>This is 3rd long long marquee</span>
            {/* duplicate */}
            <span>This is 1st long long marquee</span>
            <span>This is 2nd long long marquee</span>
            <span>This is 3rd long long marquee</span>
          </div>
        </div>
        <div className={`hidden md:flex items-center shrink-0 gap-7`}>
          <Link
            className={`flex items-center gap-1 whitespace-nowrap cursor-pointer relative hover:scale-95 transition-all duration-300
        before:absolute before:top-1/2 before:-translate-y-1/2 before:-left-[15px] before:w-0.5 before:h-3 before:bg-primary-200`}
            href={`/`}
          >
        <span>
          Cửa hàng gần bạn
        </span>
          </Link>
          <Link
            className={`flex items-center gap-1 whitespace-nowrap cursor-pointer relative hover:scale-95 transition-all duration-300
        before:absolute before:top-1/2 before:-translate-y-1/2 before:-left-[15px] before:w-0.5 before:h-3 before:bg-primary-200`}
            href={`/`}
          >
        <span>
          Cửa hàng gần bạn
        </span>
          </Link>
          <Link
            className={`flex items-center gap-1 whitespace-nowrap cursor-pointer relative hover:scale-95 transition-all duration-300
        before:absolute before:top-1/2 before:-translate-y-1/2 before:-left-[15px] before:w-0.5 before:h-3 before:bg-primary-200`}
            href={`/`}
          >
        <span>
          Cửa hàng gần bạn
        </span>
          </Link>
        </div>
      </div>
    </div>
  );
}
