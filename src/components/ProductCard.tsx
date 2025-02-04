"use client";

import { useState } from "react";

interface ProductProps {
    id: number;
    name: string;
    image_base64?: string;
    price: number;
    stock: number;
    onAddToCart: (quantity: number) => void; // ✅ Ahora recibe la cantidad
}

const ProductCard: React.FC<ProductProps> = ({ id, name, image_base64, price, stock, onAddToCart }) => {
    const [quantity, setQuantity] = useState(1);

    return (
        <div className="bg-gray-100 shadow-lg rounded-lg p-4 w-64">
            {image_base64 ? (
                <img src={`data:image/png;base64,${image_base64}`} alt={name} className="w-full h-40 object-cover rounded-md" />
            ) : (
                <div className="w-full h-40 bg-gray-300 flex items-center justify-center">
                    <span className="text-gray-500">No Image</span>
                </div>
            )}

            <h2 className="text-lg font-bold text-gray-900 mt-2">{name}</h2>
            <p className="text-gray-700">
                Precio: <span className="text-amber-500 font-bold">${price.toFixed(2)}</span>
            </p>
            <p className="text-gray-700">Stock: {stock} unidades</p>

            {/* ✅ Controles para seleccionar la cantidad */}
            <div className="flex items-center mt-2">
                <button
                    className="px-2 py-1 bg-gray-300 rounded-md"
                    onClick={() => setQuantity((prev) => Math.max(1, prev - 1))}
                >
                    -
                </button>
                <span className="mx-2">{quantity}</span>
                <button
                    className="px-2 py-1 bg-gray-300 rounded-md"
                    onClick={() => setQuantity((prev) => Math.min(stock, prev + 1))}
                >
                    +
                </button>
            </div>

            {/* ✅ Botón para añadir al carrito con la cantidad seleccionada */}
            <button
                className="bg-amber-500 text-white px-4 py-2 mt-3 w-full rounded-lg hover:bg-amber-600 transition"
                onClick={() => onAddToCart(quantity)} // ✅ Pasamos la cantidad seleccionada
                disabled={stock === 0}
            >
                {stock > 0 ? "Añadir al Carrito" : "Agotado"}
            </button>
        </div>
    );
};

export default ProductCard;
