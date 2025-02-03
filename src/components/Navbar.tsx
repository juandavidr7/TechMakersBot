"use client";
import { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [showLogin, setShowLogin] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const router = useRouter();

    useEffect(() => {
        setIsAuthenticated(localStorage.getItem("isAuthenticated") === "true");
    }, []);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        localStorage.setItem("isAuthenticated", "true");
        setIsAuthenticated(true);
        setShowLogin(false); // Cierra la caja de login
        router.push("/dashboard"); // Redirige al dashboard
    };

    const handleLogout = () => {
        localStorage.removeItem("isAuthenticated");
        setIsAuthenticated(false);
        router.push("/"); // Redirige a inicio
    };

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
                    <a href="#" className="hover:text-yellow-500">Productos</a>
                    <a href="#" className="hover:text-yellow-500">Recomendaciones</a>
                    <a href="#" className="hover:text-yellow-500">Ayuda</a>
                </div>

                {/* Botón Sign Up / Logout */}
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

            {/* Caja de Login */}
            {showLogin && !isAuthenticated && (
                <div className="absolute top-16 right-4 bg-gray-800 text-white p-4 rounded-lg shadow-lg w-64">
                    <h3 className="text-lg font-bold mb-2">Iniciar Sesión</h3>
                    <form onSubmit={handleLogin} className="flex flex-col gap-2">
                        <input type="text" placeholder="Usuario" className="p-2 border rounded text-black" required />
                        <input type="password" placeholder="Contraseña" className="p-2 border rounded text-black" required />
                        <button type="submit" className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg mt-2">
                            Login
                        </button>
                    </form>
                </div>
            )}
        </nav>
    );
}
