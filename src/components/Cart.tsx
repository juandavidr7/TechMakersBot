"use client";

import { useState } from "react";

const Cart: React.FC<{ products: any[] }> = ({ products }) => {
    const [cart, setCart] = useState<{ id: number; quantity: number }[]>([]);

    const getProduct = (id: number) => products.find(product => product.id === id);

    return (
        <div className="p-4 bg-gray-800 text-white rounded-lg w-80">
            <h2 className="text-xl font-bold mb-2">🛒 Carrito de Compras</h2>
            {cart.length === 0 ? (
                <p className="text-gray-400">El carrito está vacío.</p>
            ) : (
                <ul>
                    {cart.map((item) => {
                        const product = getProduct(item.id);
                        return (
                            <li key={item.id} className="border-b border-gray-600 py-2">
                                <span className="font-semibold">{product?.name}</span> x{item.quantity}
                                <span className="float-right">${(product?.price * item.quantity).toFixed(2)}</span>
                            </li>
                        );
                    })}
                </ul>
            )}
            <button className="mt-3 w-full bg-orange-500 px-4 py-2 rounded-lg hover:bg-orange-600">
                Finalizar Compra
            </button>
        </div>
    );
};

export default Cart;
