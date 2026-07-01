import customtkinter as ctk
from tkinter import messagebox
import threading
from client import QuizClientCore

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuizClient:
    def __init__(self):
        self.core = QuizClientCore()
        self.current_question_id = 0
        self.total_questions = 0

        self.root = ctk.CTk()
        self.root.title("Online Quiz Client")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.selected_answer = ctk.StringVar(master=self.root)

        self.create_login_frame()
        self.create_quiz_frame()
        self.show_login()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_quiz)
        self.root.mainloop()

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="🎯 ONLINE QUIZ SYSTEM", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=40)
        self.name_entry = ctk.CTkEntry(self.login_frame, width=300, height=40, placeholder_text="Enter your name")
        self.name_entry.pack(pady=20)
        self.name_entry.bind("<Return>", lambda e: self.connect())

        self.connect_btn = ctk.CTkButton(self.login_frame, text="Start Quiz", command=self.connect, height=45, fg_color="#2E7D32", hover_color="#1B5E20")
        self.connect_btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self.login_frame, text="")
        self.status_label.pack()

    def create_quiz_frame(self):
        self.quiz_frame = ctk.CTkFrame(self.root)

        header = ctk.CTkFrame(self.quiz_frame)
        header.pack(fill="x", padx=20, pady=20)
        self.progress_label = ctk.CTkLabel(header, text="Question 0 / 0", font=ctk.CTkFont(size=16, weight="bold"))
        self.progress_label.pack(side="left")
        self.name_label = ctk.CTkLabel(header, text="")
        self.name_label.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(self.quiz_frame)
        self.progress_bar.pack(fill="x", padx=20)
        self.progress_bar.set(0)

        self.question_label = ctk.CTkLabel(self.quiz_frame, text="", wraplength=620, justify="left", font=ctk.CTkFont(size=18))
        self.question_label.pack(padx=20, pady=30)

        self.options_frame = ctk.CTkFrame(self.quiz_frame, fg_color="transparent")
        self.options_frame.pack(pady=10)

        self.submit_btn = ctk.CTkButton(self.quiz_frame, text="Submit Answer", command=self.submit_answer, height=45, state="disabled")
        self.submit_btn.pack(pady=20)

        ctk.CTkButton(self.quiz_frame, text="Exit", command=self.exit_quiz, fg_color="gray").pack(pady=10)

    def show_login(self):
        self.quiz_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_quiz(self):
        self.login_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)

    def connect(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter your name.")
            return
        try:
            self.core.connect(name)
            self.name_label.configure(text=f"👤 {name}")
            self.status_label.configure(text="Connected successfully!", text_color="green")

            self.core.set_callback("new_question", self.display_question)
            self.core.set_callback("final_score", self.show_results)

            threading.Thread(target=self.core.start_listening, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def display_question(self, data):
        self.root.after(0, self._display_question, data)

    def _display_question(self, data):
        self.show_quiz()
        self.current_question_id = data["question_id"]
        self.total_questions = data["total"]
        self.progress_label.configure(text=f"Question {self.current_question_id} / {self.total_questions}")
        self.progress_bar.set(self.current_question_id / self.total_questions)
        self.question_label.configure(text=data["text"])

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.selected_answer.set("")
        for option in data["options"]:
            ctk.CTkRadioButton(self.options_frame, text=option, variable=self.selected_answer, value=option).pack(anchor="w", pady=5)
        self.submit_btn.configure(state="normal")

    def submit_answer(self):
        answer = self.selected_answer.get()
        if not answer:
            messagebox.showwarning("Warning", "Please select an answer.")
            return
        self.submit_btn.configure(state="disabled")
        self.core.submit_answer(self.current_question_id, answer)

    def show_results(self, data):
        self.root.after(0, self._show_results, data)

    def _show_results(self, data):
        score = data["score"]
        total = data["total"]
        percent = (score / total * 100) if total > 0 else 0
        if percent >= 80:
            msg = "🏆 Excellent!"
        elif percent >= 60:
            msg = "👍 Good Job!"
        elif percent >= 40:
            msg = "📚 Keep Studying!"
        else:
            msg = "💪 Better Luck Next Time!"
        result_text = f"{data['message']}\n\nScore: {score} / {total}\nPercentage: {percent:.1f}%\n\n{msg}"
        messagebox.showinfo("Quiz Completed", result_text)
        self.exit_quiz()

    def exit_quiz(self):
        self.core.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    QuizClient()