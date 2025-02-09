import SignupForm from "@/components/auth/SignupForm";
import { useState } from "react";

export default function SignupPage() {
    const [error, setError] = useState(null);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {error && <p className="text-red-500">{error}</p>}
      <SignupForm setError={setError} />
    </div>
  );
}
