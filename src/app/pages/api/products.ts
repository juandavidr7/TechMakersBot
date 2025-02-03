export const fetchProducts = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8060/products");
        if (!response.ok) throw new Error("Error al obtener productos");

        return await response.json(); // Devuelve los productos en formato JSON
    } catch (error) {
        console.error("Error al cargar los productos:", error);
        return [];
    }
};
