"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [products, setProducts] = useState([])
  useEffect(() => {
  const fetchData = async () => {
    const res = await fetch("http://localhost:8000/products");
    const data = await res.json();
    setProducts(data);
  };

  fetchData();
}, []);
  return (
    <div>
    {products &&
      products.map((p, i) => (
        <div key={i} className="border p-2 mb-2">
          {Object.entries(p).map(([key, value]) => (
            <div key={key}>
              <strong>{key}:</strong> {String(value)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
