"use client";
import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { fetchProducts } from "@/app/pages/api/products"; //

export default function DashboardCharts() {
    const [data, setData] = useState([]); // Datos originales
    const [filteredData, setFilteredData] = useState([]); // Datos filtrados
    const [brands, setBrands] = useState([]); // Lista de marcas disponibles
    const [selectedBrand, setSelectedBrand] = useState(""); // Marca seleccionada

    useEffect(() => {
        async function loadChartData() {
            const products = await fetchProducts();

            // Agrupar productos por marca y contar cantidades y stock total
            const brandCounts = products.reduce((acc, product) => {
                if (!acc[product.brand]) {
                    acc[product.brand] = { quantity: 0, stock: 0 };
                }
                acc[product.brand].quantity += 1;
                acc[product.brand].stock += product.stock;
                return acc;
            }, {});

            // Convertir datos en formato para Recharts
            const chartData = Object.keys(brandCounts).map((brand) => ({
                brand,
                quantity: brandCounts[brand].quantity,
                stock: brandCounts[brand].stock,
            }));

            setData(chartData);
            setFilteredData(chartData);
            setBrands(Object.keys(brandCounts));
        }

        loadChartData();
    }, []);

    // Filtrar por marca seleccionada
    useEffect(() => {
        if (selectedBrand) {
            setFilteredData(data.filter((item) => item.brand === selectedBrand));
        } else {
            setFilteredData(data);
        }
    }, [selectedBrand, data]);

    return (
        <div className="w-full max-w-4xl bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Product & Stock by Brand</h2>


            <select
                className="mb-4 p-2 border rounded"
                value={selectedBrand}
                onChange={(e) => setSelectedBrand(e.target.value)}
            >
                <option value="">All Brands</option>
                {brands.map((brand) => (
                    <option key={brand} value={brand}>
                        {brand}
                    </option>
                ))}
            </select>

            {/* Gráfico */}
            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={filteredData} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
                    <XAxis dataKey="brand" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="quantity" fill="#8884d8" name="Product Quantity" />
                    <Bar dataKey="stock" fill="#82ca9d" name="Total Stock" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
