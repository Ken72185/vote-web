from flask import Flask, render_template, request, jsonify
import json
import datetime
import os
import uuid

app = Flask(__name__)
# INI KUNCI FIX-NYA: Pake folder /tmp/ biar Vercel ngizinin nyimpen file
DATA_FILE = '/tmp/polls.json' 

def load_data():
    if not os.path.exists(DATA_FILE):
        return {} 
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create', methods=['POST'])
def create_poll():
    data = request.json
    title = data.get('title')
    options = data.get('options')
    
    if not title or not options or len(options) < 2:
        return jsonify({"status": "error", "message": "Judul dan minimal 2 opsi wajib diisi!"}), 400
        
    poll_id = str(uuid.uuid4())[:8]
    polls = load_data()
    
    polls[poll_id] = {
        "title": title,
        "options": options,
        "votes": []
    }
    save_data(polls)
    
    return jsonify({"status": "sukses", "poll_id": poll_id})

@app.route('/vote/<poll_id>')
def vote_page(poll_id):
    polls = load_data()
    if poll_id not in polls:
        return "Waduh brok, polling ga ketemu atau link salah", 404
    
    poll_data = polls[poll_id]
    return render_template('vote.html', poll_id=poll_id, title=poll_data['title'], options=poll_data['options'])

@app.route('/api/vote/<poll_id>', methods=['POST'])
def submit_vote(poll_id):
    data = request.json
    choice = data.get('choice')
    polls = load_data()
    
    if poll_id in polls and choice in polls[poll_id]['options']:
        new_vote = {
            'choice': choice,
            'waktu_ngisi': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        polls[poll_id]['votes'].append(new_vote)
        save_data(polls)
        return jsonify({"status": "sukses"})
    return jsonify({"status": "error"}), 400

@app.route('/dashboard/<poll_id>')
def dashboard(poll_id):
    polls = load_data()
    if poll_id not in polls:
        return "Waduh brok, polling ga ketemu", 404
    return render_template('dashboard.html', poll_id=poll_id, title=polls[poll_id]['title'])

@app.route('/api/stats/<poll_id>', methods=['GET'])
def stats(poll_id):
    polls = load_data()
    if poll_id in polls:
        return jsonify(polls[poll_id]['votes'])
    return jsonify([]), 404

if __name__ == '__main__':
    app.run(debug=True)
