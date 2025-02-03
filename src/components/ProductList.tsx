"use client";

import { useState, useEffect } from "react";
import ProductCard from "./ProductCard";
import { fetchProducts } from "@/app/pages/api/products";

const ProductList: React.FC<{ onAddToCart: (id: number, name: string, price: number) => void }> = ({ onAddToCart }) => {
    const [products, setProducts] = useState<{ id: number; name: string; image: string; price: number; stock: number }[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadProducts = async () => {
            setLoading(true);
            const data = await fetchProducts();
            setProducts(data);
            setLoading(false);
        };
        loadProducts();
    }, []);

    if (loading) {
        return <p className="text-white text-center">Cargando productos...</p>;
    }

    return (
        <div className="flex flex-wrap gap-6 justify-center">
            {products.length > 0 ? (
                products.map((product) => (
                    <ProductCard
                        key={product.id}
                        {...product}
                        onAddToCart={() => onAddToCart(product.id, product.name, product.price)}
                    />
                ))
            ) : (
                <p className="text-white text-center">No hay productos disponibles.</p>
            )}
        </div>
    );
};

export default ProductList;
