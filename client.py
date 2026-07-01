import socket
import json

HOST = "127.0.0.1"
PORT = 5000

class QuizClientCore:
    def __init__(self):
        self.socket = None
        self.student_name = ""
        self.callbacks = {}   # e.g., {"new_question": func, "final_score": func}

    def set_callback(self, event, callback):
        self.callbacks[event] = callback

    def connect(self, student_name):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
            self.student_name = student_name
            self.send_json({"action": "login", "student_name": student_name})
            return True
        except Exception as e:
            raise Exception(f"Connection failed: {e}")
     """dict → JSON string"""
    def send_json(self, obj):
        self.socket.send(json.dumps(obj).encode())

    def recv_json(self):
        data = self.socket.recv(4096).decode()
        if not data:
            return None
        """JSON → dict"""
        return json.loads(data)


    def start_listening(self):
        """Run in a separate thread to receive server messages."""
        try:
            while True:
                msg = self.recv_json()
                if not msg:
                    break
                action = msg.get("action")
                if action == "new_question" and "new_question" in self.callbacks:
                    self.callbacks["new_question"](msg)
                elif action == "final_score" and "final_score" in self.callbacks:
                    self.callbacks["final_score"](msg)
                    break
        except:
            pass

    def submit_answer(self, question_id, answer):
        self.send_json({
            "action": "submit_answer",
            "student_name": self.student_name,
            "question_id": question_id,
            "answer": answer
        })

    def disconnect(self):
        if self.socket:
            self.socket.close()