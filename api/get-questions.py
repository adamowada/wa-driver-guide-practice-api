# from aiohttp import web
from fastapi import FastAPI

from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client, get_all_questions_and_answers


app = FastAPI()


# Vercel: one function per file
# route MUST match file name or 404
@app.get("/api/get-questionsz")
async def get_questions():
    client = await get_client()
    questions_data = await get_all_questions_and_answers(client)
    return questions_data
