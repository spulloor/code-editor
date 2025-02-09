'use client';
import Head from "next/head";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import Editor from "@monaco-editor/react";
import axios from "axios";
import Navbar from "@/components/Navbar";

export default function Home({ user, code, language, fileName, description, fileId }) {
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);
  const router = useRouter();

  const previousFileName = '';

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const handleSaveCode = async () => {
    if (!token) return;

    try {

      if (fileId === '') {
        const res = await axios.post(
          "http://localhost:8000/code-files/",
          { name: fileName, language, description, content: code, owner_id: user.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
  
        setFileId(res.data.id);
        alert("Code saved successfully");
      } else {
        const res = await axios.put(
          `http://localhost:8000/code-files/${fileId}`,
          { name: fileName, language, description, content: code, owner_id: user.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(`${fileName} updated successfully`);
      }

      
    } catch (error) {
      console.error("Error saving code", error);
      setError("Failed to save code. Try again later.");
    }
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleNewFile = () => {
    setFileId('');
    setFileName("");
    setDescription("");
    setCode("// Start coding...");
    setLanguage("javascript");
  };

  return (
    <>
      {user && (
        <div className="mt-6 w-full max-w-5xl">
          {/* File Details Inputs */}
          <div className="flex flex-col gap-3 mb-4">
            <input
              type="text"
              placeholder="Enter file name"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              className="p-2 border rounded-md w-full"
            />
            <textarea
              placeholder="Enter file description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="p-2 border rounded-md w-full"
            />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="p-2 border rounded-md"
            >
              <option value="c">C</option>
              <option value="javascript">JavaScript</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
          </div>

          {/* Monaco Editor */}
          <Editor 
            height="500px"
            language={language}
            value={code}
            onChange={(value) => setCode(value)}
            className="border rounded-lg shadow-sm"
          />

          <div className="flex justify-between mt-4">
            <Button className="bg-gray-500 text-white" onClick={handleNewFile}>
              New File
            </Button>
            <Button className="bg-blue-500 text-white" onClick={handleSaveCode}>
              Save Code
            </Button>
          </div>
        </div>

      )}
      </>
  );
}
