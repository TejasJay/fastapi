import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import UserApi from "../api/UserApi.jsx";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await UserApi.signup(username, password);
      navigate("/login", { state: { signupSuccess: true } });
    } catch (err) {
      setError(`Signup failed. Try a different username. ${err}`);
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Signup</h1>
      <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: "0 auto" }}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <div className="modal-actions">
          <button type="submit">Signup</button>
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <p>
          Already have an account? <a href="/login">Login</a>
        </p>
      </form>
    </div>
  );
}

export default Signup;