import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cdn2.cellphones.com.vn",
        pathname: "/**",
      },
    ]
  }
};

export default nextConfig;
