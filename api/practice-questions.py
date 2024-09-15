# api/practice-questions.py
from aiohttp import web
from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client

from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")


async def handle(request):
	questions_data = await generate_questions()
	questions_inserted = []

	# Initialize the client within the event loop
	client = await get_client()

	# Insert each question and its answers into the database
	for question in questions_data.get('questions', []):
		question_text = question['question']
		image_url = question.get('image_url', '')

		# Insert question into the database
		question_id = await insert_question(client, question_text, image_url)

		# Insert answers
		for answer in question['answers']:
			answer_text = answer['text']
			is_correct = answer['correct']
			explanation = answer.get('explanation', '')
			await insert_answer(client, question_id, answer_text, is_correct, explanation)

		questions_inserted.append({
			'question_id': question_id,
			'question_text': question_text
		})

	# Forming the response
	response_data = {
		'status': 'success',
		'questions_inserted': questions_inserted
	}

	return web.json_response(questions_data)


if __name__ == '__main__':
	app = web.Application()
	app.router.add_get('/', handle)
	web.run_app(app, host='localhost', port=8000)
