import tkinter as tk
import threading
import time

# Глобальные переменные
windows = {}
elements = {}
button_states = {}  # Храним состояние кнопок

def interface_new(window_name):
    if window_name in windows:
        return False
    
    windows[window_name] = {
        'name': window_name,
        'width': 300,
        'height': 200,
        'title': window_name,
        'bg_color': '#2c3e50',
        'running': False,
        'tk_window': None
    }
    return True

def interface_set_settings(window_name, width, height, x, y, window_type, title):
    if window_name not in windows:
        return False
    
    windows[window_name]['width'] = int(width)
    windows[window_name]['height'] = int(height)
    windows[window_name]['title'] = title
    return True

def interface_set_bg(window_name, color):
    if window_name not in windows:
        return False
    
    windows[window_name]['bg_color'] = color
    return True

def interface_create_Button(window_name, element_name, x, y, width, height, color, editable):
    return _create_element('Button', window_name, element_name, x, y, width, height, color, editable)

def interface_create_Text(window_name, element_name, x, y, width, height, color, editable):
    return _create_element('Text', window_name, element_name, x, y, width, height, color, editable)

def _create_element(element_type, window_name, element_name, x, y, width, height, color, editable):
    if window_name not in windows:
        return False
    
    element_key = f"{window_name}_{element_name}"
    
    elements[element_key] = {
        'type': element_type,
        'window': window_name,
        'name': element_name,
        'x': int(x),
        'y': int(y),
        'width': int(width),
        'height': int(height),
        'color': color,
        'text': '',
        'widget': None,
        'tk_var': None
    }
    
    # Для кнопок создаем состояние
    if element_type == 'Button':
        button_states[element_key] = {'clicked': False}
    
    return True

# Простой обработчик клика
def _make_click_handler(element_key):
    def handler(event=None):
        button_states[element_key]['clicked'] = True
    return handler

def _create_tkinter_window(window_name):
    try:
        window = windows[window_name]
        
        root = tk.Tk()
        root.title(window['title'])
        root.geometry(f"{window['width']}x{window['height']}")
        root.configure(bg=window['bg_color'])
        
        def on_closing():
            window['running'] = False
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        window['tk_window'] = root
        window['running'] = True
        
        # Создаем элементы
        for element_key, element in elements.items():
            if element['window'] == window_name:
                if element['type'] == 'Button':
                    btn = tk.Button(
                        root,
                        text=element['text'],
                        bg=element['color'],
                        fg='white',
                        font=('Arial', 12),
                        command=_make_click_handler(element_key)
                    )
                    btn.place(x=element['x'], y=element['y'], 
                             width=element['width'], height=element['height'])
                    element['widget'] = btn
                    
                elif element['type'] == 'Text':
                    text_var = tk.StringVar()
                    text_var.set(element['text'])
                    
                    label = tk.Label(
                        root,
                        textvariable=text_var,
                        bg=root.cget('bg'),
                        fg=element['color'],
                        font=('Arial', 12)
                    )
                    label.place(x=element['x'], y=element['y'],
                               width=element['width'], height=element['height'])
                    element['widget'] = label
                    element['tk_var'] = text_var
        
        root.mainloop()
        
        window['running'] = False
        
    except Exception as e:
        print(f"Ошибка: {e}")

def interface_run(window_name):
    if window_name not in windows:
        return False
    
    if windows[window_name]['running']:
        return True
    
    thread = threading.Thread(target=_create_tkinter_window, args=(window_name,))
    thread.daemon = True
    thread.start()
    
    time.sleep(0.5)
    return windows[window_name]['running']

def interface_close(window_name):
    if window_name in windows and windows[window_name]['tk_window']:
        try:
            windows[window_name]['tk_window'].destroy()
        except:
            pass
    
    if window_name in windows:
        windows[window_name]['running'] = False
    
    return True

def interface_update():
    return True

def interface_is_running(window_name):
    return window_name in windows and windows[window_name]['running']

def interface_get_text(window_name, element_name):
    element_key = f"{window_name}_{element_name}"
    if element_key in elements:
        return elements[element_key].get('text', '')
    return ""

def interface_set_text(window_name, element_name, text):
    element_key = f"{window_name}_{element_name}"
    
    if element_key in elements:
        elements[element_key]['text'] = str(text)
        
        widget = elements[element_key].get('widget')
        tk_var = elements[element_key].get('tk_var')
        
        if widget:
            try:
                if elements[element_key]['type'] == 'Button':
                    widget.config(text=str(text))
                elif elements[element_key]['type'] == 'Text' and tk_var:
                    tk_var.set(str(text))
            except:
                pass
        
        return True
    
    return False

def interface_is_button_clicked(window_name, element_name):
    """Проверяет, была ли нажата кнопка с момента последней проверки"""
    element_key = f"{window_name}_{element_name}"
    
    # Проверяем, что элемент существует и является кнопкой
    if element_key in elements and elements[element_key]['type'] == 'Button':
        if element_key in button_states:
            if button_states[element_key]['clicked']:
                button_states[element_key]['clicked'] = False
                return True
    
    return False


def add_numbers(a, b):
    return float(a) + float(b)

def repeat_string(text, times):
    return str(text) * int(times)

def parse_expression(expr):
    try:
        return eval(str(expr))
    except:
        return None

def format_output(text, style="default"):
    return str(text)




