from aiohttp import web
from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client


async def handler(request):
	questions_data = await generate_questions()

	# Initialize the client within the event loop
	client = await get_client()

	# Insert each question and its answers into the database
	for question in questions_data['questions']:
		question_text = question['question']
		image_url = question['image_url']

		# Insert question into the database
		question_id = await insert_question(client, question_text, image_url)

		# Insert answers
		for answer in question['answers']:
			answer_text = answer['text']
			is_correct = answer['correct']
			explanation = answer['explanation']
			await insert_answer(client, question_id, answer_text, is_correct, explanation)

	return web.json_response(questions_data)


if __name__ == '__main__':
	app = web.Application()
	app.router.add_get('/api/practice-questions', handler)
	web.run_app(app, host='localhost', port=8000)
