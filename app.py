from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            question_image BLOB,
            answer_image BLOB,
            student_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    populate_random_flashcards(conn)
    conn.close()

def populate_random_flashcards(conn):
    subjects = ['Mathematics', 'Science', 'History', 'Language Arts', 'Geography']
    for _ in range(random.randint(5, 15)):  # Random number of flashcards
        subject = random.choice(subjects)
        question = f"Sample question for {subject}"
        answer = f"Sample answer for {subject}"
        student_name = f"Student {_}"
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO flashcards (category, subject, question, answer, student_name)
            VALUES (?, ?, ?, ?, ?)
        ''', ('General', subject, question, answer, student_name))
    conn.commit()

def add_predefined_flashcards(conn):
    predefined_flashcards = [
        {'category': 'General', 'subject': 'Mathematics', 'question': 'What is 2+2?', 'answer': '4', 'student_name': 'Alice'},
        {'category': 'General', 'subject': 'Science', 'question': 'What is the chemical symbol for water?', 'answer': 'H2O', 'student_name': 'Bob'},
        {'category': 'General', 'subject': 'History', 'question': 'Who was the first President of the United States?', 'answer': 'George Washington', 'student_name': 'Charlie'},
        {'category': 'General', 'subject': 'Language Arts', 'question': 'What is a synonym for happy?', 'answer': 'Joyful', 'student_name': 'David'},
        {'category': 'General', 'subject': 'Geography', 'question': 'What is the capital of France?', 'answer': 'Paris', 'student_name': 'Eve'}
    ]

    cursor = conn.cursor()
    for flashcard in predefined_flashcards:
        cursor.execute('''
            INSERT INTO flashcards (category, subject, question, answer, student_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (flashcard['category'], flashcard['subject'], flashcard['question'], flashcard['answer'], flashcard['student_name']))
    conn.commit()

@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    data = request.form
    question_image = request.files.get('question_image')
    answer_image = request.files.get('answer_image')
    
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flashcards (category, subject, question, answer, question_image, answer_image, student_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['category'], data['subject'], data['question'], data['answer'], question_image.read() if question_image else None, answer_image.read() if answer_image else None, data['student_name']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Flashcard added successfully'}), 201

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (data['username'], data['password']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/get_flashcards', methods=['GET'])
def get_flashcards():
    category = request.args.get('category')
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, question, answer, student_name FROM flashcards WHERE category = ?
    ''', (category,))
    flashcards = cursor.fetchall()
    conn.close()
    return jsonify([{'category': fc[0], 'question': fc[1], 'answer': fc[2], 'student_name': fc[3]} for fc in flashcards]), 200

if __name__ == '__main__':
    init_db()
    conn = sqlite3.connect('flashcards.db')
    add_predefined_flashcards(conn)
    conn.close()
    app.run(debug=True)
