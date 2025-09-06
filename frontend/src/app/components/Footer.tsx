// /frontend/src/app/components/Footer.tsx

export default function Footer() {
  return (
    <footer className="w-full bg-gray-800 text-white py-4 text-center mt-auto">
      <p>&copy; {new Date().getFullYear()} RailLink. All rights reserved.</p>
    </footer>
  );
}