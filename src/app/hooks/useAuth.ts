import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export function useAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [role, setRole] = useState<string | null>(null);
    const [showLogin, setShowLogin] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const storedRole = localStorage.getItem("role");
        setRole(storedRole);
        setIsAuthenticated(storedRole !== null);
    }, []);

    // ✅ Función para iniciar sesión con el backend
    const handleLogin = async (e: React.FormEvent, username: string, password: string) => {
        e.preventDefault();

        try {
            const response = await fetch("http://127.0.0.1:8092/auth/login", { // Cambia la URL por la correcta
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error("Credenciales incorrectas");
            }

            const data = await response.json();

            // ✅ Guardar credenciales en localStorage
            localStorage.setItem("isAuthenticated", "true");
            localStorage.setItem("role", data.role); // Asume que el backend envía un campo `role`
            setRole(data.role);
            setIsAuthenticated(true);

            setShowLogin(false);
            router.push("/");
        } catch (error) {
            alert("Credenciales incorrectas");
        }
    };

    // ✅ Función para cerrar sesión
    const handleLogout = () => {
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("role");
        setIsAuthenticated(false);
        setRole(null);
        router.push("/");
    };

    return { isAuthenticated, role, showLogin, setShowLogin, handleLogin, handleLogout };
}
