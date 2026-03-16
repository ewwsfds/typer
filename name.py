import pyautogui
import pyperclip
import time
import random
import sys
import re
import threading
import tkinter as tk
import os

TEXT_FILE = "text.txt"
PROGRESS_FILE = "progress.txt"

stop_flag = False


# ------------------ Stop Window ------------------ #
def stop_window():
    global stop_flag
    root = tk.Tk()
    root.title("Typer Running")
    root.geometry("220x100")
    root.attributes("-topmost", True)

    def stop():
        global stop_flag
        stop_flag = True
        root.destroy()

    btn = tk.Button(root, text="End Code", command=stop, height=2, width=15)
    btn.pack(expand=True)

    root.mainloop()


# ------------------ Helpers ------------------ #
def parse_range(arg):
    parts = arg.split("-")
    return int(parts[0]), int(parts[1])


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))


def split_sentences(text):
    sentences = re.split(r'(?<=[.!,?])\s+', text)
    return sentences


def type_character(c):
    if c in "åäöÅÄÖ":
        pyperclip.copy(c)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.write(c)
    time.sleep(0.25)


# ------------------ Typing Logic ------------------ #
def type_text(sentences, sentence_range, break_range, start_index):
    global stop_flag
    sentence_count = 0
    next_pause = random.randint(*sentence_range)

    index = start_index

    for i in range(start_index, len(sentences)):
        if stop_flag:
            save_progress(index)
            return

        sentence = sentences[i]

        for c in sentence:
            if stop_flag:
                save_progress(index)
                return
            type_character(c)

        pyautogui.write(" ")
        sentence_count += 1
        index += 1
        save_progress(index)

        if sentence_count >= next_pause:
            pause_time = random.uniform(*break_range)
            time.sleep(pause_time)
            sentence_count = 0
            next_pause = random.randint(*sentence_range)


# ------------------ Main ------------------ #
def main():
    global stop_flag

    if len(sys.argv) < 2:
        print("Usage:")
        print("python typer.py 2-4 6-8")
        print("python typer.py continue")
        return

    if sys.argv[1].lower() == "continue":
        sentence_range = (2, 4)
        break_range = (6, 8)
        start_index = load_progress()
    else:
        sentence_range = parse_range(sys.argv[1])
        break_range = parse_range(sys.argv[2])
        start_index = 0
        save_progress(0)

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = split_sentences(text)

    # Start stop window thread
    threading.Thread(target=stop_window, daemon=True).start()

    print("Starting in 7 seconds... switch to target window.")
    time.sleep(7)

    type_text(sentences, sentence_range, break_range, start_index)

    if not stop_flag:
        save_progress(0)
        print("Finished typing.")


if __name__ == "__main__":
    main()
