"use client";

import { useState, useEffect, useRef } from "react";
import { sendChatMessage } from "@/app/pages/api/chatbot"; // ✅ Importa la API del chatbot

interface Message {
    sender: "user" | "bot";
    text: string;
}

const FullScreenChat: React.FC<{ onClose: () => void }> = ({ onClose }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");
    const chatContainerRef = useRef<HTMLDivElement | null>(null);

    // ✅ Auto-scroll cuando se agregan mensajes
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage: Message = { sender: "user", text: input };
        setMessages(prevMessages => [...prevMessages, userMessage]);

        setInput(""); // Limpia el input después de enviar

        try {
            const botResponse = await sendChatMessage(input);

            console.log("🔍 Respuesta del chatbot:", botResponse); // 🛠 Debug

            const botMessage: Message = { sender: "bot", text: botResponse.response };


            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error("Error en el chatbot:", error);
            setMessages(prevMessages => [
                ...prevMessages,
                { sender: "bot", text: "❌ Hubo un error, intenta de nuevo." }
            ]);
        }
    };


    return (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-90 flex justify-center items-center">
            <div className="bg-white w-3/4 h-3/4 p-6 rounded-lg shadow-xl flex flex-col">
                {/* ✅ Encabezado con botón para cerrar */}
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-2xl font-bold text-gray-800">Asistente Virtual</h2>
                    <button
                        onClick={onClose}
                        className="bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600"
                    >
                        Cerrar
                    </button>
                </div>

                {/* ✅ Área de mensajes */}
                <div ref={chatContainerRef} className="flex-grow overflow-y-auto border p-4 bg-gray-100 rounded-lg">
                    {messages.length === 0 ? (
                        <p className="text-gray-500 text-center">Escribe un mensaje para comenzar...</p>
                    ) : (
                        messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`p-2 my-1 rounded-lg max-w-xs ${
                                    msg.sender === "user"
                                        ? "bg-blue-500 text-white self-end ml-auto"
                                        : "bg-gray-300 text-black self-start"
                                }`}
                            >
                                {msg.text}
                            </div>
                        ))
                    )}
                </div>

                {/* ✅ Input de mensaje */}
                <form className="mt-4 flex" onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
                    <input
                        type="text"
                        className="flex-grow p-2 border rounded-lg text-gray-700 focus:ring focus:ring-blue-300"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Escribe tu mensaje..."
                    />
                    <button
                        className="ml-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
                        type="submit"
                    >
                        ➤
                    </button>
                </form>
            </div>
        </div>
    );
};

export default FullScreenChat;
