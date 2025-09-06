// /frontend/src/app/trains/[train_no]/page.tsx

"use client";

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from 'next/link';
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

interface ScheduleStop {
  station_name: string;
  arrival_time: string;
  departure_time: string;
  day_of_arrival: number;
  distance: number;
}

interface TrainDetails {
  train_name: string;
  source_station_name: string;
  destination_station_name: string;
  schedule: ScheduleStop[];
}

const dayOfWeekMap: { [key: number]: string } = {
  1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'
};

export default function TrainDetailPage() {
  const params = useParams();
  const train_no = params.train_no as string;

  const [details, setDetails] = useState<TrainDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!train_no) return;
    const fetchDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:8000/trains/${train_no}`);
        if (!response.ok) {
          throw new Error("Train not found or server error.");
        }
        const data = await response.json();
        setDetails(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred.");
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [train_no]);

  const formatTime = (timeStr: string) => {
    if (!timeStr || timeStr.includes('00:00:00')) return "--:--";
    return new Date(timeStr).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Link href="/search" className="text-blue-600 hover:underline mb-6 inline-block">
            &larr; Back to Search Results
          </Link>

          {loading && <p className="text-center">Loading train details...</p>}
          {error && <p className="text-center text-red-500">Error: {error}</p>}

          {details && (
            <div className="bg-white shadow-2xl rounded-lg overflow-hidden">
              <div className="bg-blue-600 text-white p-6">
                <h1 className="text-3xl font-bold">{details.train_name} ({train_no})</h1>
                <p className="text-blue-200 mt-1">
                  {details.source_station_name} to {details.destination_station_name}
                </p>
              </div>

              <div className="p-2 md:p-4">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Station</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Arrival</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Departure</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Day</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Distance (km)</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {details.schedule.map((stop, index) => (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{stop.station_name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatTime(stop.arrival_time)}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatTime(stop.departure_time)}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{dayOfWeekMap[stop.day_of_arrival]}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stop.distance}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}