export const fetchProducts = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5002/products"); // Asegúrate de que esta ruta es correcta
        if (!response.ok) throw new Error("Error al obtener productos");

        return await response.json(); // Devuelve los productos en formato JSON
    } catch (error) {
        console.error("Error al cargar los productos:", error);
        return []; // Retorna una lista vacía en caso de error
    }
};
