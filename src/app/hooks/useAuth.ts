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

    const handleLogin = (e: React.FormEvent, username: string, password: string) => {
        e.preventDefault();

        if (username === "admin" && password === "123456") {
            localStorage.setItem("isAuthenticated", "true");
            localStorage.setItem("role", "admin");
            setRole("admin");
            setIsAuthenticated(true);
        } else if (username === "usuario" && password === "prueba123") {
            localStorage.setItem("isAuthenticated", "true");
            localStorage.setItem("role", "user");
            setRole("user");
            setIsAuthenticated(true);
        } else {
            alert("Credenciales incorrectas");
            return;
        }

        setShowLogin(false);
        router.push("/");
    };

    const handleLogout = () => {
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("role");
        setIsAuthenticated(false);
        setRole(null);
        router.push("/");
    };

    return { isAuthenticated, role, showLogin, setShowLogin, handleLogin, handleLogout };
}
