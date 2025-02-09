'use client';
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";
import { useSearchParams } from "next/navigation";

export default function Editor() {
    
    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("");
    const [fileName, setfileName] = useState("");
    const [description, setdescription] = useState("");
    const [fileId, setfileId] = useState("");
    const [ownerId, setownerId] = useState("");
    const [loading, setloading] = useState(true);
    const [token, setToken] = useState(null);

  const router = useRouter();

  useEffect(() => {

    if (router.isReady) {
      console.log(router);
      console.log(`THIS IS THE ID: ${router.query.fileid}`);
      setfileId(router.query.fileid);


      const fetchFileDetails = async () => {
        const token = localStorage.getItem("token");
        setToken(token);
        if (!token) {
          router.push("/login");
          return;
        }
        try {
          console.log(`http://localhost:8000/code-files/${router.query.fileid}`);
          const response = await axios.get(`http://localhost:8000/code-files/${router.query.fileid}`, {
            headers: { Authorization: `Bearer ${token}` },
          });

            setCode(response.data.content);
            setLanguage(response.data?.language);
            setfileName(response.data.name);
            setdescription(response.data?.description);
            setownerId(response.data.owner_id);

        } catch (error) {
          console.error("Error fetching files", error);
          if (error?.status === 401) {
            router.push("/login");
          }
        } finally {
          setLoading(false);
        }
      };
      fetchFileDetails();
      fetchUser()
    }
  }, [router.isReady, router.query]);


  const fetchUser = async () => {
    try {
      const response = await axios.get("http://localhost:8000/users/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user data", error);
      setError("Failed to fetch user data. Please log in again.");
      localStorage.removeItem("token");
      setToken(null);
    }
  };

  return (
    <>
        {loading ? "Loading..." : (

            <CodeEditor 
            user={user}
            code={code}
            language={language}
            fileName={fileName}
            description={description}
            fileId={fileId}
            />
        )}
    </>
  );
}
