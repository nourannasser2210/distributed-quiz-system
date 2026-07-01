import socket
import threading
import json
' current time of logs'
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

class QuizServerCore:
    def __init__(self):
        self.quiz = []
        self.clients = {}
        self.results = []
        self.lock = threading.Lock()
        self.server_running = True
        self.log_callback = None   # to send logs to GUI

    def set_log_callback(self, callback):
        """Register a function to receive log messages."""
        self.log_callback = callback

    def log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"[{timestamp}] {text}"
        if self.log_callback:
            self.log_callback(msg)
        else:
            print(msg)

    def add_question(self, q_data):
        with self.lock:
            self.quiz.append(q_data)
        self.log("Question added.")

    def delete_question(self, index):
        with self.lock:
            if 0 <= index < len(self.quiz):
                del self.quiz[index]
                self.log(f"Deleted question #{index+1}")
                return True
        return False

    def get_quiz_copy(self):
        with self.lock:
            return [q.copy() for q in self.quiz]

    def get_questions_list(self):
        with self.lock:
            return [f"{i+1}. [{q['type']}] {q['question'][:80]}" 
                    for i, q in enumerate(self.quiz)]

    def get_clients_status(self):
        with self.lock:
            return {name: info["status"] for name, info in self.clients.items()}

    def get_results_summary(self):
        with self.lock:
            return [{"name": r["name"], "score": r["score"], 
                     "total": r["total"], "percent": r["percent"]} 
                    for r in self.results[-50:]]

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)
        self.log(f"Server started on {HOST}:{PORT}")

        while self.server_running:
            try:
                conn, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except:
                break
        server.close()

    def recv_json(self, conn):
        data = conn.recv(4096)
        if not data:
            return None
        return json.loads(data.decode())

    def send_json(self, conn, obj):
        conn.send(json.dumps(obj).encode())

    def handle_client(self, conn, addr):
        student_name = "Unknown"
        try:
            login = self.recv_json(conn)
            if not login or login.get("action") != "login":
                conn.close()
                return
            student_name = login.get("student_name", "Unknown")
            with self.lock:
                self.clients[student_name] = {"status": "Connected", "address": addr}
            self.log(f"{student_name} connected from {addr}")

            current_quiz = self.get_quiz_copy()
            if not current_quiz:
                self.send_json(conn, {"action": "final_score", "score": 0, "total": 0, "message": "No questions available."})
                return

            total = len(current_quiz)
            score = 0
            for i, q in enumerate(current_quiz, start=1):
                with self.lock:
                    self.clients[student_name]["status"] = f"Answering {i}/{total}"
                self.send_json(conn, {
                    "action": "new_question",
                    "question_id": i,
                    "total": total,
                    "text": q["question"],
                    "options": q["options"]
                })
                answer_data = self.recv_json(conn)
                if not answer_data:
                    return
                user_answer = answer_data.get("answer", "").strip().upper()
                correct = q["answer"].strip().upper()
                if user_answer and user_answer[0] == correct[0]:
                    score += 1
                threading.Event().wait(1)

            percent = (score / total) * 100
            self.send_json(conn, {"action": "final_score", "score": score, "total": total, "message": "Quiz completed!"})
            with self.lock:
                self.clients[student_name]["status"] = "Completed"
                self.results.append({"name": student_name, "score": score, "total": total, "percent": percent})
            self.log(f"{student_name} completed quiz: {score}/{total} ({percent:.1f}%)")
        except Exception as e:
            self.log(f"Error with {student_name}: {e}")
        finally:
            with self.lock:
                if student_name in self.clients:
                    self.clients[student_name]["status"] = "Disconnected"
            conn.close()

    def stop_server(self):
        self.server_running = False