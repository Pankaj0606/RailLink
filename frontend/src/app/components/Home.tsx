// /frontend/src/app/components/Home.tsx

"use client";

import Navbar from "./Navbar";
import Footer from "./Footer";
import SearchForm from "./SearchForm";

export default function Home() {
  return (
    // Add flex flex-col to make this a vertical flex container
    <main className="min-h-screen flex flex-col items-center bg-gray-100">
      <Navbar />
      {/* Add flex-grow to make this section expand and fill available space */}
      <section className="w-full max-w-lg text-center py-10 px-4 flex-grow">
        <h1 className="text-4xl font-bold text-gray-800">Welcome to RailLink</h1>
        <p className="mt-4 text-gray-600">Find direct and connecting train journeys with ease.</p>
        <SearchForm />
      </section>
      <Footer />
    </main>
  );
}