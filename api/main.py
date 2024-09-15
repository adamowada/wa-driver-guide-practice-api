from fastapi import FastAPI

from chatgpt.question_generator import generate_questions
from database.db_operations import insert_question, insert_answer, get_client, get_all_questions_and_answers


app = FastAPI()


# @app.post("/api/create-questions")
# async def generate_questions():
# 	questions_data = await generate_questions()

# 	# Initialize the client within the event loop
# 	client = await get_client()

# 	# Insert each question and its answers into the database
# 	for question in questions_data['questions']:
# 		question_text = question['question']
# 		image_url = question['image_url']

# 		# Insert question into the database
# 		question_id = await insert_question(client, question_text, image_url)

# 		# Insert answers
# 		for answer in question['answers']:
# 			answer_text = answer['text']
# 			is_correct = answer['correct']
# 			explanation = answer['explanation']
# 			await insert_answer(client, question_id, answer_text, is_correct, explanation)

# 	return {
# 		"status": "success", 
# 		"message": "Questions generated and inserted successfully.",
# 		"questions": questions_data["questions"],
# 	}


@app.get("/api/get-questions")
async def get_all_questions():
    client = await get_client()
    questions_data = await get_all_questions_and_answers(client)
    return questions_data
