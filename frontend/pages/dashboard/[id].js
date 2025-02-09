'use client';
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";
import { useSearchParams } from "next/navigation";

export default function Dashboard() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {

    if (router.isReady) {
      console.log(router);
      console.log(`THIS IS THE ID: ${router.query.id}`);


      const fetchFiles = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/login");
          return;
        }
        try {
          console.log(`http://localhost:8000/code-files/user/${router.query.id}`);
          const response = await axios.get(`http://localhost:8000/code-files/user/${router.query.id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          console.log(response.data);
          setFiles(response.data);
        } catch (error) {
          console.error("Error fetching files", error);
          if (error?.status === 401) {
            router.push("/login");
          }
        } finally {
          setLoading(false);
        }
      };
      fetchFiles();
    }
  }, [router.isReady, router.query]);

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Your Files</h1>
      {loading ? (
        <p>Loading...</p>
      ) : files.length === 0 ? (
        <p>No files found. Create a new one!</p>
      ) : (
        <ul className="bg-white p-4 rounded-lg shadow-md">
          {files.map((file) => (
            <li key={file.id} className="flex justify-between items-center border-b p-2">
              <span>{file.name} ({file.language})</span>
              <Button onClick={() => router.push(`/editor/${file.id}`)}>Open</Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
