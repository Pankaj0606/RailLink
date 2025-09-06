// /frontend/src/app/page.tsx

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import SearchForm from "./components/SearchForm";

export default function Page() {
  return (
    <main className="min-h-screen flex flex-col items-center bg-gray-100">
      <Navbar />
      <section className="w-full max-w-lg text-center py-10 px-4">
        <h1 className="text-4xl font-bold text-gray-800">Welcome to RailLink</h1>
        <p className="mt-4 text-gray-600">Find direct and connecting train journeys with ease.</p>
        <SearchForm />
      </section>
      <Footer />
    </main>
  );
}