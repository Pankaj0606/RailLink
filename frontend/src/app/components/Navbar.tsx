// /frontend/src/app/components/Navbar.tsx

"use client"; // This component now needs client-side interactivity for the Link component

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const linkStyles = "hover:underline";
  const activeLinkStyles = "underline font-bold";

  return (
    <nav className="w-full bg-blue-600 text-white py-4 px-6 shadow-md">
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold">
          RailLink
        </Link>
        <ul className="flex space-x-6">
          <li>
            <Link href="/" className={`${linkStyles} ${pathname === "/" ? activeLinkStyles : ""}`}>
              Home
            </Link>
          </li>
          <li>
            <Link href="/trains" className={`${linkStyles} ${pathname === "/trains" ? activeLinkStyles : ""}`}>
              Trains
            </Link>
          </li>
          <li>
            <Link href="/about" className={`${linkStyles} ${pathname === "/about" ? activeLinkStyles : ""}`}>
              About
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}