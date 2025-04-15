import tkinter as tk
import tkinter.font as tkFont
import json
import os

# 스크립트 파일의 절대 경로를 얻고, 그 경로에 todo.json 파일 이름을 결합
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TODO_FILE = os.path.join(SCRIPT_DIR, "todo.json")

todo_list = []

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            try:
                loaded_tasks = json.load(f)
                for task_data in loaded_tasks:
                    done_var = tk.BooleanVar(value=task_data["done"])
                    todo_list.append({"task": task_data["task"], "done": task_data["done"], "done_var": done_var})
            except json.JSONDecodeError:
                print("할 일 목록 파일 내용이 올바르지 않습니다.")
    update_task_list()

def save_tasks():
    tasks_to_save = [{"task": task["task"], "done": task["done"]} for task in todo_list]
    with open(TODO_FILE, "w") as f:
        json.dump(tasks_to_save, f)

def add_task():
    task_text = entry.get()
    if not task_text:
        return

    done_var = tk.BooleanVar()
    task = {"task": task_text, "done": False, "done_var": done_var}
    todo_list.append(task)
    update_task_list()
    entry.delete(0, tk.END)

def delete_task(task):
    todo_list.remove(task)
    update_task_list()

def toggle_task(task):
    task["done"] = task["done_var"].get()
    update_task_list() # 체크박스 상태 변경 시 목록 업데이트

def update_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    strike_font = tkFont.Font(overstrike=1)  # 취소선 폰트 생성
    normal_font = tkFont.Font() # 기본 폰트 생성

    for task in todo_list:
        frame = tk.Frame(task_frame)

        checkbox = tk.Checkbutton(frame, variable=task["done_var"], command=lambda t=task: toggle_task(t))
        checkbox.pack(side=tk.LEFT)
        checkbox.select() if task["done"] else checkbox.deselect()

        label_font = strike_font if task["done"] else normal_font
        label = tk.Label(frame, text=task["task"], font=label_font) # 폰트 적용
        label.pack(side=tk.LEFT)

        delete_button = tk.Button(frame, text="삭제", command=lambda t=task: delete_task(t))
        delete_button.pack(side=tk.RIGHT)

        frame.pack(anchor="w")
def on_closing():
    save_tasks()
    root.destroy()

# 기본 GUI 설정
root = tk.Tk()
root.title("To-Do List")

task_frame = tk.Frame(root)
task_frame.pack(pady=10)


# 창 닫기 이벤트 처리
root.protocol("WM_DELETE_WINDOW", on_closing)

# 할 일 목록 불러오기
load_tasks()

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

add_button = tk.Button(root, text="할 일 추가", command=add_task)
add_button.pack()

# 종료 버튼 추가
exit_button = tk.Button(root, text="종료", command=on_closing)
exit_button.pack()


root.mainloop()