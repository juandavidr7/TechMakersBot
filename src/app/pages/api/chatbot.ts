export const sendChatMessage = async (query: string) => {
    try {
        const response = await fetch("http://127.0.0.1:8050/chatbot/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) throw new Error("Error en la API");

        const data = await response.json();
        return data.response || "No se recibió respuesta del servidor";
    } catch (error) {
        console.error("Error al enviar el mensaje:", error);
        return "Hubo un error al conectar con el chatbot.";
    }
};
