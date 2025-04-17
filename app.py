from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load data from JSON
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract unique subjects from data
subjects = sorted(set(item['subject'] for item in data))

# Load the questions data from data.json
with open('data.json', 'r') as f:
    questions_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', subjects=subjects)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()
    filtered_questions = []

    # Loop through the questions data to find matches
    for question in questions_data:
        if query in question['title'].lower() or query in question['question'].lower():
            filtered_questions.append(question)

    return render_template('search_results.html', query=query, results=filtered_questions)

@app.route('/papers/<subject>')
def papers(subject):
    papers = sorted(set(item['paper'] for item in data if item['subject'] == subject))
    return render_template('papers.html', subject=subject, papers=papers)

@app.route('/boards/<subject>/<paper>')
def boards(subject, paper):
    boards = sorted(set(item['board'] for item in data if item['subject'] == subject and item['paper'] == paper))
    return render_template('boards.html', subject=subject, paper=paper, boards=boards)

@app.route('/years/<subject>/<paper>/<board>')
def years(subject, paper, board):
    years = sorted(set(item['year'] for item in data if item['subject'] == subject and item['paper'] == paper and item['board'] == board), reverse=True)
    return render_template('years.html', subject=subject, paper=paper, board=board, years=years)

@app.route('/questions/<subject>/<paper>/<board>/<year>')
def questions(subject, paper, board, year):
    questions = [item for item in data if item['subject'] == subject and item['paper'] == paper and item['board'] == board and str(item['year']) == str(year)]
    return render_template('questions.html', subject=subject, paper=paper, board=board, year=year, questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
