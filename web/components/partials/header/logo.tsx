import Image from "next/image";

export default function Logo() {
  return (
    <div className={`hover:scale-95 transition-all duration-200 ease-in-out`}>
      <div className="h-10 w-10 overflow-hidden transition-all duration-200">
      <span className="cps-image-cdn relative inline-block">
        <Image unoptimized alt="CellphoneS Logo" loading="lazy" width="350" height="400"
               decoding="async" data-nimg="1"
               className="transition-opacity duration-500 opacity-100 object-contain"
               style={{ color: "transparent" }}
               src="https://cdn2.cellphones.com.vn/x/media/wysiwyg/Web/campaign/2026/Logo_TET_2026_Mb.gif"
        />
      </span>
      </div>
    </div>
  );
}