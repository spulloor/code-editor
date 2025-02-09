import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function Navbar({ onLogout, userId }) {
  const router = useRouter();

  return (
    <nav className="bg-blue-600 p-4 text-black flex justify-between items-center">
      <div className="flex gap-4">
        <Button variant="outline" className="text-black border-black" onClick={() => router.push(`/dashboard/${userId}`)}>
          Dashboard
        </Button>
        <Button variant="outline" className="text-black border-black" onClick={() => router.push("/")}>
          New File
        </Button>
        <Button variant="destructive" onClick={onLogout}>
          Logout
        </Button>
      </div>
    </nav>
  );
}
