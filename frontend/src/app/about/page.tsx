// /frontend/src/app/about/page.tsx

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function AboutPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="bg-white shadow-lg rounded-lg p-8 max-w-2xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">About RailLink</h1>
          <p className="text-gray-600 mb-4">
            RailLink is a comprehensive train schedule and journey planning application designed to
            make railway travel simple and efficient. Our goal is to provide users with a powerful
            tool to find not only direct trains but also the best connecting journeys between any
            two stations.
          </p>
          <h2 className="text-2xl font-bold text-gray-700 mt-6 mb-3">Core Features</h2>
          <ul className="list-disc list-inside text-gray-600 space-y-2">
            <li><strong>Direct & Connecting Journeys:</strong> Find all possible routes, including multi-leg journeys with changeovers.</li>
            <li><strong>Advanced Search:</strong> Specify an intermediate station to customize your route.</li>
            <li><strong>Intelligent Sorting:</strong> Sort results by the shortest total journey time or the quickest connection.</li>
            <li><strong>Station Autocomplete:</strong> Easily find stations by name or code without needing to memorize them.</li>
            <li><strong>Detailed Information:</strong> View total travel time, waiting time at connections, and the full route of each train.</li>
          </ul>
           <p className="text-gray-600 mt-6">
            This project is built with a modern tech stack, featuring a FastAPI backend for high-performance data processing and a Next.js frontend for a fast, responsive user experience.
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
}