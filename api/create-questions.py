from fastapi import FastAPI

from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client


app = FastAPI()


# Vercel: one function per file
# route MUST match file name or 404
# function can be named anything
@app.post("/api/create-questions")
async def create_questions():
	questions_data = await generate_questions()
	previous_questions = questions_data[1]
	questions_data = questions_data[0]

	client = await get_client()

	# Insert each question and its answers into the database
	for question in questions_data['questions']:
		question_text = question['question']
		image_url = question.get('image_url', None)

		# Insert question into the database
		question_id = await insert_question(client, question_text, image_url)

		# Insert answers
		for answer in question['answers']:
			answer_text = answer['text']
			is_correct = answer['correct']
			explanation = answer['explanation']
			await insert_answer(client, question_id, answer_text, is_correct, explanation)

	await client.close()

	return [questions_data, previous_questions[0]["content"][0]["text"]]
