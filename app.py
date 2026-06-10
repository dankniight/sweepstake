from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/res/flags/<path:filename>')
def serve_flag(filename):
    flags_dir = os.path.join(os.path.dirname(__file__), 'res', 'flags')
    return send_from_directory(flags_dir, filename)

WORLD_CUP_TEAMS = [
    # AFC
    {"name": "Australia", "flag": "🇦🇺"},
    {"name": "Iran", "flag": "🇮🇷"},
    {"name": "Iraq", "flag": "🇮🇶"},
    {"name": "Japan", "flag": "🇯🇵"},
    {"name": "Jordan", "flag": "🇯🇴"},
    {"name": "Qatar", "flag": "🇶🇦"},
    {"name": "Saudi Arabia", "flag": "🇸🇦"},
    {"name": "South Korea", "flag": "🇰🇷"},
    {"name": "Uzbekistan", "flag": "🇺🇿"},
    # CAF
    {"name": "Algeria", "flag": "🇩🇿"},
    {"name": "Cape Verde", "flag": "🇨🇻"},
    {"name": "DR Congo", "flag": "🇨🇩"},
    {"name": "Egypt", "flag": "🇪🇬"},
    {"name": "Ghana", "flag": "🇬🇭"},
    {"name": "Ivory Coast", "flag": "🇨🇮"},
    {"name": "Morocco", "flag": "🇲🇦"},
    {"name": "Senegal", "flag": "🇸🇳"},
    {"name": "South Africa", "flag": "🇿🇦"},
    {"name": "Tunisia", "flag": "🇹🇳"},
    # CONCACAF
    {"name": "Canada", "flag": "🇨🇦"},
    {"name": "Curaçao", "flag": "🇨🇼"},
    {"name": "Haiti", "flag": "🇭🇹"},
    {"name": "Mexico", "flag": "🇲🇽"},
    {"name": "Panama", "flag": "🇵🇦"},
    {"name": "United States", "flag": "🇺🇸"},
    # CONMEBOL
    {"name": "Argentina", "flag": "🇦🇷"},
    {"name": "Brazil", "flag": "🇧🇷"},
    {"name": "Colombia", "flag": "🇨🇴"},
    {"name": "Ecuador", "flag": "🇪🇨"},
    {"name": "Paraguay", "flag": "🇵🇾"},
    {"name": "Uruguay", "flag": "🇺🇾"},
    # OFC
    {"name": "New Zealand", "flag": "🇳🇿"},
    # UEFA
    {"name": "Austria", "flag": "🇦🇹"},
    {"name": "Belgium", "flag": "🇧🇪"},
    {"name": "Bosnia & Herzegovina", "flag": "🇧🇦"},
    {"name": "Croatia", "flag": "🇭🇷"},
    {"name": "Czech Republic", "flag": "🇨🇿"},
    {"name": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"name": "France", "flag": "🇫🇷"},
    {"name": "Germany", "flag": "🇩🇪"},
    {"name": "Netherlands", "flag": "🇳🇱"},
    {"name": "Norway", "flag": "🇳🇴"},
    {"name": "Portugal", "flag": "🇵🇹"},
    {"name": "Scotland", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿"},
    {"name": "Spain", "flag": "🇪🇸"},
    {"name": "Sweden", "flag": "🇸🇪"},
    {"name": "Switzerland", "flag": "🇨🇭"},
    {"name": "Turkey", "flag": "🇹🇷"},
]

players = []

@app.route('/')
def index():
    return render_template('index.html', teams=WORLD_CUP_TEAMS)

@app.route('/api/players', methods=['GET'])
def get_players():
    return jsonify(players)

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    name = data.get('name', '').strip()
    photo = data.get('photo', '')
    if name:
        player = {"id": len(players) + 1, "name": name, "photo": photo, "teams": []}
        players.append(player)
    return jsonify(players)

@app.route('/api/players/<int:player_id>/assign', methods=['POST'])
def assign_team(player_id):
    data = request.json
    team = data.get('team')
    for p in players:
        if p['id'] == player_id:
            p['teams'].append(team)
            return jsonify(p)
    return jsonify({"error": "Player not found"}), 404

@app.route('/api/players/reset', methods=['POST'])
def reset_players():
    global players
    players = []
    return jsonify(players)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
