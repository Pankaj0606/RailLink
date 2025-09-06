// /frontend/src/app/components/SearchForm.tsx

"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Station {
  station_code: string;
  station_name: string;
}

const AutocompleteInput = ({
  value, onChange, onSuggestionClick, placeholder, stations, isRequired,
}: {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSuggestionClick: (station: Station) => void;
  placeholder: string;
  stations: Station[];
  isRequired: boolean; // NEW PROP
}) => {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const filteredStations = value
    ? stations.filter(s => s.station_name.toLowerCase().includes(value.toLowerCase()) || s.station_code.toLowerCase().includes(value.toLowerCase()))
    : [];

  return (
    <div className="relative w-full">
      <input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        className="p-2 border rounded text-black bg-white focus:outline-none w-full"
        required={isRequired} // Use the new prop
      />
      {showSuggestions && filteredStations.length > 0 && (
        <ul className="absolute z-20 w-full bg-white border rounded-md mt-1 max-h-60 overflow-y-auto shadow-lg">
          {filteredStations.slice(0, 100).map((station) => (
            <li key={station.station_code} onMouseDown={() => onSuggestionClick(station)} className="p-2 text-black cursor-pointer hover:bg-gray-200">
              {station.station_name} ({station.station_code})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default function SearchForm() {
  const [sourceName, setSourceName] = useState("");
  const [sourceCode, setSourceCode] = useState("");
  const [destName, setDestName] = useState("");
  const [destCode, setDestCode] = useState("");
  const [interName, setInterName] = useState("");
  const [interCode, setInterCode] = useState("");
  const [date, setDate] = useState("");
  const [stations, setStations] = useState<Station[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchStations = async () => {
      try {
        const response = await fetch("http://localhost:8000/stations");
        const data = await response.json();
        setStations(data.stations || []);
      } catch (error) { console.error("Failed to fetch stations:", error); }
    };
    fetchStations();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceCode || !destCode || !date) {
      alert("Please select valid Source and Destination stations from the list!");
      return;
    }
    const params = new URLSearchParams({ source: sourceCode, destination: destCode, date });
    if (interCode) {
      params.append("intermediate", interCode);
    }
    router.push(`/search?${params.toString()}`);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md flex flex-col gap-4 mt-6">
      <AutocompleteInput
        value={sourceName} onChange={(e) => setSourceName(e.target.value)}
        onSuggestionClick={(s) => { setSourceName(s.station_name); setSourceCode(s.station_code); }}
        placeholder="Source Station" stations={stations} isRequired={true}
      />
      <AutocompleteInput
        value={destName} onChange={(e) => setDestName(e.target.value)}
        onSuggestionClick={(s) => { setDestName(s.station_name); setDestCode(s.station_code); }}
        placeholder="Destination Station" stations={stations} isRequired={true}
      />
      <AutocompleteInput
        value={interName} onChange={(e) => setInterName(e.target.value)}
        onSuggestionClick={(s) => { setInterName(s.station_name); setInterCode(s.station_code); }}
        placeholder="Via Station (Optional)" stations={stations} isRequired={false} // THIS IS NOW OPTIONAL
      />
      <input
        type="date" value={date} onChange={(e) => setDate(e.target.value)}
        className="p-2 border rounded w-full text-black bg-white focus:outline-none" required
      />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
        Search Trains
      </button>
    </form>
  );
}