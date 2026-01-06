"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [products, setProducts] = useState([])
  // useEffect(() => {
  //   const fetchData = async () => {
  //     const res = await fetch("http://localhost:8000/products");
  //     const data = await res.json();
  //     setProducts(data);
  //   };
  //
  //   fetchData();
  // }, []);
  return (
    <div className={`h-screen`}>
      abc
    </div>
  );
}
