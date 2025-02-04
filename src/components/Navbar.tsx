"use client";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { useAuth } from "@/app/hooks/useAuth";

export default function Navbar({ onHelpClick }: { onHelpClick: () => void }) {
    const [isOpen, setIsOpen] = useState(false);
    const { isAuthenticated, role, showLogin, setShowLogin, handleLogin, handleLogout } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    return (
        <nav className="bg-gray-900 text-white p-4 relative">
            <div className="container mx-auto flex justify-between items-center">
                {/* Logo */}
                <div className="text-xl font-bold flex items-center">
                    <span className="text-orange-500 text-2xl">🎮</span>
                    <span className="ml-2">Makers Tech</span>
                </div>

                {/* Menú de Navegación */}
                <div className="hidden md:flex space-x-8 text-lg">
                    <a href="/" className="hover:text-orange-500">Inicio</a>
                    <button onClick={onHelpClick} className="hover:text-yellow-500">Ayuda</button> {/* ✅ Abre chat grande */}

                    {role === "admin" && (
                        <a href="/dashboard" className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg">Dashboard</a>
                    )}
                </div>

                {/* Botón de Inicio de Sesión o Logout */}
                <div className="hidden md:block">
                    {isAuthenticated ? (
                        <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg">
                            Logout
                        </button>
                    ) : (
                        <button onClick={() => setShowLogin(!showLogin)} className="bg-yellow-500 hover:bg-orange-600 px-4 py-2 rounded-lg">
                            Sign Up
                        </button>
                    )}
                </div>

                {/* Menú Mobile */}
                <div className="md:hidden">
                    <button onClick={() => setIsOpen(!isOpen)}>
                        {isOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>

            {/* Formulario de Login */}
            {showLogin && !isAuthenticated && (
                <div className="absolute top-16 right-4 bg-gray-800 text-white p-4 rounded-lg shadow-lg w-64">
                    <h3 className="text-lg font-bold mb-2">Iniciar Sesión</h3>
                    <form onSubmit={(e) => handleLogin(e, username, password)} className="flex flex-col gap-2">
                        <input
                            type="text"
                            placeholder="Usuario"
                            className="p-2 border rounded text-black"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                        <input
                            type="password"
                            placeholder="Contraseña"
                            className="p-2 border rounded text-black"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <button type="submit" className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg mt-2">
                            Login
                        </button>
                    </form>
                </div>
            )}
        </nav>
    );
}
