from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
todos = []

HTML_TEMPLATE = """
<!doctype html>
<html>
<head><title>To-Do List</title></head>
<body style="font-family: Arial; margin: 40px;">
  <h1>📝 To-Do List</h1>
  <form method="POST" action="/add">
    <input name="task" placeholder="Enter a new task" required>
    <button type="submit">Add</button>
  </form>
  <ul>
    {% for task in todos %}
      <li>{{ loop.index }}. {{ task }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos.append(task)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)