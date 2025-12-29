from flask import Flask, jsonify, request
from flask_cors import CORS
from Family_tree import FamilyTree
from relation   import find_relation
# =========================
# Flask App
# =========================

app = Flask(__name__)
CORS(app)  # برای ارتباط با HTML

# درخت خانوادگی global
tree = FamilyTree()

# داده‌های اولیه
tree.add_person("حسن", "male")
tree.add_person("فاطمه", "female")
tree.add_person("رضا", "male")
tree.add_person("زهرا", "female")
tree.add_person("علی", "male")
tree.set_father("رضا", "حسن")
tree.set_mother("رضا", "فاطمه")
tree.set_father("زهرا", "حسن")
tree.set_mother("زهرا", "فاطمه")
tree.set_father("علی", "رضا")


@app.route('/api/people', methods=['GET'])
def get_people():
    """دریافت لیست تمام افراد"""
    return jsonify(tree.to_dict())


@app.route('/api/person', methods=['POST'])
def add_person():
    """افزودن فرد جدید"""
    data = request.json
    try:
        tree.add_person(data['name'], data['gender'])
        return jsonify({'success': True, 'message': 'Person added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/father', methods=['POST'])
def set_father():
    """تنظیم پدر"""
    data = request.json
    try:
        tree.set_father(data['child'], data['father'])
        return jsonify({'success': True, 'message': 'Father set successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/mother', methods=['POST'])
def set_mother():
    """تنظیم مادر"""
    data = request.json
    try:
        tree.set_mother(data['child'], data['mother'])
        return jsonify({'success': True, 'message': 'Mother set successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/path', methods=['POST'])
def find_path():
    """پیدا کردن مسیر"""
    data = request.json
    try:
        path = tree.find_path(data['start'], data['end'])
        if path is not None:
            relation_path = find_relation(path)
            return jsonify({'success': True, 'path': relation_path})
        else:
            return jsonify({'success': False, 'error': 'No path found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)