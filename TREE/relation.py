# relation.py

def find_relation(path):
    """
    تبدیل مسیر به نسبت فارسی
    """
    
    if not path:
        return "خودش"
    
    # نقشه اصلی روابط
    relations = {
        # روابط مستقیم
        ('father',): 'پدر',
        ('mother',): 'مادر',
        ('son',): 'پسر',
        ('daughter',): 'دختر',
        
        # پدربزرگ و مادربزرگ
        ('father', 'father'): 'پدربزرگ (پدری)',
        ('father', 'mother'): 'مادربزرگ (پدری)',
        ('mother', 'father'): 'پدربزرگ (مادری)',
        ('mother', 'mother'): 'مادربزرگ (مادری)',
        
        # نوه
        ('son', 'son'): 'نوه پسری',
        ('son', 'daughter'): 'نوه دختری',
        ('daughter', 'son'): 'نوه پسری',
        ('daughter', 'daughter'): 'نوه دختری',
        
        # عمو و عمه
        ('father', 'father', 'son'): 'عمو',
        ('father', 'father', 'daughter'): 'عمه',
        
        # دایی و خاله
        ('mother', 'father', 'son'): 'دایی',
        ('mother', 'father', 'daughter'): 'خاله',
        ('mother', 'mother', 'son'): 'دایی',
        ('mother', 'mother', 'daughter'): 'خاله',
        
        # پسرعمو، دخترعمو
        ('father', 'father', 'son', 'son'): 'پسرعمو',
        ('father', 'father', 'son', 'daughter'): 'دخترعمو',
        ('father', 'father', 'daughter', 'son'): 'پسرعمه',
        ('father', 'father', 'daughter', 'daughter'): 'دخترعمه',
        
        # پسردایی، دختردایی، پسرخاله، دخترخاله
        ('mother', 'father', 'son', 'son'): 'پسردایی',
        ('mother', 'father', 'son', 'daughter'): 'دختردایی',
        ('mother', 'father', 'daughter', 'son'): 'پسرخاله',
        ('mother', 'father', 'daughter', 'daughter'): 'دخترخاله',
        ('mother', 'mother', 'son', 'son'): 'پسردایی',
        ('mother', 'mother', 'son', 'daughter'): 'دختردایی',
        ('mother', 'mother', 'daughter', 'son'): 'پسرخاله',
        ('mother', 'mother', 'daughter', 'daughter'): 'دخترخاله',
        
        # نوه عمو/عمه/دایی/خاله
        ('father', 'father', 'son', 'son', 'son'): 'نوه عمو',
        ('father', 'father', 'son', 'son', 'daughter'): 'نوه عمو',
        ('father', 'father', 'daughter', 'son', 'son'): 'نوه عمه',
        ('mother', 'father', 'son', 'son', 'son'): 'نوه دایی',
        ('mother', 'mother', 'daughter', 'son', 'son'): 'نوه خاله',
        
        # پدربزرگ بزرگ
        ('father', 'father', 'father'): 'پدربزرگ بزرگ',
        ('mother', 'mother', 'mother'): 'مادربزرگ بزرگ',
        
        # نتیجه نوه
        ('son', 'son', 'son'): 'نتیجه (نوه نوه)',
        ('daughter', 'daughter', 'daughter'): 'نتیجه (نوه نوه)',
    }
    
    path_tuple = tuple(path)
    
    # بررسی مطابقت مستقیم
    if path_tuple in relations:
        return relations[path_tuple]
    
    # تحلیل الگوریتمی برای حالت‌های پیچیده
    return analyze_complex_relation(path)


def analyze_complex_relation(path):
    """
    تحلیل روابط پیچیده‌تر که در دیکشنری نیست
    """
    
    up_count = 0  # تعداد بالا رفتن (father/mother)
    down_count = 0  # تعداد پایین آمدن (son/daughter)
    
    # شمارش بالا و پایین
    for step in path:
        if step in ['father', 'mother']:
            up_count += 1
        elif step in ['son', 'daughter']:
            down_count += 1
    
    # پدربزرگ چند نسل بالاتر
    if down_count == 0 and up_count > 0:
        if up_count == 1:
            return 'پدر' if path[0] == 'father' else 'مادر'
        elif up_count == 2:
            if path[0] == 'father' and path[1] == 'father':
                return 'پدربزرگ (پدری)'
            elif path[0] == 'mother' and path[1] == 'mother':
                return 'مادربزرگ (مادری)'
            else:
                return 'پدربزرگ یا مادربزرگ'
        else:
            generation = "بزرگ " * (up_count - 2)
            return f'پدربزرگ {generation}'
    
    # نوه چند نسل پایین‌تر
    if up_count == 0 and down_count > 0:
        if down_count == 1:
            return 'پسر' if path[0] == 'son' else 'دختر'
        elif down_count == 2:
            return 'نوه'
        else:
            generation = "نوه " * (down_count - 1)
            return f'{generation}'
    
    # روابط مرکب (بالا رفتن و پایین آمدن)
    if up_count > 0 and down_count > 0:
        # بررسی الگوی عمو/عمه/دایی/خاله
        if up_count >= 2:
            parent_type = "پدری" if path[0] == 'father' else "مادری"
            sibling_type = ""
            
            # پیدا کردن نقطه برگشت (اولین son/daughter بعد از father/mother ها)
            for i, step in enumerate(path):
                if step in ['son', 'daughter']:
                    if i >= 2:
                        prev_parent = path[0]
                        if prev_parent == 'father':
                            sibling_type = 'عمو' if step == 'son' else 'عمه'
                        else:
                            sibling_type = 'دایی' if step == 'son' else 'خاله'
                    break
            
            # اگر بعد از برادر/خواهر والد، فرزند داشته باشیم
            remaining_downs = down_count - 1
            if remaining_downs == 1 and sibling_type:
                child_type = 'پسر' if path[-1] == 'son' else 'دختر'
                return f'{child_type}{sibling_type}'
            elif remaining_downs > 1 and sibling_type:
                return f'نوه {sibling_type}'
            elif sibling_type:
                return sibling_type
    
    # اگر هیچ الگویی نشناختیم، مسیر را نمایش بده
    persian_steps = []
    persian_map = {
        'father': 'پدر',
        'mother': 'مادر',
        'son': 'پسر',
        'daughter': 'دختر'
    }
    
    for step in path:
        persian_steps.append(persian_map.get(step, step))
    
    return ' '.join(persian_steps)


