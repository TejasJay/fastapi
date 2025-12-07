import api from "./ApiService.jsx";

const getAuthHeader = () => {
    const token = sessionStorage.getItem("jwt_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
}

const ProductApi = {
    fetchAllProducts: () => api.get("/api/v1/products", {headers: getAuthHeader()}),
    createProduct: (productData) => api.post("/api/v1/products", productData, {headers: getAuthHeader()}),
};

export default ProductApi;