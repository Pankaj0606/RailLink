// /frontend/src/app/search/page.tsx

"use client";

import { Suspense } from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import TrainList from "../components/TrainList";
import { useSearchParams } from "next/navigation";

function SearchHeader() {
    // ... (This component is unchanged)
    const searchParams = useSearchParams();
    const source = searchParams.get('source');
    const destination = searchParams.get('destination');
    const date = searchParams.get('date');

    if (!source || !destination || !date) {
        return <p className="text-center text-red-500">Search parameters are missing.</p>;
    }
    
    const displayDate = new Date(date + 'T00:00:00Z').toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC'
    });

    return (
        <div className="w-full max-w-4xl bg-white p-3 rounded-lg shadow-md sticky top-4 z-10">
            <p className="text-center text-gray-800">
                Showing results for: <strong>{source}</strong> → <strong>{destination}</strong> on <strong>{displayDate}</strong>
            </p>
        </div>
    );
}

export default function SearchPage() {
    return (
        <Suspense fallback={<div className="text-center p-8">Loading search...</div>}>
            <main className="min-h-screen flex flex-col items-center bg-gray-100">
                <Navbar />
                {/* Add flex-grow here */}
                <section className="w-full max-w-4xl text-center py-6 flex flex-col items-center gap-6 flex-grow">
                    <SearchHeader />
                    <TrainList />
                </section>
                <Footer />
            </main>
        </Suspense>
    );
}