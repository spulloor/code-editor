import { useState } from "react";
import axios from "axios";
import "@/app/globals.css";

export default function SignupForm({ setError }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const validateForm = () => {
    if (!username || !email || !password) {
      setError("All fields are required.");
      return false;
    }
    if (username.length < 3) {
      setError("Username must be at least 3 characters long.");
      return false;
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      setError("Invalid email format.");
      return false;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return false;
    }
    return true;
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    if (!validateForm()) return;

    try {
      await axios.post("http://localhost:8000/users/register", {
        username,
        email,
        password,
      });
      setError(null);
      window.location.href = "/login";
    } catch (error) {
      console.error("Signup failed", error);
      setError("Signup failed. Try again.");
    }
  };

  return (
    <form onSubmit={handleSignup} className="bg-white p-6 rounded shadow-md w-80">
      <h2 className="text-xl font-bold mb-4">Signup</h2>
      <input
        type="text"
        placeholder="Username"
        className="w-full p-2 border rounded mb-2"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        className="w-full p-2 border rounded mb-2"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="w-full p-2 border rounded mb-2"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit" className="w-full bg-green-500 text-white p-2 rounded">
        Signup
      </button>
    </form>
  );
}
