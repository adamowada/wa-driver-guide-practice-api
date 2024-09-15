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
