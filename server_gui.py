import customtkinter as ctk
from tkinter import messagebox
import threading
from server import QuizServerCore

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuizServerApp:
    def __init__(self):
        self.core = QuizServerCore()
        self.core.set_log_callback(self.log)

        self.selected_question = None
        self.root = ctk.CTk()
        self.root.title("Distributed Quiz System - Server Dashboard")
        self.root.geometry("1200x800")

        self.build_gui()

        self.server_thread = threading.Thread(target=self.core.start_server, daemon=True)
        self.server_thread.start()

        self.refresh_question_list()
        self.refresh_clients()
        self.refresh_results()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def build_gui(self):
        title = ctk.CTkLabel(self.root, text="🎓 DISTRIBUTED QUIZ SYSTEM - SERVER", font=ctk.CTkFont(size=30, weight="bold"))
        title.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.root, text=f"🟢 Server Running on 127.0.0.1:5000", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)

        main = ctk.CTkFrame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT PANEL
        left = ctk.CTkFrame(main)
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(left, text="➕ Add Question", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        self.q_type = ctk.StringVar(value="MCQ")
        type_frame = ctk.CTkFrame(left)
        type_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkRadioButton(type_frame, text="Multiple Choice", variable=self.q_type, value="MCQ", command=self.toggle_fields).pack(side="left", padx=10, pady=10)
        ctk.CTkRadioButton(type_frame, text="True / False", variable=self.q_type, value="TF", command=self.toggle_fields).pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(left, text="Question").pack(anchor="w", padx=20)
        self.question_text = ctk.CTkTextbox(left, height=100)
        self.question_text.pack(fill="x", padx=20, pady=5)

        self.mcq_frame = ctk.CTkFrame(left)
        self.mcq_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.mcq_frame, text="Options (one per line, e.g. A) Cairo)").pack(anchor="w", padx=10, pady=5)
        self.mcq_options = ctk.CTkTextbox(self.mcq_frame, height=100)
        self.mcq_options.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.mcq_frame, text="Correct Answer (A/B/C)").pack(anchor="w", padx=10)
        self.mcq_answer = ctk.CTkEntry(self.mcq_frame, width=80)
        self.mcq_answer.pack(anchor="w", padx=10, pady=5)

        self.tf_frame = ctk.CTkFrame(left)
        ctk.CTkLabel(self.tf_frame, text="Correct Answer").pack(anchor="w", padx=10, pady=5)
        self.tf_answer = ctk.CTkComboBox(self.tf_frame, values=["TRUE", "FALSE"], width=100)
        self.tf_answer.pack(anchor="w", padx=10, pady=5)
        self.tf_answer.set("TRUE")

        btn_frame = ctk.CTkFrame(left)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Add Question", command=self.add_question, fg_color="#2E7D32", hover_color="#1B5E20").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_question, fg_color="#C62828", hover_color="#B71C1C").pack(side="left", padx=5)

        ctk.CTkLabel(left, text="📋 Questions", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10,5))
        self.question_list = ctk.CTkScrollableFrame(left, height=300)
        self.question_list.pack(fill="both", expand=True, padx=10, pady=5)

        # RIGHT PANEL
        right = ctk.CTkFrame(main, width=450)
        right.pack(side="right", fill="both", padx=5, pady=5)

        ctk.CTkLabel(right, text="👥 Logged-in Clients", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        self.clients_frame = ctk.CTkScrollableFrame(right, height=220)
        self.clients_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(right, text="🏆 Completed Results", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        self.results_frame = ctk.CTkScrollableFrame(right, height=220)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(right, text="📝 Live Logs", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        self.log_box = ctk.CTkTextbox(right, height=180)
        self.log_box.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_box.configure(state="disabled")

        self.toggle_fields()

    def log(self, text):
        self.root.after(0, self._append_log, text + "\n")

    def _append_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def toggle_fields(self):
        if self.q_type.get() == "MCQ":
            self.tf_frame.pack_forget()
            self.mcq_frame.pack(fill="x", padx=20, pady=10)
        else:
            self.mcq_frame.pack_forget()
            self.tf_frame.pack(fill="x", padx=20, pady=10)

    def clear_fields(self):
        self.question_text.delete("1.0", "end")
        self.mcq_options.delete("1.0", "end")
        self.mcq_answer.delete(0, "end")
        self.tf_answer.set("TRUE")

    def add_question(self):
        question = self.question_text.get("1.0", "end").strip()
        if not question:
            messagebox.showwarning("Warning", "Enter a question.")
            return

        if self.q_type.get() == "MCQ":
            options_text = self.mcq_options.get("1.0", "end").strip()
            answer = self.mcq_answer.get().strip().upper()
            if not options_text or answer not in ["A", "B", "C"]:
                messagebox.showwarning("Warning", "Enter options and answer A/B/C.")
                return
            options = [line.strip() for line in options_text.splitlines() if line.strip()]
            self.core.add_question({
                "type": "MCQ",
                "question": question,
                "options": options,
                "answer": answer
            })
        else:
            answer = self.tf_answer.get().strip().upper()
            self.core.add_question({
                "type": "TF",
                "question": question,
                "options": ["TRUE", "FALSE"],
                "answer": answer
            })
        self.refresh_question_list()
        self.clear_fields()

    def refresh_question_list(self):
        for widget in self.question_list.winfo_children():
            widget.destroy()
        questions = self.core.get_questions_list()
        for i, text in enumerate(questions):
            label = ctk.CTkLabel(self.question_list, text=text, anchor="w", justify="left")
            label.pack(fill="x", padx=5, pady=2)
            label.bind("<Button-1>", lambda e, idx=i: self.select_question(idx))

    def select_question(self, index):
        self.selected_question = index
        self.log(f"Selected question #{index+1}")

    def delete_question(self):
        if self.selected_question is None:
            messagebox.showwarning("Warning", "Select a question.")
            return
        if self.core.delete_question(self.selected_question):
            self.selected_question = None
            self.refresh_question_list()

    def refresh_clients(self):
        for widget in self.clients_frame.winfo_children():
            widget.destroy()
        clients_status = self.core.get_clients_status()
        if not clients_status:
            ctk.CTkLabel(self.clients_frame, text="No clients connected.").pack(anchor="w", padx=5, pady=2)
        else:
            for name, status in clients_status.items():
                ctk.CTkLabel(self.clients_frame, text=f"👤 {name} - {status}", anchor="w").pack(fill="x", padx=5, pady=2)
        self.root.after(1000, self.refresh_clients)

    def refresh_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        results = self.core.get_results_summary()
        if not results:
            ctk.CTkLabel(self.results_frame, text="No completed results.").pack(anchor="w", padx=5, pady=2)
        else:
            for r in reversed(results):
                ctk.CTkLabel(self.results_frame, text=f"🏅 {r['name']} : {r['score']}/{r['total']} ({r['percent']:.1f}%)", anchor="w").pack(fill="x", padx=5, pady=2)
        self.root.after(1000, self.refresh_results)

    def on_close(self):
        self.core.stop_server()
        self.root.destroy()

if __name__ == "__main__":
    QuizServerApp()