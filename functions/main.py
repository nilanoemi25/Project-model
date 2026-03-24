# from firebase_functions import https_fn
# from fastapi import FastAPI, Query
# from fastapi.testclient import TestClient
# from fastapi.middleware.cors import CORSMiddleware
# import json

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- CONFIGURATION ---
# MONGO_URI = "mongodb+srv://20108892_db_user:DUBFUR5f3@cluster0.gcbfedc.mongodb.net/test?appName=Cluster0"
# DB_NAME = "test"
# COLLECTION_TASKS = "tasks"
# COLLECTION_DATES = "dates"

# def get_ai_logic(target_user_id: str):
#     import pandas as pd
#     import numpy as np
#     import random
#     from pymongo import MongoClient

#     SUGGESTION_POOLS = {
#     "Consistent Star": [
#         "You're a star! Your rhythm is perfect.",
#         "Incredible consistency! Keep leading the way.",
#         "Masterful work! Your habits are becoming second nature.",
#         "You're in the 'flow state'—don't stop now!",
#         "Elite performance! How does it feel to be this disciplined?",
#         "You've turned effort into identity. You are officially a pro."
#     ],
#    "At-Risk": [
#         "Let's try to get back on track with one small win today.",
#         "Progress isn't linear. What's one tiny task you can do now?",
#         "Don't let a slip become a slide. You've got this!",
#         "The best time to start again is right now. Just 2 minutes?",
#         "Forget yesterday. What is the smallest possible version of this habit?",
#         "Your streak might have paused, but your potential hasn't. Reset and go."
#     ],
#        "Rising Star": [
#         "Great progress! Your consistency is improving.",
#         "You're building momentum! Keep showing up.",
#         "The trend is looking up! Stay focused.",
#         "You're bridging the gap between 'trying' and 'doing.' Keep at it!",
#         "Can you feel the shift? You're becoming the person you want to be.",
#         "Almost at 'Consistent Star' status—just a few more days!"
#     ],
#    "Habit Builder": [
#         "Start logging more tasks in this category to unlock your AI persona!",
#         "Consistency starts with small, daily entries.",
#         "Try to complete at least one task here today to build a streak.",
#         "You're in the 'foundation' phase. Every brick counts.",
#         "Small steps lead to big changes. What's the plan for today?",
#         "The AI is hungry for data! Log your progress to see your evolution."
#     ]
#     }

#     try:
#         client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
#         db = client[DB_NAME]
        
#         pipeline = [
#             {"$addFields": {"converted_dateid": {"$toObjectId": "$dateid"}}},
#             {"$lookup": {
#                 "from": COLLECTION_DATES,
#                 "localField": "converted_dateid",
#                 "foreignField": "_id",
#                 "as": "date_info"
#             }},
#             {"$unwind": "$date_info"},
#             {"$project": {
#                 "user_id": "$userid",
#                 "category": { "$ifNull": ["$classification", "General"] }, 
#                 "fulldatestamp": "$date_info.fulldatestamp"
#             }}
#         ]
        
#         data = list(db[COLLECTION_TASKS].aggregate(pipeline))
#         if not data:
#             return {"error": "No matching data found."}

#         df = pd.DataFrame(data)
#         df['user_id'] = df['user_id'].astype(str)
        
#         # Filter for the specific user
#         user_df = df[df['user_id'] == target_user_id].copy()
#         if user_df.empty:
#             return {"error": f"User {target_user_id} not found."}

#         # Data Cleaning: Normalize category names and parse dates
#         user_df['category'] = user_df['category'].astype(str).str.strip().str.title()
#         user_df['timestamp'] = pd.to_datetime(user_df['fulldatestamp'], errors='coerce')
#         user_df.dropna(subset=['timestamp'], inplace=True)

#         categories = user_df['category'].unique()
#         final_results = []

#         for cat in categories:
#             cat_df = user_df[user_df['category'] == cat].copy()
            
#             # Count unique physical days logged for this category
#             active_days = cat_df['timestamp'].dt.normalize().unique()
#             active_days_count = len(active_days)
            
#             # Create daily completion matrix for scoring
#             cat_df = cat_df.set_index('timestamp')
#             cat_df['completed'] = 1
#             matrix = cat_df.groupby(pd.Grouper(freq='D'))['completed'].any().astype(int)
            
#             # --- EVALUATION LOGIC ---
#             # Trigger Persona on the 3rd day of activity (3 or more)
#             if active_days_count < 3:
#                 persona = "Habit Builder"
#             else:
#                 completion_rate = matrix.mean()
#                 if completion_rate >= 0.75:
#                     persona = "Consistent Star"
#                 elif completion_rate <= 0.40:
#                     persona = "At-Risk"
#                 else:
#                     persona = "Rising Star"

#             final_results.append({
#                 "user_id": target_user_id,
#                 "category": cat,
#                 "persona": persona,
#                 "suggestion": random.choice(SUGGESTION_POOLS[persona])
#             })

#         return final_results

#     except Exception as e:
#         return {"error": str(e)}

# # --- API ROUTES ---

# @app.get("/get-suggestions")
# async def fetch_suggestions(user_id: str = Query(...)):
#     results = get_ai_logic(user_id)
#     if isinstance(results, dict) and "error" in results:
#         return {"status": "error", "message": results["error"]}
    
#     return {"status": "success", "data": results}

# @app.get("/")
# async def root():
#     return {"message": "AI Habitat API is Online."}

# # --- FIREBASE ENTRY POINT ---

# @https_fn.on_request(memory=1024, timeout_sec=60)
# def habitat_api(req: https_fn.Request) -> https_fn.Response:
#     with TestClient(app) as client:
#         path = req.path.replace("/habitat_api", "")
#         if not path: path = "/"
            
#         response = client.request(
#             method=req.method,
#             url=path,
#             params=req.args,
#             content=req.data,
#             headers=dict(req.headers)
#         )
        
#         return https_fn.Response(
#             response.text,
#             status=response.status_code,
#             headers=dict(response.headers),
#             mimetype="application/json"
#         )

from firebase_functions import https_fn
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION ---
MONGO_URI = "mongodb+srv://20108892_db_user:DUBFUR5f3@cluster0.gcbfedc.mongodb.net/test?appName=Cluster0"
DB_NAME = "test"
COLLECTION_TASKS = "tasks"
COLLECTION_DATES = "dates"

def get_ai_logic(target_user_id: str):
    import pandas as pd
    import numpy as np
    from pymongo import MongoClient

    SUGGESTION_POOLS = {
        "Consistent Star": [
            "You're a star! Your rhythm is perfect.",
            "Incredible consistency! Keep leading the way.",
            "Masterful work! Your habits are becoming second nature.",
            "Elite performance! How does it feel to be this disciplined?"
        ],
        "At-Risk": [
            "Let's try to get back on track with one small win today.",
            "Progress isn't linear. What's one tiny task you can do now?",
            "Don't let a slip become a slide. You've got this!",
            "The best time to start again is right now."
        ],
        "Rising Star": [
            "Great progress! Your consistency is improving.",
            "You're building momentum! Keep showing up.",
            "The trend is looking up! Stay focused.",
            "Can you feel the shift? You're becoming the person you want to be."
        ],
        "Habit Builder": [
            "Start logging more tasks in this category to unlock your AI persona!",
            "Consistency starts with small, daily entries.",
            "The AI is hungry for data! Log your progress to see your evolution.",
            "Small steps lead to big changes. What's the plan for today?"
        ],
        "Newcomer": [
            "Welcome! Ready to start your journey? Add your first task to see AI insights!",
            "Your habit tracker is a blank canvas. Let's add some color—log a task!",
            "Every big change starts with a single entry. What are we working on today?",
            "Start your first habit today and let the AI track your rise to the top!"
        ],
        "Diversity Scout": [
            "Focus is great, but balance is better! Try adding a task in a new category.",
            "One-track mind? Add tasks to other categories to see your full life-balance score!",
            "You're doing great here! Why not start a small habit in 'Health' or 'Learning'?",
            "Variety is the spice of life. What else can we track today?"
        ]
    }

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        
        # Pipeline to join Tasks with Dates
        pipeline = [
            {"$addFields": {"converted_dateid": {"$toObjectId": "$dateid"}}},
            {"$lookup": {
                "from": COLLECTION_DATES,
                "localField": "converted_dateid",
                "foreignField": "_id",
                "as": "date_info"
            }},
            {"$unwind": "$date_info"},
            {"$project": {
                "user_id": "$userid",
                "category": { "$ifNull": ["$classification", "General"] }, 
                "fulldatestamp": "$date_info.fulldatestamp"
            }}
        ]
        
        data = list(db[COLLECTION_TASKS].aggregate(pipeline))
        
        # 1. CHECK IF USER HAS DATA
        user_found = False
        user_df = pd.DataFrame()
        if data:
            df = pd.DataFrame(data)
            df['user_id'] = df['user_id'].astype(str)
            user_df = df[df['user_id'] == target_user_id].copy()
            if not user_df.empty:
                user_found = True

        # 2. IF NEW USER (NO DATA)
        if not user_found:
            return [{
                "user_id": target_user_id,
                "category": "Getting Started",
                "persona": "Newcomer",
                "suggestion": random.choice(SUGGESTION_POOLS["Newcomer"])
            }]

        # 3. PROCESS DATA FOR EXISTING USER
        user_df['category'] = user_df['category'].astype(str).str.strip().str.title()
        user_df['timestamp'] = pd.to_datetime(user_df['fulldatestamp'], errors='coerce')
        user_df.dropna(subset=['timestamp'], inplace=True)

        categories = user_df['category'].unique()
        final_results = []

        # Generate persona for each active category
        for cat in categories:
            cat_df = user_df[user_df['category'] == cat].copy()
            active_days_count = len(cat_df['timestamp'].dt.normalize().unique())
            
            # Matrix for completion rate
            cat_df = cat_df.set_index('timestamp')
            cat_df['completed'] = 1
            matrix = cat_df.groupby(pd.Grouper(freq='D'))['completed'].any().astype(int)
            
            if active_days_count < 3:
                persona = "Habit Builder"
            else:
                completion_rate = matrix.mean()
                if completion_rate >= 0.75:
                    persona = "Consistent Star"
                elif completion_rate <= 0.40:
                    persona = "At-Risk"
                else:
                    persona = "Rising Star"

            final_results.append({
                "user_id": target_user_id,
                "category": cat,
                "persona": persona,
                "suggestion": random.choice(SUGGESTION_POOLS[persona])
            })

        # 4. ADD DIVERSITY SCOUT MESSAGE (IF ONLY 1-2 CATEGORIES EXIST)
        if len(categories) <= 2:
            final_results.append({
                "user_id": target_user_id,
                "category": "Growth Tip",
                "persona": "Diversity Scout",
                "suggestion": random.choice(SUGGESTION_POOLS["Diversity Scout"])
            })

        return final_results

    except Exception as e:
        return {"error": str(e)}

# --- API ROUTES ---

@app.get("/get-suggestions")
async def fetch_suggestions(user_id: str = Query(...)):
    results = get_ai_logic(user_id)
    # If the logic returns a dict with error, bubble it up
    if isinstance(results, dict) and "error" in results:
        return {"status": "error", "message": results["error"]}
    
    return {"status": "success", "data": results}

@app.get("/")
async def root():
    return {"message": "AI Habitat API is Online."}

# --- FIREBASE ENTRY POINT ---

@https_fn.on_request(memory=1024, timeout_sec=60)
def habitat_api(req: https_fn.Request) -> https_fn.Response:
    with TestClient(app) as client:
        path = req.path.replace("/habitat_api", "")
        if not path: path = "/"
            
        response = client.request(
            method=req.method,
            url=path,
            params=req.args,
            content=req.data,
            headers=dict(req.headers)
        )
        
        return https_fn.Response(
            response.text,
            status=response.status_code,
            headers=dict(response.headers),
            mimetype="application/json"
        )