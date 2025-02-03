"use client";

import { useState } from "react";
import ProductList from "../components/ProductList";
import Cart from "../components/Cart";
import Chat from "@/components/Chat";
import NavBar from "../components/Navbar";

export default function Home() {
    const [isChatOpen, setIsChatOpen] = useState(false);
    const [cart, setCart] = useState<{ id: number; name: string; price: number; quantity: number }[]>([]);

    // Función para añadir productos al carrito
    const addToCart = (id: number, name: string, price: number) => {
        setCart((prevCart) => {
            const existingProduct = prevCart.find((item) => item.id === id);
            if (existingProduct) {
                return prevCart.map((item) =>
                    item.id === id ? { ...item, quantity: item.quantity + 1 } : item
                );
            }
            return [...prevCart, { id, name, price, quantity: 1 }];
        });
    };

    return (
        <div className="bg-gray-900 min-h-screen text-black relative">
            <NavBar />

            <div className="text-center py-6">
                <h1 className="text-4xl font-bold text-amber-400">Online Store</h1>
            </div>

            <div className="flex flex-col items-center p-6">
                <div className="mb-6">
                    <ProductList onAddToCart={addToCart} />
                </div>
                <Cart cart={cart} />
            </div>

            {/* Botón flotante para abrir/cerrar el chat */}
            <button
                onClick={() => setIsChatOpen(!isChatOpen)}
                className="fixed bottom-6 right-6 bg-blue-500 text-white px-4 py-2 rounded-full shadow-lg hover:bg-blue-600 transition"
            >
                {isChatOpen ? "Cerrar Chat" : "💬 Asistente virtual"}
            </button>


            {isChatOpen && (
                <div className="fixed bottom-16 right-6 bg-white p-4 shadow-lg rounded-lg w-80 h-96 border border-gray-300">
                    <Chat />
                </div>
            )}
        </div>
    );
}
