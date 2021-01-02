import matplotlib.pyplot as plt
import multiprocessing
import tkinter as tk
import cv2
import pdfgen
import numpy as np
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from fer import FER
import pandas as pd
import threading
import matplotlib
matplotlib.use('Agg')

input_dict = {'sample': 'value'}
detector = FER(mtcnn=True)
e = multiprocessing.Event()
p = None


def generate_graphs(emo_list):
    # print(type(emo_list[0]))
    # emo_list = ['neutral', 'disgust', 'neutral', 'sad', 'neutral', 'happy', 'neutral',
    #             'angry', 'surprise', 'fear', 'fear', 'happy', 'disgust', 'neutral', 'neutral', ]
    df = pd.DataFrame(emo_list, columns=['emotions'])
    em_df = pd.DataFrame(df.value_counts().reset_index())
    em_df.columns = em_df.columns.map(str)
    labels = em_df['emotions'].unique()
    fig1, ax1 = plt.subplots()
    ax1.pie(em_df['0'],  labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    plt.show()
    plt.savefig('emograph.png')
    # print("Maybe:::", em_df['emotions'][1])
    return em_df['emotions']
    # print("Your dominant emotion during the session was",
    #       em_df['emotions'][0], "followed by", em_df['emotions'][1])


def startrecording(e):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('cache.avi', fourcc, 20.0, (640, 480))

    while(True):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
        else:
            break


def start_recording_proc():
    global p
    p = multiprocessing.Process(target=startrecording, args=(e,))
    p.start()


def process_output():
    emotions_list_raw = []
    cap = cv2.VideoCapture('cache.avi')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            try:
                result, _ = detector.top_emotion(frame)
                emotions_list_raw.append(result)
                # print(result)
            except:
                print("Face Not found  in frame")
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    if not emotions_list_raw:
        print("List is empty")
    # print("\n\n", emotions_list_raw)

    emotions_detected = generate_graphs(emotions_list_raw)
    # print(input_dict)
    pdfgen.gen(emotions_detected, input_dict)
    print("Report generated")


def stoprecording():
    e.set()
    p.join()
    # print(input_dict)
    threading.Thread(target=process_output()).start()


class window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tkinter.Label(text="Emo.ai").pack()

        self.name_var = tk.StringVar()
        self.q1 = Label(text="1. How would you like us to call you?").pack()
        self.q1_user_input = tk.Entry(
            root, textvariable=self.name_var)
        self.q1_user_input.pack()

        self.q2 = Label(
            text="2. How often do you communicate with people close to you").pack()
        self.q2_n = tk.StringVar()
        self.q2_user_input = ttk.Combobox(width=35, textvariable=self.q2_n)
        self.q2_user_input['values'] = [
            'Daily', 'Once or twice in a week', 'Once in a while', 'Never']
        self.q2_user_input.pack()

        self.q3 = Label(
            text="3. Has there been any change in your appetite?").pack()
        self.q3_n = tk.StringVar()
        self.q3_user_input = ttk.Combobox(width=27, textvariable=self.q3_n)
        self.q3_user_input['values'] = ['Yes', 'No']
        self.q3_user_input.pack()

        self.q4 = Label(
            text="4. Are you able to find time for yourself and engage in activities you like?").pack()
        self.q4_n = tk.StringVar()
        self.q4_user_input = ttk.Combobox(width=50, textvariable=self.q4_n)
        self.q4_user_input['values'] = [
            'No, I never find spare time ', 'I do get time but have no interest in such activities nowadays',
            'Yes, I always find time and enjoy doing things I like']
        self.q4_user_input.pack()

        self.q5 = Label(
            text="5. Do you consider yourself happy?").pack()
        self.q5_n = tk.StringVar()
        self.q5_user_input = ttk.Combobox(width=27, textvariable=self.q5_n)
        self.q5_user_input['values'] = ['Yes', 'No']
        self.q5_user_input.pack()

        self.q6 = Label(
            text="6. Does the thought of tomorrow make you worry?").pack()
        self.q6_n = tk.StringVar()
        self.q6_user_input = ttk.Combobox(width=50, textvariable=self.q6_n)
        self.q6_user_input['values'] = [
            'Yes, always worry about what will happen tomorrow', 'No, I am always excited of what will happen tomorrow']
        self.q6_user_input.pack()

        self.q7 = Label(
            text="7. Are you having trouble with concentrating in your work?").pack()
        self.q7_n = tk.StringVar()
        self.q7_user_input = ttk.Combobox(width=27, textvariable=self.q7_n)
        self.q7_user_input['values'] = ['No, I am fine', 'Yes, I do']
        self.q7_user_input.pack()

        self.q8 = Label(
            text="8. How often have you felt difficulties were piling up so high that you could not overcome them?").pack()
        self.q8_n = tk.StringVar()
        self.q8_user_input = ttk.Combobox(width=27, textvariable=self.q8_n)
        self.q8_user_input['values'] = ['Never', 'Often', 'Always']
        self.q8_user_input.pack()

        self.q9_user_input = tk.StringVar()
        self.q9 = Label(
            text="9. How would you describe yourself? Be as detailed as you can").pack()
        self.q9_user_input = tk.Entry(
            root, textvariable=self.q9_user_input, width=50)
        self.q9_user_input.pack()

        self.q10_user_input = tk.StringVar()
        self.q10 = Label(
            text="10. Has there been any incident that occurred and later you felt you should have acted differently?").pack()
        self.q10_user_input = tk.Entry(
            root, textvariable=self.q10_user_input, width=50)
        self.q10_user_input.pack()

        self.q11_user_input = tk.StringVar()
        self.q11 = Label(
            text="11. On a scale of 1-10 how satisfied are you with your life?").pack()
        self.q11_user_input = tk.Entry(
            root, textvariable=self.q11_user_input, width=20)
        self.q11_user_input.pack()

        self.q12_user_input = tk.StringVar()
        self.q12 = Label(
            text="12. What can you do differently to make your life better?").pack()
        self.q12_user_input = tk.Entry(
            root, textvariable=self.q12_user_input, width=60)
        self.q12_user_input.pack()

        self.stoprec = tk.Button(
            text='Check results', command=self.setter, relief=RAISED)
        self.stoprec.pack()

    def check(self):
        tkinter.messagebox.showinfo("Success", "Report generated")

    def setter(self):

        dict_key = {'q1': self.q1_user_input.get(), 'q2': self.q2_user_input.get(), 'q3': self.q3_user_input.get(), 'q4': self.q4_user_input.get(), 'q5': self.q5_user_input.get(), 'q6': self.q6_user_input.get(
        ), 'q7': self.q7_user_input.get(), 'q8': self.q8_user_input.get(), 'q9': self.q9_user_input.get(), 'q10': self.q10_user_input.get(), 'q11': self.q11_user_input.get(), 'q12': self.q12_user_input.get(), }
        input_dict.update(dict_key)
        stoprecording()


if __name__ == "__main__":
    start_recording_proc()
    root = tk.Tk()
    root.geometry("800x700")
    root.title("Emo.ai")
    window(root).pack()
    root.mainloop()
