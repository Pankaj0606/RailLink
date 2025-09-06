export async function GET() {
    try {
      const response = await fetch("http://127.0.0.1:8000/trains"); // FastAPI URL
      if (!response.ok) throw new Error("Failed to fetch train data");
  
      const trains = await response.json();
      return new Response(JSON.stringify(trains), { status: 200 });
    } catch (error) {
      return new Response(JSON.stringify({ error: "Error fetching trains" }), {
        status: 500,
      });
    }
  }
  