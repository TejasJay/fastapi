import api from "./ApiService.jsx";

const UserApi = {
  login: (username, password) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    return api.post("/api/v1/users/token", formData);
  },
  getSession: (token) =>
    api.get("/api/v1/users/my_session/", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  signup: (username, password) =>
    api.post("/api/v1/users/", { username, password }),
};

export default UserApi;