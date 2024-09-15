from fastapi import FastAPI

from database.db_operations import get_client, get_all_questions_and_answers


app = FastAPI()


# Vercel: one function per file
# route MUST match file name or 404
# function can be named anything
@app.get("/api/get-questions")
async def get_questions():
    client = await get_client()
    try:
        questions_data = await get_all_questions_and_answers(client)
    finally:
        client.close()
    return questions_data
