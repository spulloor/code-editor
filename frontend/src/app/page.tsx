'use client';
import Head from "next/head";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import Editor from "@monaco-editor/react";
import axios from "axios";
import Navbar from "@/components/Navbar";
import CodeEditor from "@/components/ui/CodeEditor";

export default function Home() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);
  const router = useRouter();

  const previousFileName = '';

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
      fetchUser(storedToken);
    }
  }, []);

  const fetchUser = async (authToken) => {
    try {
      const response = await axios.get("http://localhost:8000/users/me", {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user data", error);
      setError("Failed to fetch user data. Please log in again.");
      localStorage.removeItem("token");
      setToken(null);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    router.push("/");
  };


  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <Head>
        <title>Collaborative Code Editor</title>
      </Head>
      <Navbar onLogout={handleLogout} userId={user ? user.id : null} />
      <div className="p-6 bg-white rounded-xl shadow-md w-full max-w-3xl text-center">
        <h1 className="text-2xl font-bold">Welcome to the Code Editor</h1>
        <p className="text-gray-600 mt-2">Real-time collaboration powered by AI</p>
        {error && <p className="text-red-500">{error}</p>}
        {!user ? (
          <div className="flex gap-4 justify-center mt-4">
            <Button onClick={() => router.push("/login")}>Login</Button>
            <Button onClick={() => router.push("/signup")}>Signup</Button>
          </div>
        ) : (
          <div>
            <p className="text-green-600">Logged in as {user.email}</p>
            <Button className="mt-2" onClick={handleLogout}>Logout</Button>
          </div>
        )}
      </div>

      <CodeEditor 
        user={user}
        code=""
        language=""
        fileName=""
        description=""
        fileId=""
         />
      
    </div>
  );
}
