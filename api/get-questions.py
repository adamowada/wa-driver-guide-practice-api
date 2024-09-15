# from aiohttp import web
from fastapi import FastAPI

from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client, get_all_questions_and_answers


app = FastAPI()


@app.get("/api/get-questions")
async def get1_questions():
    client = await get_client()
    questions_data = await get_all_questions_and_answers(client)
    return questions_data
