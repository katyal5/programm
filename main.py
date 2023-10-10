import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import os


current_directory = os.path.dirname(os.path.abspath(__file__))


FILE_PATH = os.path.join(current_directory, "daily_notes.txt")


daily_notes = {}

def save_notes():
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        for date, notes in daily_notes.items():
            file.write(f"{date}::{';'.join(notes)}\n")

def load_notes():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if "::" in line:
                    date, notes = line.strip().split("::")
                    daily_notes[date] = notes.split(";")
                else:
                    print(f"Некорректный формат строки в файле: {line}")


def add_note():
    date = calendar.get_date()
    note = note_entry.get("1.0", tk.END).strip()
    if note:
        if date in daily_notes:
            daily_notes[date].append(note)
        else:
            daily_notes[date] = [note]
        messagebox.showinfo("Успех", "Заметка успешно добавлена!")
        note_entry.delete("1.0", tk.END)
        save_notes()
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите заметку.")

def show_notes():
    date = calendar.get_date()
    notes = daily_notes.get(date, ["Нет заметок для этой даты."])
    notes_listbox.delete(0, tk.END)
    for note in notes:
        notes_listbox.insert(tk.END, note)

def delete_note():
    selected_note_indices = notes_listbox.curselection()
    if not selected_note_indices:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите заметку для удаления.")
    else:
        selected_note_index = selected_note_indices[0]
        selected_note = notes_listbox.get(selected_note_index)
        date = calendar.get_date()
        if date in daily_notes and selected_note in daily_notes[date]:
            daily_notes[date].remove(selected_note)
            messagebox.showinfo("Успех", "Заметка удалена успешно!")
            show_notes()
            save_notes()

def edit_note():
    selected_note_index = notes_listbox.curselection()
    if not selected_note_index:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите заметку для изменения.")
    else:
        selected_note_index = selected_note_index[0]
        selected_note = notes_listbox.get(selected_note_index)
        new_note = edit_entry.get("1.0", tk.END).strip()
        date = calendar.get_date()
        if date in daily_notes and selected_note in daily_notes[date]:
            index = daily_notes[date].index(selected_note)
            daily_notes[date][index] = new_note
            messagebox.showinfo("Успех", "Заметка успешно изменена!")
            show_notes()
            save_notes()

root = tk.Tk()
root.title("Ежедневник")

calendar = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd", locale='ru_RU')
calendar.pack(padx=20, pady=20)

note_label = tk.Label(root, text="Введите заметку:")
note_label.pack()
note_entry = tk.Text(root, height=5, width=40)
note_entry.pack()

add_button = tk.Button(root, text="Добавить заметку", command=add_note, width=20)
add_button.pack(pady=10)

show_button = tk.Button(root, text="Показать заметки", command=show_notes, width=20)
show_button.pack(pady=10)

delete_label = tk.Label(root, text="Выберите заметку для удаления:")
delete_label.pack()

notes_listbox = tk.Listbox(root, height=10, width=40)
notes_listbox.pack()

delete_button = tk.Button(root, text="Удалить заметку", command=delete_note, width=20)
delete_button.pack(pady=10)

edit_label = tk.Label(root, text="Введите новую заметку:")
edit_label.pack()
edit_entry = tk.Text(root, height=5, width=40)
edit_entry.pack()

edit_button = tk.Button(root, text="Изменить заметку", command=edit_note, width=20)
edit_button.pack(pady=10)


# Загрузка заметок из файла при запуске
load_notes()

root.mainloop()


