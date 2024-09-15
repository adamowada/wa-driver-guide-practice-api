import os

from libsql_client import create_client
from dotenv import load_dotenv


# Load environment variables
load_dotenv(".env")

# Turso Database Credentials
TURSO_DB_URL = os.getenv("TURSO_DB_URL")
TURSO_DB_AUTH_TOKEN = os.getenv("TURSO_DB_AUTH_TOKEN")


async def get_client():
    return create_client(url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)


async def insert_question(client, question_text, image_url):
    try:
        query = """
        INSERT INTO questions (question_text, image_url) VALUES (?, ?)
        """
        params = (question_text, image_url)
        result = await client.execute(query, params)
        question_id = result.last_insert_rowid
        return question_id

    except Exception as e:
        print(f"Error inserting question: {e}")
        return None


async def insert_answer(client, question_id, answer_text, is_correct, explanation):
    try:
        query = """
        INSERT INTO answers (question_id, answer_text, is_correct, explanation)
        VALUES (?, ?, ?, ?)
        """
        params = (question_id, answer_text, is_correct, explanation)
        await client.execute(query, params)

    except Exception as e:
        print(f"Error inserting answer: {e}")


async def get_all_questions_and_answers(client):
    try:
        # Fetch all questions
        questions_query = "SELECT id, question_text, image_url FROM questions"
        questions_result = await client.execute(questions_query)
        
        columns = questions_result.columns
        rows = questions_result.rows

        questions_list = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            question_id = row_dict['id']
            question_text = row_dict['question_text']
            image_url = row_dict['image_url'] or ""

            # Fetch answers for the current question
            answers_query = "SELECT answer_text, is_correct, explanation FROM answers WHERE question_id = ?"
            answers_result = await client.execute(answers_query, [question_id])
            answer_columns = answers_result.columns
            answer_rows = answers_result.rows

            answers_list = []
            
            for answer_row in answer_rows:
                answer_row_dict = dict(zip(answer_columns, answer_row))
                answer_text = answer_row_dict['answer_text']
                is_correct = answer_row_dict['is_correct']
                explanation = answer_row_dict['explanation']

                answer_dict = {
                    "correct": bool(is_correct),
                    "explanation": explanation,
                    "text": answer_text
                }
                answers_list.append(answer_dict)

            question_dict = {
                "question": question_text,
                "answers": answers_list,
                "image_url": image_url
            }

            questions_list.append(question_dict)
        
        return {"questions": questions_list}
    
    except Exception as e:
        print(f"Error fetching questions and answers: {e}")
        return {"questions": []}
