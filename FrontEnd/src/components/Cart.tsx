"use client";

import { useState } from "react";

interface CartItem {
    id: number;
    name: string;
    price: number;
    quantity: number;
}

const Cart: React.FC<{ cart: CartItem[], setCart: (cart: CartItem[]) => void }> = ({ cart, setCart }) => {
    const [purchaseMessage, setPurchaseMessage] = useState("");

    // ✅ Calcular el total de la compra
    const total = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);

    // ✅ Agregar un producto al carrito y sumar la cantidad si ya existe
    const addToCart = (id: number, name: string, price: number, quantity: number) => {
        setCart(prevCart => {
            const existingItem = prevCart.find(item => item.id === id);
            if (existingItem) {
                return prevCart.map(item =>
                    item.id === id
                        ? { ...item, quantity: item.quantity + quantity } // ✅ Suma la cantidad seleccionada
                        : item
                );
            } else {
                return [...prevCart, { id, name, price, quantity }];
            }
        });
    };

    // ✅ Finalizar compra
    const handleCheckout = () => {
        if (cart.length === 0) return;
        setPurchaseMessage("🎉 Su compra ha sido un éxito. ¡Gracias por comprar con nosotros! 🛍️");
    };

    // ✅ Vaciar el carrito
    const handleClearCart = () => {
        setCart([]);
        setPurchaseMessage("");
    };

    return (
        <div className="p-4 bg-gray-800 text-white rounded-lg w-80">
            <h2 className="text-xl font-bold mb-2">🛒 Carrito de Compras</h2>

            {cart.length === 0 ? (
                <p className="text-gray-400">El carrito está vacío.</p>
            ) : (
                <>
                    <ul>
                        {cart.map((item) => (
                            <li key={item.id} className="border-b border-gray-600 py-2 flex justify-between items-center">
                                <div>
                                    <span className="font-semibold">{item.name}</span>
                                    <span className="text-gray-400"> x{item.quantity}</span>
                                </div>
                                <span className="float-right">${(item.price * item.quantity).toFixed(2)}</span>
                            </li>
                        ))}
                    </ul>

                    {/* ✅ Total de la compra */}
                    <p className="text-lg font-bold mt-4">Total: <span className="text-green-400">${total.toFixed(2)}</span></p>

                    {/* ✅ Botón de Finalizar Compra */}
                    <button
                        className="mt-3 w-full bg-orange-500 px-4 py-2 rounded-lg hover:bg-orange-600"
                        onClick={handleCheckout}
                    >
                        Finalizar Compra
                    </button>
                </>
            )}

            {/* ✅ Mensaje de compra exitosa con botón de vaciar carrito */}
            {purchaseMessage && (
                <div className="mt-3 p-3 bg-green-500 text-white text-center rounded-lg">
                    <p>{purchaseMessage}</p>
                    <button
                        className="mt-2 bg-red-500 px-3 py-1 rounded-lg hover:bg-red-600 transition"
                        onClick={handleClearCart}
                    >
                        Vaciar Carrito
                    </button>
                </div>
            )}
        </div>
    );
};

export default Cart;
