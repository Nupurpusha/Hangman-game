import tkinter as tk
from tkinter import messagebox
import random

def get_random_word(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
    words = [word.strip() for word in words]
    return random.choice(words)

def get_hangman_stages(filename):
    with open(filename, 'r') as file:
        stages = file.read().split('###')
    return stages

class HangmanGame:
    def __init__(self, master, words_file, stages_file):
        self.master = master
        self.master.title("Hangman Game")
        
        self.word = get_random_word(words_file)
        self.stages = get_hangman_stages(stages_file)
        self.word_letters = set(self.word)
        self.guessed_letters = set()
        self.correct_letters = set()
        self.tries = 6
        
        self.hangman_label = tk.Label(master, text=self.stages[self.tries], font=('Courier', 18))
        self.hangman_label.pack(pady=10)
        
        self.word_label = tk.Label(master, text='_ ' * len(self.word), font=('Courier', 24))
        self.word_label.pack(pady=10)
        
        self.guess_entry = tk.Entry(master, font=('Courier', 16))
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', self.make_guess)
        
        self.message_label = tk.Label(master, text="", font=('Courier', 16))
        self.message_label.pack(pady=10)
        
        self.tries_label = tk.Label(master, text=f"Tries left: {self.tries}", font=('Courier', 16))
        self.tries_label.pack(pady=10)
    
    def make_guess(self, event=None):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="Invalid input. Please guess a single letter.")
            return
        
        if guess in self.guessed_letters:
            self.message_label.config(text="You already guessed that letter.")
            return
        
        self.guessed_letters.add(guess)
        
        if guess in self.word_letters:
            self.correct_letters.add(guess)
            self.message_label.config(text=f"Good job! '{guess}' is in the word.")
        else:
            self.tries -= 1
            self.message_label.config(text=f"Sorry, '{guess}' is not in the word.")
            self.hangman_label.config(text=self.stages[self.tries])
            self.tries_label.config(text=f"Tries left: {self.tries}")
        
        # Display the current state of the word
        current_word = [letter if letter in self.correct_letters else '_' for letter in self.word]
        self.word_label.config(text=" ".join(current_word))
        
        if self.correct_letters == self.word_letters:
            messagebox.showinfo("Hangman", f"Congratulations! You've guessed the word '{self.word}' correctly.")
            self.master.destroy()
        elif self.tries == 0:
            messagebox.showinfo("Hangman", f"Game over! The word was '{self.word}'.")
            self.master.destroy()

if __name__ == "__main__":
    words_file = 'words.txt'
    stages_file = 'stages.txt'
    
    root = tk.Tk()
    hangman_game = HangmanGame(root, words_file, stages_file)
    root.mainloop()
