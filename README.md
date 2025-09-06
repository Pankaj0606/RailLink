# RailLink 🚄

RailLink is a dynamic, full-stack web application designed to be a comprehensive train journey planner. It empowers users to find not only direct trains but also the most efficient multi-leg connecting routes between any two stations in the dataset. Built with a modern tech stack, it features a high-performance Python backend using FastAPI and a responsive, feature-rich frontend built with Next.js and React.

---

## ✨ Core Features

*   **Direct & Connecting Journey Engine:**
    *   Finds all possible direct train journeys based on the user's selected source, destination, and date.
    *   Intelligently discovers multi-leg journeys, calculating the optimal path from A to B via an intermediate station C.

*   **Advanced & User-Friendly Search:**
    *   **"Via" Station Search:** Allows users to specify a preferred intermediate station, filtering results to show only routes that pass through or connect at that specific location.
    *   **Station Autocomplete:** A user-friendly search form with station name and code autocomplete to prevent errors and simplify input.

*   **Intelligent Sorting & Filtering:**
    *   **Shortest Journey Time:** Users can sort complex journey results by the shortest total travel time, including layovers.
    *   **Shortest Waiting Time:** Users can also sort connecting journeys by the quickest connection time between trains.

*   **Detailed Information at a Glance:**
    *   Each search result displays crucial data, including total travel duration and the train's full origin-to-destination route for context.
    *   Connecting journey cards prominently display the waiting time at the intermediate station.

*   **Dynamic Train Schedules:**
    *   Every train card in the application (on both search results and the "All Trains" page) is clickable.
    *   Clicking a train navigates to a dedicated, beautifully styled page showing its complete schedule, including all stops, arrival/departure times, day of the week, and distance.

*   **Clean, Multi-Page Interface:**
    *   A fully navigable site built with Next.js App Router, featuring dedicated pages for searching (Home), viewing all available trains, and learning about the project.

---

## 🛠️ Tech Stack

*   **Backend:** **Python** with **FastAPI** (for high-performance, asynchronous API endpoints).
*   **Database:** **PostgreSQL** (for storing and performing complex relational queries on train schedule data).
*   **Frontend:** **Next.js** (React Framework), **TypeScript**, **Tailwind CSS** (for a modern, responsive, and type-safe user interface).
*   **Data Handling:** **Pandas** and **SQLAlchemy** for initial data loading and database setup.

---

## 🚀 Getting Started

To run this project locally, you will need to set up the PostgreSQL database, the Python backend, and the Next.js frontend.

### Prerequisites

*   Python 3.10+
*   Node.js (v18 or higher recommended)
*   PostgreSQL installed and running
*   A code editor (e.g., VS Code)

### Installation & Setup

1.  **Clone the Repository:**
    ```sh
    git clone https://github.com/your-username/RailLink.git
    cd RailLink
    ```

2.  **Set Up the Backend & Database:**
    ```sh
    # Navigate into the backend directory
    cd backend

    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install Python dependencies
    pip install fastapi "uvicorn[standard]" psycopg2-binary pandas sqlalchemy

    # IMPORTANT: Configure your PostgreSQL connection details in `database.py`
    # (e.g., DB_USER, DB_NAME).

    # Run the one-time script to create the database and load the dataset.csv
    python setup_database.py
    ```

3.  **Set Up the Frontend:**
    ```sh
    # Navigate into the frontend directory from the root
    cd frontend

    # Install Node.js dependencies
    npm install
    ```

### Running the Application

You will need two separate terminal windows open.

**Terminal 1 (Backend):**
```sh
# Make sure you are in the backend directory with the venv activated
cd backend
source venv/bin/activate

# Run the backend server
uvicorn main:app --reload 
```
The backend will now be running at http://localhost:8000.

**Terminal 2 (Frontend):**
```sh
# Make sure you are in the frontend directory
cd frontend

# Run the frontend development server
npm run dev
```
Access the application in your browser at http://localhost:3000.


## 📁 Project Structure
The project is a monorepo containing two main parts:
```sh
RailLink/
|
|-- backend/                # FastAPI (Python) backend server
|   |-- venv/               # Virtual environment (ignored by Git)
|   |-- database.py         # PostgreSQL connection logic
|   |-- dataset.csv         # The raw train schedule data
|   |-- main.py             # Main server file with all API endpoints
|   |-- setup_database.py   # Script to initialize the database
|
|-- frontend/               # Next.js + React frontend application
|   |-- public/             # Static assets (SVGs, etc.)
|   |-- src/app/
|   |   |-- components/     # Reusable React components (Navbar, SearchForm, etc.)
|   |   |-- search/         # The search results page
|   |   |-- trains/         # "All Trains" list page & dynamic [train_no] details page
|   |   |-- about/          # The "About" page
|   |   |-- page.tsx        # (Note: your setup uses components which are then rendered)
|   |-- package.json        # Project dependencies and scripts
|   |-- tailwind.config.js  # Tailwind CSS configuration
|
|-- .gitignore              # Specifies files for Git to ignore
|-- README.md               # This file
```