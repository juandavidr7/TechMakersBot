"use client";

import { useState, useEffect, useRef } from "react";
import { sendChatMessage } from "@/app/pages/api/chatbot"; // ✅ Importa la lógica del chatbot

// Definir estructura del mensaje
interface Message {
    sender: "user" | "bot";
    text: string;
}

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");
    const chatContainerRef = useRef<HTMLDivElement | null>(null);


    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage: Message = { sender: "user", text: input };
        setMessages(prevMessages => [...prevMessages, userMessage]);


        setInput("");

        const botResponse = await sendChatMessage(input);
        const botMessage: Message = { sender: "bot", text: botResponse.response };
        setMessages(prevMessages => [...prevMessages, botMessage]);
    };
    return (
        <div className="flex justify-center items-center fixed bottom-20 right-6 w-[350px] h-[500px] bg-white shadow-xl rounded-lg border border-gray-300">
            <div className="w-full h-full flex flex-col p-4">
                <h2 className="text-lg font-bold text-center mb-2 text-gray-700">💬 Makers Tech Chat</h2>

                {/* Chat Container */}
                <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-2 border rounded-lg bg-gray-50">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`p-2 my-1 rounded-lg max-w-[80%] ${
                                msg.sender === "user"
                                    ? "ml-auto bg-blue-500 text-white"
                                    : "mr-auto bg-gray-300 text-black"
                            }`}
                        >
                            {msg.text}
                        </div>
                    ))}
                </div>

                <form className="flex mt-2" onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
                    <input
                        type="text"
                        className="flex-grow border rounded-lg p-2 text-gray-700 focus:ring focus:ring-blue-300"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Escribe tu mensaje..."
                    />
                    <button
                        className="ml-2 bg-blue-500 text-white px-3 py-2 rounded-lg hover:bg-blue-600 transition"
                        type="submit"
                    >
                        ➤
                    </button>
                </form>
            </div>
        </div>
    );
}
