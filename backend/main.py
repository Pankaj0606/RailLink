# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras  # ✅ Required for DictCursor

# app = FastAPI()

# # ✅ Enable CORS for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # ✅ Function to fetch valid train numbers based on source, destination, and day
# def get_valid_trains(source, destination, day_of_departure, conn):
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # ✅ Use DictCursor

#     print(f"Fetching trains for Source: {source}, Destination: {destination}, Day: {day_of_departure}")

#     # Step 1: Get train numbers that start or pass through the source on the given day
#     cur.execute(
#         "SELECT DISTINCT train_no FROM trains WHERE station_code = %s AND day_of_departure = %s",
#         (source, day_of_departure)
#     )
#     train_nos = [row["train_no"] for row in cur.fetchall()]  # ✅ Extract train_no list

#     if not train_nos:
#         print("No trains found for given source and day.")
#         return []

#     valid_trains = []

#     # Step 2: Fetch routes for these train numbers
#     for train_no in train_nos:
#         cur.execute(
#             "SELECT station_code, seq, arrival_time, departure_time FROM trains WHERE train_no = %s ORDER BY seq",
#             (train_no,)
#         )
#         route = cur.fetchall()

#         source_seq, destination_seq = None, None
#         source_departure, destination_arrival, destination_departure = None, None, None

#         # Step 3: Find source and destination sequence numbers
#         for row in route:
#             if row["station_code"] == source:
#                 source_seq = row["seq"]
#                 source_departure = row["departure_time"]

#             if row["station_code"] == destination:
#                 destination_seq = row["seq"]
#                 destination_arrival = row["arrival_time"]
#                 destination_departure = row["departure_time"]
#                 break  # ✅ No need to loop further once destination is found

#         # Step 4: Ensure source comes before destination
#         if source_seq is not None and destination_seq is not None and source_seq < destination_seq:
#             valid_trains.append(train_no)

#     return valid_trains  # ✅ Return only valid train numbers


# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# # ✅ Train search API
# @app.get("/trains")
# def get_trains(
#     source: str = Query(..., description="Source station"),
#     destination: str = Query(..., description="Destination station"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         day_number = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
        
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # Fetch unique train numbers that pass through the source station on the given day
#         cur.execute("""
#             SELECT DISTINCT train_no FROM trains
#             WHERE station_code = %s AND day_of_departure = %s
#         """, (source, day_number))
#         train_nos = [row["train_no"] for row in cur.fetchall()]
        
#         valid_trains = []
        
#         for train_no in train_nos:
#             cur.execute("""
#                 SELECT station_code, seq, arrival_time, departure_time, day_of_departure 
#                 FROM trains WHERE train_no = %s ORDER BY seq
#             """, (train_no,))
#             route = cur.fetchall()
            
#             source_seq, destination_seq = None, None
#             source_departure, destination_arrival = None, None
            
#             for row in route:
#                 if row["station_code"] == source:
#                     source_seq = row["seq"]
#                     source_departure = row["departure_time"]
                    
#                     # Check if day of departure matches
#                     if row["seq"] == 1 and row["day_of_departure"] != day_number:
#                         break  # Skip this train as it doesn't match the required day
                
#                 if row["station_code"] == destination:
#                     destination_seq = row["seq"]
#                     destination_arrival = row["arrival_time"]
#                     break
            
#             if source_seq is not None and destination_seq is not None and source_seq < destination_seq:
#                 valid_trains.append({
#                     "train_no": train_no,
#                     "from": source,
#                     "to": destination,
#                     "departure": source_departure,
#                     "arrival": destination_arrival
#                 })
        
#         return {"trains": valid_trains}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
#     finally:
#         conn.close()


# # ✅ API to fetch all stations
# @app.get("/stations")
# def get_stations():
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]

#         cur.close()
#         conn.close()
#         return {"stations": stations}

#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))



# /backend/main.py

# /backend/main.py

# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- QUERY FOR DIRECT TRAINS ---
#         if intermediate:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
#         direct_trains = [dict(row) for row in cur.fetchall()]

#         # --- QUERY FOR MULTI-LEG JOURNEYS ---
#         where_clause_for_intermediate = "leg1.intermediate_code = %s" if intermediate else "leg1.intermediate_code != %s AND leg1.intermediate_code != %s"
#         params_for_multileg = [source, journey_day, destination]
#         if intermediate:
#             params_for_multileg.append(intermediate)
#         else:
#             params_for_multileg.extend([destination, source])

#         query_multileg = f"""
#             WITH leg1 AS (
#                 SELECT
#                     t_start.train_no, t_start.station_name AS start_name, t_start.source_station_name AS train_origin,
#                     t_start.destination_station_name AS train_dest, t_start.departure_time AS start_departure_time,
#                     t_start.day_of_departure AS start_departure_day, t_intermediate.station_code AS intermediate_code,
#                     t_intermediate.station_name AS intermediate_name, t_intermediate.arrival_time AS intermediate_arrival_time,
#                     t_intermediate.day_of_arrival AS intermediate_arrival_day
#                 FROM trains AS t_start
#                 JOIN trains AS t_intermediate ON t_start.train_no = t_intermediate.train_no AND t_start.seq < t_intermediate.seq
#                 WHERE t_start.station_code = %s AND t_start.day_of_departure = %s
#             ),
#             leg2 AS (
#                 SELECT
#                     t_intermediate.train_no, t_intermediate.station_name AS start_name, t_intermediate.source_station_name AS train_origin,
#                     t_intermediate.destination_station_name AS train_dest, t_intermediate.station_code as intermediate_code,
#                     t_intermediate.departure_time AS start_departure_time, t_intermediate.day_of_departure AS start_departure_day,
#                     t_final.station_name AS final_name, t_final.arrival_time AS final_arrival_time,
#                     t_final.day_of_arrival AS final_arrival_day
#                 FROM trains AS t_intermediate
#                 JOIN trains AS t_final ON t_intermediate.train_no = t_final.train_no AND t_intermediate.seq < t_final.seq
#                 WHERE t_final.station_code = %s
#             )
#             SELECT
#                 leg1.train_no AS train1_no, leg1.start_name AS leg1_source_name, leg1.intermediate_name AS leg1_dest_name,
#                 leg1.train_origin AS train1_origin_name, leg1.train_dest AS train1_dest_name,
#                 leg1.start_departure_time AS t1_departure, leg1.start_departure_day AS t1_departure_day,
#                 leg1.intermediate_arrival_time AS t1_arrival, leg1.intermediate_arrival_day AS t1_arrival_day,
#                 leg2.train_no AS train2_no, leg2.start_name AS leg2_source_name, leg2.final_name AS leg2_dest_name,
#                 leg2.train_origin AS train2_origin_name, leg2.train_dest AS train2_dest_name,
#                 leg2.start_departure_time AS t2_departure,
#                 leg2.final_arrival_time AS t2_arrival,
                
#                 -- The crucial logic to calculate absolute journey days for Leg 2
#                 CASE
#                     WHEN leg1.intermediate_arrival_time > leg2.start_departure_time THEN leg1.intermediate_arrival_day + (leg2.start_departure_day - leg1.intermediate_arrival_day) + 1
#                     ELSE leg1.intermediate_arrival_day + (leg2.start_departure_day - leg1.intermediate_arrival_day)
#                 END AS t2_departure_day,
#                 CASE
#                     WHEN leg1.intermediate_arrival_time > leg2.start_departure_time THEN leg1.intermediate_arrival_day + (leg2.start_departure_day - leg1.intermediate_arrival_day) + 1 + (leg2.final_arrival_day - leg2.start_departure_day)
#                     ELSE leg1.intermediate_arrival_day + (leg2.start_departure_day - leg1.intermediate_arrival_day) + (leg2.final_arrival_day - leg2.start_departure_day)
#                 END AS t2_arrival_day
#             FROM leg1
#             JOIN leg2 ON leg1.intermediate_code = leg2.intermediate_code
#             WHERE 
#                 (leg1.intermediate_arrival_day, leg1.intermediate_arrival_time) <= (leg2.start_departure_day, leg2.start_departure_time)
#                 AND {where_clause_for_intermediate} AND leg1.train_no != leg2.train_no;
#         """

#         cur.execute(query_multileg, tuple(params_for_multileg))
#         multileg_journeys = [dict(row) for row in cur.fetchall()]

#         return {
#             "direct_trains": direct_trains,
#             "multileg_journeys": multileg_journeys
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- QUERY FOR DIRECT TRAINS (No change needed) ---
#         if intermediate:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
#         direct_trains = [dict(row) for row in cur.fetchall()]

#         # --- QUERY FOR MULTI-LEG JOURNEYS (DEFINITIVE FIX) ---
        
#         params_for_multileg = [source, journey_day, destination]
        
#         if intermediate:
#             where_clause_for_intermediate = "t1_dest.station_code = %s"
#             params_for_multileg.append(intermediate)
#         else:
#             where_clause_for_intermediate = "t1_dest.station_code != %s AND t1_dest.station_code != %s"
#             params_for_multileg.extend([destination, source])

#         # This query is now simpler and correctly structured
#         query_multileg = f"""
#             SELECT
#                 t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
#                 t1_dest.station_name AS leg1_dest_name,
#                 t1.source_station_name AS train1_origin_name, t1.destination_station_name AS train1_dest_name,
#                 t1.departure_time AS t1_departure, t1.day_of_departure AS t1_departure_day,
#                 t1_dest.arrival_time AS t1_arrival, t1_dest.day_of_arrival AS t1_arrival_day,
                
#                 t2.train_no AS train2_no, t2.station_name AS leg2_source_name,
#                 t2_dest.station_name AS leg2_dest_name,
#                 t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
#                 t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
#                 t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
#             FROM trains t1
#             JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
#             JOIN trains t2 ON t1_dest.station_code = t2.station_code
#             JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
#             WHERE
#                 t1.station_code = %s AND t1.day_of_departure = %s
#                 AND t2_dest.station_code = %s
#                 AND (t1_dest.day_of_arrival, t1_dest.arrival_time) <= (t2.day_of_departure, t2.departure_time)
#                 AND {where_clause_for_intermediate}
#                 AND t1.train_no != t2.train_no;
#         """

#         cur.execute(query_multileg, tuple(params_for_multileg))
#         multileg_journeys = [dict(row) for row in cur.fetchall()]

#         return {"direct_trains": direct_trains, "multileg_journeys": multileg_journeys}
#     except Exception as e:
#         # This will now print the specific database error to your backend terminal for easier debugging
#         print(f"An error occurred: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- QUERY FOR DIRECT TRAINS (Correct) ---
#         if intermediate:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
#         direct_trains = [dict(row) for row in cur.fetchall()]

#         # --- QUERY FOR MULTI-LEG JOURNEYS (DEFINITIVE FIX) ---
        
#         # CORRECTED PARAMETER LOGIC
#         params = [source, journey_day, destination]
        
#         intermediate_filter = ""
#         if intermediate:
#             intermediate_filter = "AND t1_dest.station_code = %s"
#             params.append(intermediate)
#         else:
#             intermediate_filter = "AND t1_dest.station_code != %s AND t1_dest.station_code != %s"
#             params.append(destination) # Add destination for the '!=' check
#             params.append(source)      # Add source for the '!=' check

#         query_multileg = f"""
#             SELECT
#                 t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
#                 t1_dest.station_name AS leg1_dest_name,
#                 t1.source_station_name AS train1_origin_name, t1.destination_station_name AS train1_dest_name,
#                 t1.departure_time AS t1_departure, t1.day_of_departure AS t1_departure_day,
#                 t1_dest.arrival_time AS t1_arrival, t1_dest.day_of_arrival AS t1_arrival_day,
                
#                 t2.train_no AS train2_no, t2.station_name AS leg2_source_name,
#                 t2_dest.station_name AS leg2_dest_name,
#                 t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
#                 t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
#                 t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
#             FROM trains t1
#             JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
#             JOIN trains t2 ON t1_dest.station_code = t2.station_code
#             JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
#             WHERE
#                 t1.station_code = %s AND t1.day_of_departure = %s
#                 AND t2_dest.station_code = %s
#                 AND (
#                     (t1_dest.day_of_arrival = t2.day_of_departure AND t1_dest.arrival_time <= t2.departure_time)
#                     OR ((t1_dest.day_of_arrival % 7) + 1 = t2.day_of_departure) -- Handles next day wrap-around
#                     OR (t1_dest.day_of_arrival = 7 AND t2.day_of_departure = 1) -- Explicitly handles Sun -> Mon
#                 )
#                 {intermediate_filter}
#                 AND t1.train_no != t2.train_no;
#         """

#         cur.execute(query_multileg, tuple(params))
#         multileg_journeys = [dict(row) for row in cur.fetchall()]

#         return {"direct_trains": direct_trains, "multileg_journeys": multileg_journeys}
#     except Exception as e:
#         print(f"An error occurred: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- DIRECT TRAINS LOGIC (Unchanged and Correct) ---
#         if intermediate:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
#         direct_trains = [dict(row) for row in cur.fetchall()]

#         # --- MULTI-LEG JOURNEYS (DEFINITIVE, SIMPLIFIED FIX) ---
#         multileg_journeys = []
#         base_query_select = """
#             SELECT
#                 t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
#                 t1_dest.station_name AS leg1_dest_name, t1.source_station_name AS train1_origin_name,
#                 t1.destination_station_name AS train1_dest_name, t1.departure_time AS t1_departure,
#                 t1.day_of_departure AS t1_departure_day, t1_dest.arrival_time AS t1_arrival,
#                 t1_dest.day_of_arrival AS t1_arrival_day, t2.train_no AS train2_no,
#                 t2.station_name AS leg2_source_name, t2_dest.station_name AS leg2_dest_name,
#                 t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
#                 t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
#                 t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
#             FROM trains t1
#             JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
#             JOIN trains t2 ON t1_dest.station_code = t2.station_code
#             JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
#         """
        
#         if intermediate:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s AND t1_dest.station_code = %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, intermediate))
#         else:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s
#                   AND t1_dest.station_code != %s AND t1_dest.station_code != %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, destination, source))
        
#         multileg_journeys = [dict(row) for row in cur.fetchall()]

#         return {"direct_trains": direct_trains, "multileg_journeys": multileg_journeys}

#     except Exception as e:
#         print(f"An error occurred: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     # ... (This function is correct and unchanged) ...
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- DIRECT TRAINS LOGIC ---
#         if intermediate:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = """
#                 SELECT
#                     t_source.train_no, t_source.station_name AS user_source_station_name,
#                     t_dest.station_name AS user_dest_station_name, t_source.departure_time AS user_departure_time,
#                     t_source.day_of_departure AS user_departure_day, t_dest.arrival_time AS user_arrival_time,
#                     t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                     t_source.destination_station_name AS train_destination_name
#                 FROM trains AS t_source
#                 JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
#         direct_trains = [dict(row) for row in cur.fetchall()]

#         # --- MULTI-LEG JOURNEYS LOGIC ---
#         base_query_select = """
#             SELECT
#                 t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
#                 t1_dest.station_name AS leg1_dest_name, t1.source_station_name AS train1_origin_name,
#                 t1.destination_station_name AS train1_dest_name, t1.departure_time AS t1_departure,
#                 t1.day_of_departure AS t1_departure_day, t1_dest.arrival_time AS t1_arrival,
#                 t1_dest.day_of_arrival AS t1_arrival_day, t2.train_no AS train2_no,
#                 t2.station_name AS leg2_source_name, t2_dest.station_name AS leg2_dest_name,
#                 t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
#                 t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
#                 t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
#             FROM trains t1
#             JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
#             JOIN trains t2 ON t1_dest.station_code = t2.station_code
#             JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
#         """
        
#         if intermediate:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s AND t1_dest.station_code = %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, intermediate))
#         else:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s
#                   AND t1_dest.station_code != %s AND t1_dest.station_code != %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, destination, source))
        
#         multileg_journeys = [dict(row) for row in cur.fetchall()]

#         return {"direct_trains": direct_trains, "multileg_journeys": multileg_journeys}

#     except Exception as e:
#         print(f"An error occurred: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

# /backend/main.py

# from fastapi import FastAPI, HTTPException, Query
# from database import get_db_connection
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime, timedelta
# import psycopg2.extras

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to RailLink API 🚄"}

# def get_full_date(base_date_str: str, base_day_of_week: int, event_day_of_week: int, event_time_iso: str) -> datetime:
#     """Calculates the absolute datetime for a train event."""
#     day_diff = event_day_of_week - base_day_of_week
#     if day_diff < 0:
#         day_diff += 7
    
#     base_date = datetime.strptime(base_date_str, "%Y-%m-%d")
#     event_date = base_date + timedelta(days=day_diff)
    
#     event_time = datetime.fromisoformat(event_time_iso).time()
    
#     return event_date.replace(hour=event_time.hour, minute=event_time.minute, second=event_time.second, microsecond=0)

# @app.get("/trains/search")
# def search_trains(
#     source: str = Query(..., description="Source station code"),
#     destination: str = Query(..., description="Destination station code"),
#     date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
#     intermediate: str | None = Query(None, description="Optional intermediate station code")
# ):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
    
#     try:
#         journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
#         # --- DIRECT TRAINS LOGIC ---
#         query_direct_base = """
#             SELECT
#                 t_source.train_no, t_source.station_name AS user_source_station_name,
#                 t_dest.station_name AS user_dest_station_name, t_source.departure_time,
#                 t_source.day_of_departure AS user_departure_day, t_dest.arrival_time,
#                 t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
#                 t_source.destination_station_name AS train_destination_name
#             FROM trains AS t_source JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
#         """
#         if intermediate:
#             query_direct = query_direct_base + """
#                 JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
#                 WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
#                   AND t_dest.station_code = %s AND t_source.day_of_departure = %s
#                   AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, intermediate, destination, journey_day))
#         else:
#             query_direct = query_direct_base + """
#                 WHERE t_source.station_code = %s AND t_dest.station_code = %s
#                   AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
#             """
#             cur.execute(query_direct, (source, destination, journey_day))
        
#         direct_train_results = cur.fetchall()
#         direct_trains = [
#             {
#                 **train,
#                 "user_departure_time": get_full_date(date, journey_day, train['user_departure_day'], str(train['departure_time'])).isoformat(),
#                 "user_arrival_time": get_full_date(date, journey_day, train['user_arrival_day'], str(train['arrival_time'])).isoformat() # CORRECTED
#             } for train in direct_train_results
#         ]

#         # --- MULTI-LEG JOURNEYS LOGIC ---
#         base_query_select = """
#             SELECT
#                 t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
#                 t1_dest.station_name AS leg1_dest_name, t1.source_station_name AS train1_origin_name,
#                 t1.destination_station_name AS train1_dest_name, t1.departure_time AS t1_departure,
#                 t1.day_of_departure AS t1_departure_day, t1_dest.arrival_time AS t1_arrival,
#                 t1_dest.day_of_arrival AS t1_arrival_day, t2.train_no AS train2_no,
#                 t2.station_name AS leg2_source_name, t2_dest.station_name AS leg2_dest_name,
#                 t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
#                 t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
#                 t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
#             FROM trains t1
#             JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
#             JOIN trains t2 ON t1_dest.station_code = t2.station_code
#             JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
#         """
        
#         if intermediate:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s AND t1_dest.station_code = %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, intermediate))
#         else:
#             query_multileg = base_query_select + """
#                 WHERE t1.station_code = %s AND t1.day_of_departure = %s
#                   AND t2_dest.station_code = %s
#                   AND t1_dest.station_code != %s AND t1_dest.station_code != %s
#                   AND t1.train_no != t2.train_no;
#             """
#             cur.execute(query_multileg, (source, journey_day, destination, destination, source))
        
#         multileg_results = cur.fetchall()
        
#         valid_journeys = []
#         for journey in multileg_results:
#             leg1_dep = get_full_date(date, journey_day, journey['t1_departure_day'], str(journey['t1_departure']))
#             leg1_arr = get_full_date(date, journey_day, journey['t1_arrival_day'], str(journey['t1_arrival'])) # CORRECTED
            
#             leg1_arr_date_str = leg1_arr.strftime("%Y-%m-%d")
#             leg2_dep = get_full_date(leg1_arr_date_str, journey['t1_arrival_day'], journey['t2_departure_day'], str(journey['t2_departure']))
            
#             if leg1_arr <= leg2_dep:
#                 leg2_arr = get_full_date(leg1_arr_date_str, journey['t1_arrival_day'], journey['t2_arrival_day'], str(journey['t2_arrival'])) # CORRECTED
#                 valid_journeys.append({
#                     **journey,
#                     "t1_departure": leg1_dep.isoformat(), "t1_arrival": leg1_arr.isoformat(),
#                     "t2_departure": leg2_dep.isoformat(), "t2_arrival": leg2_arr.isoformat(),
#                 })

#         return {"direct_trains": direct_trains, "multileg_journeys": valid_journeys}

#     except Exception as e:
#         print(f"An error occurred: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()

# @app.get("/stations")
# def get_stations():
#     # ... (This function is correct and unchanged) ...
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     try:
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
#         stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
#         cur.close()
#         return {"stations": stations}
#     except Exception as e:
#         print("❌ Error fetching stations:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if conn:
#             conn.close()


# /backend/main.py

from fastapi import FastAPI, HTTPException, Query
from database import get_db_connection
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import psycopg2.extras

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to RailLink API 🚄"}

def get_full_date(base_date_str: str, base_day_of_week: int, event_day_of_week: int, event_time_iso: str) -> datetime:
    """Calculates the absolute datetime for a train event."""
    day_diff = event_day_of_week - base_day_of_week
    if day_diff < 0:
        day_diff += 7
    
    base_date = datetime.strptime(base_date_str, "%Y-%m-%d")
    event_date = base_date + timedelta(days=day_diff)
    
    event_time = datetime.fromisoformat(event_time_iso).time()
    
    return event_date.replace(hour=event_time.hour, minute=event_time.minute, second=event_time.second, microsecond=0)

@app.get("/trains/search")
def search_trains(
    source: str = Query(..., description="Source station code"),
    destination: str = Query(..., description="Destination station code"),
    date: str = Query(..., description="Journey date (YYYY-MM-DD)"),
    intermediate: str | None = Query(None, description="Optional intermediate station code")
):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        journey_day = datetime.strptime(date, "%Y-%m-%d").weekday() + 1
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # --- DIRECT TRAINS LOGIC ---
        query_direct_base = """
            SELECT
                t_source.train_no, t_source.station_name AS user_source_station_name,
                t_dest.station_name AS user_dest_station_name, t_source.departure_time,
                t_source.day_of_departure AS user_departure_day, t_dest.arrival_time,
                t_dest.day_of_arrival AS user_arrival_day, t_source.source_station_name AS train_origin_name,
                t_source.destination_station_name AS train_destination_name
            FROM trains AS t_source JOIN trains AS t_dest ON t_source.train_no = t_dest.train_no
        """
        if intermediate:
            query_direct = query_direct_base + """
                JOIN trains AS t_intermediate ON t_source.train_no = t_intermediate.train_no
                WHERE t_source.station_code = %s AND t_intermediate.station_code = %s
                  AND t_dest.station_code = %s AND t_source.day_of_departure = %s
                  AND t_source.seq < t_intermediate.seq AND t_intermediate.seq < t_dest.seq;
            """
            cur.execute(query_direct, (source, intermediate, destination, journey_day))
        else:
            query_direct = query_direct_base + """
                WHERE t_source.station_code = %s AND t_dest.station_code = %s
                  AND t_source.day_of_departure = %s AND t_source.seq < t_dest.seq;
            """
            cur.execute(query_direct, (source, destination, journey_day))
        
        direct_train_results = cur.fetchall()
        direct_trains = [
            {
                **train,
                "user_departure_time": get_full_date(date, journey_day, train['user_departure_day'], str(train['departure_time'])).isoformat(),
                "user_arrival_time": get_full_date(date, journey_day, train['user_arrival_day'], str(train['arrival_time'])).isoformat()
            } for train in direct_train_results
        ]

        # --- MULTI-LEG JOURNEYS LOGIC ---
        base_query_select = """
            SELECT
                t1.train_no AS train1_no, t1.station_name AS leg1_source_name,
                t1_dest.station_name AS leg1_dest_name, t1.source_station_name AS train1_origin_name,
                t1.destination_station_name AS train1_dest_name, t1.departure_time AS t1_departure,
                t1.day_of_departure AS t1_departure_day, t1_dest.arrival_time AS t1_arrival,
                t1_dest.day_of_arrival AS t1_arrival_day, t2.train_no AS train2_no,
                t2.station_name AS leg2_source_name, t2_dest.station_name AS leg2_dest_name,
                t2.source_station_name AS train2_origin_name, t2.destination_station_name AS train2_dest_name,
                t2.departure_time AS t2_departure, t2.day_of_departure AS t2_departure_day,
                t2_dest.arrival_time AS t2_arrival, t2_dest.day_of_arrival AS t2_arrival_day
            FROM trains t1
            JOIN trains t1_dest ON t1.train_no = t1_dest.train_no AND t1.seq < t1_dest.seq
            JOIN trains t2 ON t1_dest.station_code = t2.station_code
            JOIN trains t2_dest ON t2.train_no = t2_dest.train_no AND t2.seq < t2_dest.seq
        """
        
        if intermediate:
            query_multileg = base_query_select + """
                WHERE t1.station_code = %s AND t1.day_of_departure = %s
                  AND t2_dest.station_code = %s AND t1_dest.station_code = %s
                  AND t1.train_no != t2.train_no;
            """
            cur.execute(query_multileg, (source, journey_day, destination, intermediate))
        else:
            query_multileg = base_query_select + """
                WHERE t1.station_code = %s AND t1.day_of_departure = %s
                  AND t2_dest.station_code = %s
                  AND t1_dest.station_code != %s AND t1_dest.station_code != %s
                  AND t1.train_no != t2.train_no;
            """
            cur.execute(query_multileg, (source, journey_day, destination, destination, source))
        
        multileg_results = cur.fetchall()
        
        valid_journeys = []
        for journey in multileg_results:
            leg1_dep = get_full_date(date, journey_day, journey['t1_departure_day'], str(journey['t1_departure']))
            leg1_arr = get_full_date(date, journey_day, journey['t1_arrival_day'], str(journey['t1_arrival']))
            
            leg1_arr_date_str = leg1_arr.strftime("%Y-%m-%d")
            leg2_dep = get_full_date(leg1_arr_date_str, journey['t1_arrival_day'], journey['t2_departure_day'], str(journey['t2_departure']))
            
            if leg1_arr <= leg2_dep:
                # --- THIS IS THE CORRECTED LINE ---
                leg2_dep_date_str = leg2_dep.strftime("%Y-%m-%d")
                leg2_arr = get_full_date(leg2_dep_date_str, journey['t2_departure_day'], journey['t2_arrival_day'], str(journey['t2_arrival']))
                
                valid_journeys.append({
                    **journey,
                    "t1_departure": leg1_dep.isoformat(), "t1_arrival": leg1_arr.isoformat(),
                    "t2_departure": leg2_dep.isoformat(), "t2_arrival": leg2_arr.isoformat(),
                })

        return {"direct_trains": direct_trains, "multileg_journeys": valid_journeys}

    except Exception as e:
        print(f"An error occurred: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/trains/all")
def get_all_trains(page: int = 1, limit: int = 20):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # First, count the total number of unique trains for pagination
        cur.execute("SELECT COUNT(DISTINCT train_no) FROM trains;")
        total_trains = cur.fetchone()[0]
        total_pages = (total_trains + limit - 1) // limit # Ceiling division

        # Then, fetch the unique trains for the current page
        offset = (page - 1) * limit
        query = """
            SELECT DISTINCT train_no, train_name, source_station_name, destination_station_name
            FROM trains
            ORDER BY train_no
            LIMIT %s OFFSET %s;
        """
        cur.execute(query, (limit, offset))
        trains = [dict(row) for row in cur.fetchall()]

        return {
            "trains": trains,
            "total_pages": total_pages,
            "current_page": page
        }

    except Exception as e:
        print(f"An error occurred while fetching all trains: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/trains/{train_no}")
def get_train_details(train_no: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT * FROM trains
            WHERE train_no = %s
            ORDER BY seq;
        """
        cur.execute(query, (train_no,))
        
        schedule = [dict(row) for row in cur.fetchall()]

        if not schedule:
            raise HTTPException(status_code=404, detail="Train not found")

        return {
            "train_name": schedule[0]['train_name'],
            "source_station_name": schedule[0]['source_station_name'],
            "destination_station_name": schedule[0]['destination_station_name'],
            "schedule": schedule
        }

    except Exception as e:
        print(f"An error occurred while fetching train details: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/stations")
def get_stations():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT DISTINCT station_code, station_name FROM trains ORDER BY station_name;")
        stations = [{"station_code": row["station_code"], "station_name": row["station_name"]} for row in cur.fetchall()]
        cur.close()
        return {"stations": stations}
    except Exception as e:
        print("❌ Error fetching stations:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()