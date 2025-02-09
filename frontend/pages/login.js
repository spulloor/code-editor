import LoginForm from "@/components/auth/LoginForm";
import { useState } from "react";

export default function LoginPage() {
    const [error, setError] = useState(null);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {error && <p className="text-red-500">{error}</p>}
      <LoginForm setError={setError} />
    </div>
  );
}
