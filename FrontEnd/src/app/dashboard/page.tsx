"use client";

import { useState, useEffect } from "react";
import DashboardCharts from "../../components/DashBoardcharts";
import Cart from "@/components/Cart";
import Chat from "@/components/Chat";
import NavBar from "@/components/Navbar";
import { useRouter } from "next/navigation";

export default function Dashboard() {
    const [isChatOpen, setIsChatOpen] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const role = localStorage.getItem("role");
        if (role !== "admin") {
            router.push("/");
        }
    }, []);

    return (
        <div className="bg-gray-900 min-h-screen text-black relative">
            <NavBar />

            <div className="text-center py-6">
                <h1 className="text-4xl font-bold text-amber-400">Admin Dashboard</h1>
            </div>

            <div className="flex flex-col items-center p-6">
                <div className="mb-6">
                    <DashboardCharts />
                </div>
            </div>


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
