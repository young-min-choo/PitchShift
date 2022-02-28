import tkinter.simpledialog
import tkinter.messagebox
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize

class audioApp:
    def __init__(self, root):
        self.root = root
        self.file_path = ""
        self.out_path = ""

        #create main window
        self.canvas = tkinter.Canvas(self.root, width=600, height=400)
        self.canvas.grid(columnspan=5, rowspan=9)

        self.instructions = tkinter.Label(self.root, text="Select an audio file to tinker with.")
        self.instructions.grid(columnspan=5, column=0, row=0)

        #Text box for presentation
        self.text_box = tkinter.Text(self.root, height=2, width=50, padx=15, pady=15)
        self.text_box.grid(columnspan=3, row=2)

        #Browse button
        self.browse_text = tkinter.StringVar()
        self.browse_button = tkinter.Button(self.root, textvariable=self.browse_text, command=lambda: self.open_file(), height=2, width=15)
        self.browse_text.set("Browse")
        self.browse_button.grid(column=0, row=1, pady=15)

        #Audio Manipulating options
        self.options = tkinter.Label(self.root, text="Audio Manipulation Options:")
        self.options.grid(columnspan=5, column=0, row=3)

        # Pitch change button
        self.pitch_text = tkinter.StringVar()
        self.pitch_button = tkinter.Button(self.root, textvariable=self.pitch_text, command=self.pitch_selection_window, height=2, width=15)
        self.pitch_text.set("Pitch Change")
        self.pitch_button.grid(column=0, row=4, padx=20, pady=15)
        self.pitch_button.config(state="disabled")
        self.pitch_level = 0

        #Pitch option confirmation text box
        self.text_pitch = tkinter.Text(self.root, height=0.75, width=75, padx=15, pady=15, font=1)
        self.text_pitch.grid(columnspan=3, row=5, padx=15)
        self.hide_widget(self.text_pitch)

        #Output File browse button
        self.output_text = tkinter.StringVar()
        self.output_button = tkinter.Button(self.root, textvariable=self.output_text, command=lambda: self.save_file(), height=1, width=30)
        self.output_text.set("Browse Output")
        self.output_button.grid(column=0, row=6, pady=15)
        self.hide_widget(self.output_button)

        #Output File text box
        self.address_box = tkinter.Text(self.root, height=0.5, width=80, padx=15, font=1)
        self.address_box.grid(columnspan=3, row=7, padx=5)
        self.hide_widget(self.address_box)

        # clear selected song button
        self.clear_text = tkinter.StringVar()
        self.clear_button = tkinter.Button(self.root, textvariable=self.clear_text, command=self.delete_text, height=2, width=7)
        self.clear_text.set("Clear")
        self.clear_button.grid(column=4, row=2, padx=20)
        self.clear_button.config(state="disabled")

        #Final confirmation button
        self.run_manipulation_text = tkinter.StringVar()
        self.run_manipulation_button = tkinter.Button(self.root, textvariable=self.run_manipulation_text, command=lambda: self.run_pitch_change(self.file_path, self.out_path, self.pitch_level), width=25, bg = "light green")
        self.run_manipulation_text.set("Run")
        self.run_manipulation_button.grid(column=2, row=8, pady=5)
        self.disable_button(self.run_manipulation_button)
        self.hide_widget(self.run_manipulation_button)

    #Disables a button
    def disable_button(self, btn_name):
        btn_name.config(state="disabled")

    #Enables a button
    def enable_button(self, btn_name):
        btn_name.config(state="normal")

    #Closes a window
    def close_window(self, window_name):
        window_name.destroy()

    #Hide Widgets
    def hide_widget(self, widget_name):
        widget_name.grid_remove()

    #Show Widgets
    def show_widget(self, widget_name):
        widget_name.grid()

    #fills text box with information
    def fill_text(self, text_box_name):
        text_box_name.delete("1.0", "end")
        text_box_name.insert("1.0", 'Changing pitch of {} by {}.'.format(self.file, self.pitch_level))

    #opens dialog box to retrieve audio file information
    def open_file(self):
        self.browse_text.set("Loading...")
        self.file_path = askopenfilename(parent=self.root, title="Choose a file", filetypes=[("Audio file", "*.mp3"), ("Audio file", "*.FLAC"), ("Audio file", "*.WAV")])
        if self.file_path:
            self.enable_button(self.pitch_button)
            self.enable_button(self.clear_button)

        #retrieve filename for presentation
        self.drive, self.path_and_file = os.path.splitdrive(self.file_path)
        self.path, self.file = os.path.split(self.path_and_file)

        #print filename into text box
        self.text_box.insert("1.0", self.file)
        self.text_box.tag_configure("center", justify="center")
        self.text_box.tag_add("center", 1.0, "end")
        self.browse_text.set("Browse")

    #opens dialog box to retrieve save location
    def save_file(self):
        self.output_text.set("Loading...")
        self.out_path = asksaveasfilename(parent=self.root, title="Choose a file", filetypes=[("Audio file", "*.FLAC")])
        self.address_box.delete("1.0", "end")
        self.address_box.insert("1.0", self.out_path)
        self.enable_button(self.run_manipulation_button)

        self.output_text.set("Browse")

    #opens pitch selection window
    def pitch_selection_window(self):
        #create new window for selecting pitch
        self.pitch_window = tkinter.Toplevel(self.root)
        self.pitch_window.title('Pitch Selection')
        self.canvas2 = tkinter.Canvas(self.pitch_window, width=600, height=300)
        self.canvas2.grid(columnspan=6, rowspan=2)



        #Create Text box for presentation
        text_box_pitch = tkinter.Text(self.pitch_window, height=1, width=2, padx=15, pady=15)
        text_box_pitch.grid(column=2, row=1)

        #Label for Text Box
        pitch_label = tkinter.Label(self.pitch_window, text="Selection:")
        pitch_label.grid(column=1, row=1)

        #Confirmation button
        self.pitch_confirm_text = tkinter.StringVar()
        self.pitch_confirm_button = tkinter.Button(self.pitch_window, textvariable= self.pitch_confirm_text, command=lambda: self.close_window(self.pitch_window), height= 2, width=15, bg="light green")
        self.pitch_confirm_text.set("OK")
        #shows pitch change section in main window and fills with information
        self.pitch_confirm_button.bind('<Destroy>', lambda event: self.show_widget(self.text_pitch))
        self.pitch_confirm_button.bind('<Destroy>', lambda event: self.show_widget(self.output_button), add='+')
        self.pitch_confirm_button.bind('<Destroy>', lambda event: self.show_widget(self.address_box), add='+')
        self.pitch_confirm_button.bind('<Destroy>', lambda event: self.show_widget(self.run_manipulation_button), add='+')
        self.pitch_confirm_button.bind('<Destroy>', lambda event: self.fill_text(self.text_pitch), add='+')
        self.pitch_confirm_button.grid(column=4, row=1, padx=10)
        self.disable_button(self.pitch_confirm_button)

        #show pitch selection in text box
        def pitch(level):
            text_box_pitch.delete("1.0", "end")
            text_box_pitch.insert("1.0", str(level))
            text_box_pitch.tag_configure("center", justify="center")
            text_box_pitch.tag_add("center", 1.0, "end")
            self.enable_button(self.pitch_confirm_button)
            self.pitch_level = level



        #create buttons for each pitch selection
        self.pitch_selection_text0 = tkinter.StringVar()
        self.pitch_selection_button0 = tkinter.Button(self.pitch_window, textvariable= self.pitch_selection_text0, command=lambda:pitch(-3), height=2, width=15)
        self.pitch_selection_text0.set("-3")
        self.pitch_selection_button0.grid(column=0, row=0, padx=10)

        self.pitch_selection_text = tkinter.StringVar()
        self.pitch_selection_button = tkinter.Button(self.pitch_window, textvariable= self.pitch_selection_text, command=lambda:pitch(-2), height=2, width=15)
        self.pitch_selection_text.set("-2")
        self.pitch_selection_button.grid(column=1, row=0, padx=10)

        self.pitch_slt = tkinter.StringVar()
        self.pitch_slt_btn = tkinter.Button(self.pitch_window, textvariable= self.pitch_slt, command=lambda:pitch(-1), height=2, width=15)
        self.pitch_slt.set("-1")
        self.pitch_slt_btn.grid(column=2, row=0, padx=10)

        self.pitch_selection_text2 = tkinter.StringVar()
        self.pitch_selection_button2 = tkinter.Button(self.pitch_window, textvariable= self.pitch_selection_text2, command=lambda:pitch(1), height=2, width=15)
        self.pitch_selection_text2.set("+1")
        self.pitch_selection_button2.grid(column=3, row=0, padx=10)

        self.pitch_selection_text3 = tkinter.StringVar()
        self.pitch_selection_button3 = tkinter.Button(self.pitch_window, textvariable= self.pitch_selection_text3, command=lambda:pitch(2), height=2, width=15)
        self.pitch_selection_text3.set("+2")
        self.pitch_selection_button3.grid(column=4, row=0, padx=10)

        self.pitch_selection_text4 = tkinter.StringVar()
        self.pitch_selection_button4 = tkinter.Button(self.pitch_window, textvariable= self.pitch_selection_text4, command=lambda:pitch(3), height=2, width=15)
        self.pitch_selection_text4.set("+3")
        self.pitch_selection_button4.grid(column=5, row=0, padx=10)

    def delete_text(self):
        self.text_box.delete("1.0", "end")
        self.clear_button.config(state="disabled")
        self.pitch_button.config(state="disabled")

    def complete_message(self, man_type):
        tkinter.messagebox.showinfo('{}'.format(man_type), "Audio Manipulation: {} Complete!".format(man_type))

    def run_pitch_change(self, song_path, output_path, pitch_level):
        self.run_manipulation_text.set("Running...")
        self.run_manipulation_button.config(bg="orange")
        y, sr = librosa.load(song_path, sr=None, mono=True)
        # #pitch shifting entire audio track
        # y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_level)
        # sf.write(output_path, y_shifted, samplerate=sr, format='FLAC', subtype='PCM_24')

        #splitting track into harmonic and percussive components, pitch shifting harmonic component, then merging components into final track
        y_harmonic = librosa.effects.harmonic(y)
        y_percussive = librosa.effects.percussive(y, margin=3.0)
        shifted_y_harmonic = librosa.effects.pitch_shift(y_harmonic, sr=sr, n_steps=pitch_level)
        sf.write(output_path, y_percussive, samplerate=sr, format='FLAC', subtype='PCM_24')
        merged_track = np.vstack((shifted_y_harmonic, y_percussive)).T
        sf.write(output_path, merged_track, samplerate=sr, format='FLAC', subtype='PCM_24')
        # #normalizing volumes on merged track
        # volume_control_target = AudioSegment.from_file(output_path)
        # normalized_audio = normalize(volume_control_target)
        # normalized_audio.export(out_f= output_path, format="flac")

        self.run_manipulation_text.set("Run")
        self.run_manipulation_button.config(bg="light green")
        self.complete_message("Pitch Change")

    def run(self):
        self.root.mainloop()



if __name__=='__main__':
    root = tkinter.Tk()
    root.title('Audio Manipulator v1.0')
    app = audioApp(root)
    app.run()
