// /frontend/src/app/components/TrainList.tsx

"use client";

import React, { useState, useEffect, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import Link from 'next/link';

// --- Interfaces ---
interface DirectTrain {
  train_no: string; user_source_station_name: string; user_dest_station_name: string;
  user_departure_time: string; user_arrival_time: string;
  train_origin_name: string; train_destination_name: string;
  totalDurationMinutes?: number;
}
interface MultiLegJourney {
    train1_no: string; leg1_source_name: string; leg1_dest_name: string;
    train1_origin_name: string; train1_dest_name: string;
    t1_departure: string; t1_arrival: string;
    train2_no: string; leg2_source_name: string; leg2_dest_name: string;
    train2_origin_name: string; train2_dest_name: string;
    t2_departure: string; t2_arrival: string;
    waitingTimeMinutes?: number;
    totalDurationMinutes?: number;
}

const DIRECT_PER_PAGE = 10;
const MULTILEG_PER_PAGE = 5;
type SortMode = 'default' | 'shortestWait' | 'shortestJourney';

export default function TrainList() {
    const searchParams = useSearchParams();
    const source = searchParams.get('source');
    const destination = searchParams.get('destination');
    const date = searchParams.get('date');
    const intermediate = searchParams.get('intermediate');

    const [directTrains, setDirectTrains] = useState<DirectTrain[]>([]);
    const [multilegJourneys, setMultilegJourneys] = useState<MultiLegJourney[]>([]);
    const [viewMode, setViewMode] = useState<'direct' | 'multileg'>('direct');
    const [currentPage, setCurrentPage] = useState(1);
    const [sortMode, setSortMode] = useState<SortMode>('default');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const getDurationInMinutes = (start: Date, end: Date): number => {
        const diffMs = end.getTime() - start.getTime();
        return Math.floor(diffMs / (1000 * 60));
    };
    
    useEffect(() => {
        if (!source || !destination || !date) return;
        const fetchTrains = async () => {
          setLoading(true);
          setError(null);
          setViewMode(intermediate ? 'multileg' : 'direct');
          try {
            const params = new URLSearchParams({ source, destination, date });
            if (intermediate) {
                params.append("intermediate", intermediate);
            }
            const url = `http://localhost:8000/trains/search?${params.toString()}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Failed to fetch train data.");
            const data = await response.json();
            
            const directWithDuration = (data.direct_trains || []).map((train: DirectTrain) => ({
                ...train,
                totalDurationMinutes: getDurationInMinutes(new Date(train.user_departure_time), new Date(train.user_arrival_time)),
            }));
            setDirectTrains(directWithDuration);

            const journeysWithCalcs = (data.multileg_journeys || []).map((journey: MultiLegJourney) => {
                const leg1Dep = new Date(journey.t1_departure);
                const leg1Arr = new Date(journey.t1_arrival);
                const leg2Dep = new Date(journey.t2_departure);
                const leg2Arr = new Date(journey.t2_arrival);
                return { 
                    ...journey, 
                    waitingTimeMinutes: getDurationInMinutes(leg1Arr, leg2Dep),
                    totalDurationMinutes: getDurationInMinutes(leg1Dep, leg2Arr)
                };
            });
            setMultilegJourneys(journeysWithCalcs);
          } catch (err) {
            setError(err instanceof Error ? err.message : "An unknown error occurred.");
          } finally {
            setLoading(false);
          }
        };
        fetchTrains();
    }, [source, destination, date, intermediate]);

    const formatDateTime = (dateStr: string): string => {
        if (!dateStr) return "N/A";
        return new Date(dateStr).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true });
    };

    const formatDuration = (startStr: string, endStr: string): string => {
        if (!startStr || !endStr) return "";
        const start = new Date(startStr);
        const end = new Date(endStr);
        const diffMs = end.getTime() - start.getTime();
        if (diffMs < 0) return "Invalid";
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        return `${diffHours}h ${diffMinutes}m`;
    };
    
    const handleViewChange = (mode: 'direct' | 'multileg') => {
        setViewMode(mode);
        setCurrentPage(1);
        setSortMode('default');
    };

    const sortedData = useMemo(() => {
        const dataToSort = viewMode === 'direct' ? [...directTrains] : [...multilegJourneys];
        const validData = dataToSort.filter(j => (j.totalDurationMinutes ?? -1) >= 0);
        if (sortMode === 'shortestJourney') {
            validData.sort((a, b) => (a.totalDurationMinutes ?? Infinity) - (b.totalDurationMinutes ?? Infinity));
        } else if (sortMode === 'shortestWait' && viewMode === 'multileg') {
            (validData as MultiLegJourney[]).sort((a, b) => (a.waitingTimeMinutes ?? Infinity) - (b.waitingTimeMinutes ?? Infinity));
        }
        return validData;
    }, [viewMode, directTrains, multilegJourneys, sortMode]);

    const totalPages = Math.ceil(sortedData.length / (viewMode === 'direct' ? DIRECT_PER_PAGE : MULTILEG_PER_PAGE));
    const currentData = sortedData.slice((currentPage - 1) * (viewMode === 'direct' ? DIRECT_PER_PAGE : MULTILEG_PER_PAGE), currentPage * (viewMode === 'direct' ? DIRECT_PER_PAGE : MULTILEG_PER_PAGE));

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

    if (loading) return <p className="text-center text-gray-700 py-8">Searching for trains...</p>;
    if (error) return <p className="text-center text-red-500 py-8">Error: {error.toString()}</p>;

    return (
        <div className="w-full">
            <div className="flex justify-center gap-4 mb-6">
                {!intermediate && viewMode === 'multileg' && (
                    <button onClick={() => handleViewChange('direct')} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                        Show Direct Trains ({directTrains.length})
                    </button>
                )}
                {!intermediate && viewMode === 'direct' && (
                    <button onClick={() => handleViewChange('multileg')} className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                        Check Connecting Trains ({multilegJourneys.length})
                    </button>
                )}
            </div>
            {(sortedData.length > 0) && (
                <div className="bg-white p-3 rounded-md shadow mb-6 flex items-center justify-center gap-4">
                    <label htmlFor="sort-select" className="font-semibold text-gray-700">Sort results by:</label>
                    <select id="sort-select" value={sortMode} onChange={(e) => { setSortMode(e.target.value as SortMode); setCurrentPage(1); }} className="p-2 border rounded-md">
                        <option value="default">Default</option>
                        <option value="shortestJourney">Shortest Journey Time</option>
                        <option value="shortestWait" disabled={viewMode === 'direct'}> Shortest Waiting Time </option>
                    </select>
                </div>
            )}
            {viewMode === 'direct' ? (
                <div>
                    {currentData.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {(currentData as DirectTrain[]).map((train, index) => (
                                <Link href={`/trains/${train.train_no}`} key={index} className="block hover:scale-105 transition-transform duration-200">
                                    <div className="bg-white shadow-lg rounded-lg p-4 border flex flex-col justify-between h-full">
                                        <div>
                                            <div className="flex justify-between items-center mb-3">
                                                <h3 className="text-lg font-bold text-blue-600">Train No: {train.train_no}</h3>
                                                <span className="text-sm font-semibold text-gray-700 bg-gray-200 px-2 py-1 rounded"> {formatDuration(train.user_departure_time, train.user_arrival_time)} </span>
                                            </div>
                                            <div className="text-center mb-3">
                                                <p className="text-xl font-bold">{train.user_source_station_name}</p>
                                                <p className="text-gray-500 text-lg my-1">↓</p>
                                                <p className="text-xl font-bold">{train.user_dest_station_name}</p>
                                            </div>
                                            <div className="space-y-2 text-sm">
                                                <p><strong>Departure:</strong> {formatDateTime(train.user_departure_time)}</p>
                                                <p><strong>Arrival:</strong> {formatDateTime(train.user_arrival_time)}</p>
                                            </div>
                                        </div>
                                        <div className="mt-4 pt-3 border-t text-xs text-gray-500 bg-slate-50 p-2 rounded-md">
                                            <p><strong>Full Route:</strong> {train.train_origin_name} to {train.train_destination_name}</p>
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    ) : <p className="text-center py-8">No direct trains found.</p>}
                </div>
            ) : (
                <div>
                    {currentData.length > 0 ? (
                         <div className="space-y-6">
                            {(currentData as MultiLegJourney[]).map((journey, index) => (
                                <div key={index} className="bg-gray-100 shadow-inner rounded-lg p-4 border">
                                    <div className="flex justify-between items-center mb-4 pb-3 border-b">
                                        <h3 className="text-lg font-bold text-gray-800">Connecting Journey</h3>
                                        <span className="text-base font-bold text-indigo-600 bg-indigo-100 px-3 py-1 rounded-full"> Total: {formatDuration(journey.t1_departure, journey.t2_arrival)} </span>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] items-center gap-4">
                                        <Link href={`/trains/${journey.train1_no}`} className="block hover:shadow-xl transition-shadow duration-200">
                                            <div className="bg-white shadow rounded p-3 h-full">
                                                <div className="flex justify-between items-center mb-2">
                                                    <h4 className="font-bold text-green-700">Leg 1: Train {journey.train1_no}</h4>
                                                    <span className="text-xs font-semibold bg-gray-200 px-2 py-1 rounded">{formatDuration(journey.t1_departure, journey.t1_arrival)}</span>
                                                </div>
                                                <p className="font-semibold">{journey.leg1_source_name} → {journey.leg1_dest_name}</p>
                                                <div className="text-xs mt-2 space-y-1">
                                                    <p><strong>Depart:</strong> {formatDateTime(journey.t1_departure)}</p>
                                                    <p><strong>Arrive:</strong> {formatDateTime(journey.t1_arrival)}</p>
                                                </div>
                                            </div>
                                        </Link>
                                        <div className="text-center font-bold text-blue-600">
                                            <p className="text-2xl">➔</p>
                                            <p className="text-sm">Change</p>
                                            <span className="text-xs font-normal text-red-600 bg-red-100 px-2 py-1 rounded-full mt-1 inline-block"> Wait: {formatDuration(journey.t1_arrival, journey.t2_departure)} </span>
                                        </div>
                                        <Link href={`/trains/${journey.train2_no}`} className="block hover:shadow-xl transition-shadow duration-200">
                                            <div className="bg-white shadow rounded p-3 h-full">
                                                <div className="flex justify-between items-center mb-2">
                                                    <h4 className="font-bold text-green-700">Leg 2: Train {journey.train2_no}</h4>
                                                    <span className="text-xs font-semibold bg-gray-200 px-2 py-1 rounded">{formatDuration(journey.t2_departure, journey.t2_arrival)}</span>
                                                </div>
                                                <p className="font-semibold">{journey.leg2_source_name} → {journey.leg2_dest_name}</p>
                                                <div className="text-xs mt-2 space-y-1">
                                                    <p><strong>Depart:</strong> {formatDateTime(journey.t2_departure)}</p>
                                                    <p><strong>Arrive:</strong> {formatDateTime(journey.t2_arrival)}</p>
                                                </div>
                                            </div>
                                        </Link>
                                    </div>
                                </div>
                            ))}
                         </div>
                    ) : <p className="text-center py-8">No connecting trains found.</p>}
                </div>
            )}
            <Pagination />
        </div>
    );
}