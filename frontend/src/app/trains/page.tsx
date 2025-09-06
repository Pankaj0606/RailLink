// /frontend/src/app/trains/page.tsx

"use client";

import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Link from "next/link"; // Import the Link component

interface TrainInfo {
  train_no: string;
  train_name: string;
  source_station_name: string;
  destination_station_name: string;
}

const TRAINS_PER_PAGE = 20;

export default function AllTrainsPage() {
  const [trains, setTrains] = useState<TrainInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchTrains = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:8000/trains/all?page=${currentPage}&limit=${TRAINS_PER_PAGE}`);
        const data = await response.json();
        setTrains(data.trains || []);
        setTotalPages(data.total_pages || 1);
      } catch (error) {
        console.error("Failed to fetch trains:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTrains();
  }, [currentPage]);

  const Pagination = () => {
    if (totalPages <= 1) return null;
    return (
        <div className="flex justify-center items-center mt-8 gap-2">
            <button onClick={() => setCurrentPage(1)} disabled={currentPage === 1} className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50">First</button>
            <button onClick={() => setCurrentPage(c => c - 1)} disabled={currentPage === 1} className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50">Prev</button>
            <span className="px-3 py-1 text-gray-700">Page {currentPage} of {totalPages}</span>
            <button onClick={() => setCurrentPage(c => c + 1)} disabled={currentPage === totalPages} className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50">Next</button>
            <button onClick={() => setCurrentPage(totalPages)} disabled={currentPage === totalPages} className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50">Last</button>
        </div>
    );
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-6">All Available Trains</h1>
        {loading ? (
          <p className="text-center">Loading trains...</p>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {trains.map((train) => (
                // --- WRAP THE CARD WITH THE LINK COMPONENT ---
                <Link 
                  href={`/trains/${train.train_no}`} 
                  key={train.train_no} 
                  className="block hover:scale-105 transition-transform duration-200"
                >
                  <div className="bg-white shadow-md rounded-lg p-4 border h-full">
                    <h2 className="text-lg font-bold text-blue-600">
                      {train.train_name} ({train.train_no})
                    </h2>
                    <p className="text-gray-700 mt-2">
                      <span className="font-semibold">From:</span> {train.source_station_name}
                    </p>
                    <p className="text-gray-700">
                      <span className="font-semibold">To:</span> {train.destination_station_name}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
            <Pagination />
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}