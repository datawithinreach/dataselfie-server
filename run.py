from flask import Flask#, render_template
# from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['PORT'] = 5501



# socketio = SocketIO(app)



# @socketio.on('detect_patterns')
# def detect(data):
# 	G = suggest.from_dict(data)
# 	patterns = suggest.get_hubs(G, nx.pagerank)
# 	patterns = patterns + suggest.get_cliques(G)
# 	patterns = patterns + suggest.get_communities(G)
# 	patterns = patterns + suggest.get_articulation_points(G)
# 	patterns1 = suggest.prune_patterns(G,patterns)
# 	patterns2 = suggest.rank_patterns(G, patterns1, data['highlights'])
	
# 	socketio.emit('patterns', patterns2)
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
	# socketio.run(app, port=app.config['PORT'], host='0.0.0.0', debug=True)
	app.run(port=9999, debug=True)