import json
import re
import os
import random

#Sprawadzenie importu biblioteki i próba jej automatycznego zainstalowania/pobrania przy starcie
try:
    import customtkinter as ctk
except:
    os.system("pip install customtkinter")
    import customtkinter as ctk

# -*- coding: utf-8 -*-

# Wczytanie pliku bazy słów w formie JSON
def load_json(file):
    with open(file, encoding="utf-8") as bot_responses:
        print(f"Wczytano baze danych: '{file}'")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")

def random_string():
    random_list = [
        "Spróbuj napisać coś bardziej opisowego.",
        "O! Wygląda na to, że napisałeś coś, czego jeszcze nie rozumiem.",
        "Czy mógłbyś spróbować to sformułować inaczej?",
        "Bardzo przepraszam, nie do końca to zrozumiałem.",
        "Nie mogę jeszcze na to odpowiedzieć, spróbuj zadać inne pytanie."
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]

# Funckja odpowiedzialna za zwrócenie najlepszej odpowiedzi poprzez 
# usuniecie znaków interpunkcji i szukaniu słów kluczowych jeżeli
# takie zostały w pliku .json dodatkowo dopisane itp
def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Sprawdza wszystkie odpowiedzi
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Sprawdza czy w zapytaniu są słowa klucz/wymagane/required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Ilość wymaganych słów które mają występować
        if required_score == len(required_words):
            # Sprawdza każde słowo które użytkownik wprowadził
            for word in split_message:
                # Jeżeli słowo jest w odpowiedzi dodaje score
                if word in response["user_input"]:
                    response_score += 1

        # Dodaje zliczone punkty poprawnosci dopasowania szukanego słowa
        score_list.append(response_score)

    # Szuka najlepszej pasujacej slowami odpowiedzi i ja zwraca jezeli suma score nie jest 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Sprawdza i komunikuje o pustym polu (nic nie zostało wpisane do zapytania)
    if input_string == "":
        return "Napisz co kolwiek byśmy mogli porozmawiać :("

    # Jeżeli nie ma dobrej odpowiedzi wylosuje random odpowiedź.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_string()

# Funkcja czyszcząca okno wprowadzania zapytań użytkownika i wyprowadzająca natychmiast 
# wpisane i otrzymane pytanie z opdpowiedzią w textbox o "result" 
def send_function():
    result.configure(state='normal')
    user_input = entry.get()
    result.insert('end','Ty: '+user_input+'\n')
    result.insert('end','Bot: '+get_response(user_input)+'\n',)  
    result.configure(state='disabled')
    entry.delete(0, ctk.END)
    result.see(ctk.END)

#okno GUI za pomoca biblioteki ctk 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title('ChatBOT ver. 1.0')
root.geometry("700x280")
root.resizable(False,False)

#textbox zawierający konwersacje z BOT-em
result = ctk.CTkTextbox(root, font=ctk.CTkFont(size=15))
result.pack(pady=10, fill="x", padx=10)
result.configure(state='normal')
result.insert('end','Witaj w ChatBOT-JSON - Zadaj mi jakieś pytanie.\n')
result.configure(state='disabled')

#input box dla użytkownika do wprowadzania zapytań
entry = ctk.CTkEntry(master=root, height=25,width=500,font=ctk.CTkFont(size=15))
entry.place(y=235,x=50)
entry.bind("<Return>", (lambda event: send_function()))

#przycisk Wyślij 
button = ctk.CTkButton(master=root, text="Wyślij", width=80, height=40,command=send_function)
button.place(y=226,x=560)

#główny loop uruchamiający form'y/GUI biblioteki CTK dzięki której mamy okno GUI
root.mainloop()