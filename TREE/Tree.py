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
# نسل 0 (ریشه‌ی خاندان)
tree.add_person("کریم", "male")
tree.add_person("طاهره", "female")

# نسل 1 (فرزندان کریم)
tree.add_person("حسن", "male")
tree.add_person("مریم", "female")
tree.add_person("اکبر", "male")

tree.set_father("حسن", "کریم")
tree.set_mother("حسن", "طاهره")

tree.set_father("مریم", "کریم")
tree.set_mother("مریم", "طاهره")

tree.set_father("اکبر", "کریم")
tree.set_mother("اکبر", "طاهره")

# نسل 2 (نوه‌ها)
tree.add_person("رضا", "male")
tree.add_person("زهرا", "female")
tree.add_person("سعید", "male")
tree.add_person("لیلا", "female")
tree.add_person("حمید", "male")

tree.set_father("رضا", "حسن")
tree.set_mother("رضا", "مریم")

tree.set_father("زهرا", "حسن")
tree.set_mother("زهرا", "مریم")

tree.set_father("سعید", "اکبر")
tree.set_mother("سعید", "لیلا")

tree.set_father("حمید", "اکبر")
tree.set_mother("حمید", "لیلا")

# نسل 3 (نتیجه‌ها)
tree.add_person("علی", "male")
tree.add_person("نگار", "female")
tree.add_person("پارسا", "male")

tree.set_father("علی", "رضا")
tree.set_mother("علی", "زهرا")

tree.set_father("نگار", "رضا")
tree.set_mother("نگار", "زهرا")

tree.set_father("پارسا", "سعید")
tree.set_mother("پارسا", "نگار")

# نسل 4 (نوه‌ی نوه)
tree.add_person("آرین", "male")
tree.set_father("آرین", "علی")



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


# @app.route('/api/path', methods=['POST'])
# def find_path():
#     """پیدا کردن مسیر"""
#     data = request.json
#     try:
#         path = tree.find_path(data['start'], data['end'])
#         if path is not None:
#             relation_path = find_relation(path)
#             return jsonify({'success': True, 'path': relation_path})
#         else:
#             return jsonify({'success': False, 'error': 'No path found'})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/path', methods=['POST'])
def find_path():
    """پیدا کردن مسیر"""
    data = request.json
    try:
        path = tree.find_path(data['start'], data['end'])
        if path is not None:
            relation_text = find_relation(path)  # این یک string است
            
            # برگرداندن هم مسیر و هم نسبت
            return jsonify({
                'success': True, 
                'path': relation_text,  # نسبت فارسی
                'raw_path': path  # مسیر اصلی
            })
        else:
            return jsonify({'success': False, 'error': 'No path found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)