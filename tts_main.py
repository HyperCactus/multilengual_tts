# A function that will read a file of text in a given language and create an mp3 file of the text.
# where each sentence is spoken in a specified language first and then in a language the user chooses.

import os
from googletrans import Translator
from moviepy.editor import concatenate_audioclips, AudioFileClip
# from moviepy.audio.io.VideoFileClip import VideoFileClip
# from moviepy.audio.fx.audio_fadein import audio_fadein
# from moviepy.audio.fx.audio_fadeout import audio_fadeout
# from moviepy.audio.fx.audio_left_right import audio_left_right
# from moviepy.audio.fx.audio_loop import audio_loop
# from moviepy.audio.fx.audio_normalize import audio_normalize
# from moviepy.audio.fx.volumex import volumex
# from moviepy.audio.io.AudioFileClip import AudioFileClip
from gtts import gTTS
import PyPDF2
import tkinter as tk
from tkinter import filedialog
import webbrowser


#=====================================================================================================================

class LanguageReader:
    def __init__(self):
        self.file_name = 'test_text.txt'
        self.language = 'de'
        self.first_read = 'en'
        self.second_read = 'de'
        self.furst_slow = False
        self.second_slow = False
        self.status = tk.StringVar()
        # self.print_current_directory()

    def concatenate_audio(self, audio_clip_paths, output_path='multilingual_audio.mp3'):
        """Concatenates several audio files into one audio file using MoviePy
        and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)

    # A function that will print out the current directory.
    def print_current_directory(self):
        """
        Prints out the current directory.
        """
        print(os.getcwd())

    # A function that creates a temporary folder for the files to be saved in.
    def _create_temp_folder(self, folder_name='temp'):
        """
        Creates a temporary folder for the files to be saved in.
        """
        os.mkdir('temp_folder')
        # os.chdir('temp_folder')
        # self.print_current_directory()

    # Create a function that will read a file and turn it into a list of sentences.
    def read_file(self, file_name):
        """
        Reads a file and turns it into a list of sentences.
        Perameters:
            file_name: name of the file to read
        :param file_name:
        :return:
        """
        # Checks the file type
        if file_name.endswith('.pdf'):
            # If the file is a pdf, turn it into a string using PyPDF2
            pdf_file = open(file_name, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            pdf_reader.numPages
            text_string = ''
            for page in range(pdf_reader.numPages):
                text_string += pdf_reader.getPage(page).extractText()
            pdf_file.close()

        elif file_name.endswith('.txt'):
            # If the file is a txt, turn it into a string using the open function
            text_file = open(file_name, 'r')
            text_string = text_file.read()
            text_file.close()
        else:
            self._set_status('File type not supported')

        # Turn the string into a list of sentences
        sentences = text_string.split('.')
        cleaned_sentences = []
        for i in range(len(sentences)):
            # If the sentence is not empty, add it to the list of cleaned sentences
            if sentences[i] not in ['', '\n', '\n\n', ' ', '\n\n\n', '  ']:
                cleaned_sentences.append(sentences[i])

        for i in range(len(cleaned_sentences)):
            sentences[i] += '...   '

        return cleaned_sentences

    def _set_status(self, status):
        """
        Sets the status of the program.
        Perameters:
            status: status to set the program to
        """
        self.status.set(status)
        # print(self.status)

    def get_status(self):
        """
        Returns the status of the program.
        """
        return self.status

    def delete_list_of_files(self, file_list):
        """
        Deletes a list of files.
        Perameters:
            file_list: list of files to delete
        """
        for file in file_list:
            os.remove(file)

    def translate_list_of_sentences(self, sentences: list, input_language='de', target_language='en') -> list:
        """
        Translates a list of sentences to a given language.
        Perameters:
            sentences: list of sentences to translate
            input_language: language of the sentences
            target_language: language to translate the sentences to
        Returns:
            list of translated sentences
        """
        translator = Translator()
        result = []
        for n, sentence in enumerate(sentences):
            try:
                self._set_status('Translating sentence ' + str(n + 1) + ' of ' + str(len(sentences)))
                result.append(translator.translate(sentence, src=input_language,
                                                   dest=target_language).text)
            except:
                self._set_status('Error translating sentence: ' + sentence)
                result.append(sentence)

        return result

    def speek_sentence(self, sentence, language='en', slow=False, file_name='temp.mp3'):
        """
        Speaks a sentence in a given language.
        Perameters:
            sentence: sentence to speak
            language: language to speak the sentence in
        """
        tts = gTTS(text=sentence, lang=language, slow=slow)
        tts.save(file_name)

    def create_audio_file(self, sentences_first, sentences_second,
                          language_first='en', language_second='de',
                            slow_first=False, slow_second=False):
        """
        Creates an audio file of the given sentences.
        Assumes that the sentences are already translated.
        Perameters:
            sentences_first: list of sentences to speak in the first language
            sentences_second: list of sentences to speak in the second language
            language_first: language to speak the sentences in the first language
            language_second: language to speak the sentences in the second language
            slow_first: whether or not to slow down the first language
            slow_second: whether or not to slow down the second language
        """
        # create a temp folder to save the audio files in
        self._create_temp_folder('temp_folder')
        os.chdir('temp_folder')
        # create an mp3 of each sentence in both languages
        temp_audio_filenames = []
        for i in range(len(sentences_first)):
            # first language
            self._set_status('Creating audio file for sentence ' + str(i + 1) + ' of ' + str(len(sentences_first)))
            self.speek_sentence(sentences_first[i], language=language_first, slow=slow_first,
                                file_name='temp_' + str(i) + '_' + language_first + '.mp3')
            temp_audio_filenames.append('temp_folder/temp_' + str(i) + '_' + language_first + '.mp3')
            # second language
            self.speek_sentence(sentences_second[i], language=language_second, slow=slow_second,
                                file_name='temp_' + str(i) + '_' + language_second + '.mp3')
            temp_audio_filenames.append('temp_folder/temp_' + str(i) + '_' + language_second + '.mp3')

        # change the directory back to the original directory
        os.chdir('..')

        self._set_status('Concatenating audio files')
        # concatenate the mp3 files
        self.concatenate_audio(temp_audio_filenames,
                               output_path='{}_{}_tts.mp3'.format(language_first, language_second))

        # delete the temp folder
        self.delete_list_of_files(temp_audio_filenames)
        os.rmdir('temp_folder')
        self._set_status('Done!')

    def create_audio_file_from_file(self, file_name, file_language, language_first='en', language_second='de',
                                    slow_first=False, slow_second=False):
        """
        Creates an audio file of the given file.
        Perameters:
            file_name: name of the file to read
            file_language: language of the file
            language_first: language to speak the sentences in the first language
            language_second: language to speak the sentences in the second language
            slow_first: whether or not to slow down the first language
            slow_second: whether or not to slow down the second language
        """
        # create a list of sentences from the file
        sentences = self.read_file(file_name)

        if file_language == language_first:
            sentences_first = sentences
        else:
            # translate the sentences to the file language
            sentences_first = self.translate_list_of_sentences(sentences,
                                                               input_language=file_language,
                                                               target_language=language_first)

        # translate the sentences to the second language
        if file_language == language_second:
            sentences_second = sentences
        else:
            sentences_second = self.translate_list_of_sentences(sentences,
                                                                input_language=file_language,
                                                                target_language=language_second)

        # create the audio file
        self.create_audio_file(sentences_first, sentences_second,
                               language_first=language_first, language_second=language_second,
                               slow_first=slow_first, slow_second=slow_second)




#=====================================================================================================================

# Create a GUI class for the program
class TtsGui(tk.Frame):
    """
    Creates a GUI for the program.
    """
    def __init__(self, master):
        """
        Creates a GUI for the program.
        :param master:
        """
        self.all_interactable_widgets = []
        self.background_color = '#f5f5f5'
        self.font = ('Arial', 10)
        super().__init__(master, borderwidth=4, relief=tk.RIDGE, padx=20, pady=20, background=self.background_color)
        self.master = master
        self.pack(expand=True, fill='both')
        # set the title of the window
        self.master.title('Multilingual Text to Speech')
        self.row_frames = []
        self.file_name = ''
        self.languages = {'English': 'en', 'German': 'de', 'French': 'fr',
                          'Spanish': 'es', 'Italian': 'it', 'Portuguese': 'pt',
                          'Russian': 'ru', 'Japanese': 'ja', 'Chinese': 'zh-CN'}

        self.donation_message = 'If you like this program, please consider donating to support the development of projects like this.'
        self.donation_link = 'https://www.paypal.com/donate/?business=4PGVV946AQ2SA&no_recurring=0&item_name=I+am+a+student+developing+and+sharing+open+source+educational+software+for+free.+Your+generosity+is+greatly+appreciated%21&currency_code=AUD'

        # create an instance of the LanguageReader class
        self.language_reader = LanguageReader()

        # Create a title label
        self.title_label = tk.Label(self, text='Multilingual Text to Speech', font=('Arial', 20),
                                    background=self.background_color, padx=20, pady=30)
        self.title_label.pack(side=tk.TOP, fill=tk.X)

        # Create a row with text and a button to select a file
        self.add_row_frame()
        self.file_label = tk.Label(self.row_frames[-1], text='Please select a file: ', font=self.font,
                                   background=self.background_color)
        self.file_label.pack(side=tk.LEFT, padx=4, pady=0)

        # Adding the file button
        self.file_button = tk.Button(self.row_frames[-1], text='Select File', font=self.font,
                                     command=self.select_file)
        self.file_button.pack(side=tk.LEFT, padx=4, pady=0)
        self.all_interactable_widgets.append(self.file_button)

        # Adding the file name label
        self.file_name_label = tk.Label(self.row_frames[-1], text=self.file_name, font=self.font,
                                        background=self.background_color)
        self.file_name_label.pack(side=tk.LEFT, padx=4, pady=0)

        # Create a row with a dropdown menu to select the language of the file
        self.add_row_frame()
        self.language_label = tk.Label(self.row_frames[-1], text='Please select the language of the file: ',
                                       font=self.font, background=self.background_color)
        self.language_label.pack(side=tk.LEFT, padx=4, pady=0)

        # Adding the language dropdown menu
        self.file_language = tk.StringVar()
        self.file_language.set('German')
        self.file_language_menu_dropdown = tk.OptionMenu(self.row_frames[-1], self.file_language, *self.languages.keys())
        self.file_language_menu_dropdown.pack(side=tk.LEFT, padx=4, pady=0)
        self.all_interactable_widgets.append(self.file_language_menu_dropdown)

        # Create a row with a dropdown menu to select the first and second language
        self.add_row_frame()
        self.language_label = tk.Label(self.row_frames[-1],
                                       text='I would like each sentence to be read out first in: ',
                                        font=self.font, background=self.background_color)
        self.language_label.pack(side=tk.LEFT, padx=4, pady=0)
        # Adding the language dropdown menu
        self.first_language = tk.StringVar()
        self.first_language.set('English')
        self.first_language_menu_dropdown = tk.OptionMenu(self.row_frames[-1], self.first_language, *self.languages.keys())
        self.first_language_menu_dropdown.pack(side=tk.LEFT, padx=0, pady=0)
        self.all_interactable_widgets.append(self.first_language_menu_dropdown)

        # Create a slow tickbox
        self.first_slow = tk.IntVar()
        self.first_slow_tickbox = tk.Checkbutton(self.row_frames[-1], text='Slow', font=self.font,
                                                 variable=self.first_slow, background=self.background_color)
        self.first_slow_tickbox.pack(side=tk.LEFT, padx=2, pady=0)
        self.all_interactable_widgets.append(self.first_slow_tickbox)

        # Adding the label for the second language
        self.add_label('and then read out in: ', self.row_frames[-1])
        # Adding the second language dropdown menu
        self.second_language = tk.StringVar()
        self.second_language.set('German')
        self.second_language_menu_dropdown = tk.OptionMenu(self.row_frames[-1], self.second_language, *self.languages.keys())
        self.second_language_menu_dropdown.pack(side=tk.LEFT, padx=0, pady=0)
        self.all_interactable_widgets.append(self.second_language_menu_dropdown)

        # Create a slow tickbox
        self.second_slow = tk.IntVar()
        self.second_slow.set(1)
        self.second_slow_tickbox = tk.Checkbutton(self.row_frames[-1], text='Slow', font=self.font,
                                           variable=self.second_slow, background=self.background_color)
        # self.second_slow_tickbox.select()
        self.second_slow_tickbox.pack(side=tk.LEFT, padx=2, pady=0)
        self.all_interactable_widgets.append(self.second_slow_tickbox)

        # Create a row with a button to start the program
        self.add_row_frame()
        self.start_button = tk.Button(self.row_frames[-1], text='Generate audio file', font=self.font,
                                        command=self.start_program)
        self.start_button.pack(side=tk.LEFT, padx=4, pady=0)
        self.all_interactable_widgets.append(self.start_button)

        # Create a donation button
        self.donation_button = tk.Button(self.row_frames[-1], text='Donate', font=self.font,
                                         command=lambda: webbrowser.open(self.donation_link))
        self.donation_button.pack(side=tk.RIGHT, padx=1, pady=0)

        # Create a donation message label
        self.donation_label = tk.Label(self.row_frames[-1], text=self.donation_message, font=self.font,
                                       background=self.background_color)
        self.donation_label.pack(side=tk.RIGHT, padx=1, pady=0)

        # Create a row with a state label that shows the state of the program
        self.add_row_frame()
        self.state = self.language_reader.get_status()
        self.state_label = tk.Label(self.row_frames[-1], textvariable=self.language_reader.get_status(), font=self.font,
                                    background=self.background_color)
        self.state_label.pack(side=tk.LEFT, padx=4, pady=0)



    def add_label(self, text, row_frame):
        """
        Adds a label to the row frame.
        :param text: text to display
        :param row_frame: row frame to add the label to
        """
        label = tk.Label(row_frame, text=text, font=self.font,
                                    background=self.background_color)
        label.pack(side=tk.LEFT, padx=5, pady=0)

    def add_row_frame(self):
        """
        Creates a frame for a row of widgets.
        """
        row_frame = tk.Frame(self, padx=5, pady=4, background=self.background_color)
        row_frame.pack(side=tk.TOP, fill=tk.X)
        self.row_frames.append(row_frame)

    def select_file(self):
        """
        Selects a PDF or txt file using a filedialog menue.
        """
        self.file_name = filedialog.askopenfilename(filetypes=[('PDF', '*.pdf'), ('Text', '*.txt')])
        self.file_name_label.config(text=self.file_name.split('/')[-1], font=self.font,
                                    background=self.background_color, fg='blue')

    def disable_widgets(self):
        """
        Disables all widgets.
        """
        for widget in self.all_interactable_widgets:
            widget.config(state=tk.DISABLED)

    def enable_widgets(self):
        """
        Enables all widgets.
        """
        for widget in self.all_interactable_widgets:
            widget.config(state=tk.NORMAL)

    def start_program(self):
        """
        Starts the program.
        """
        self.disable_widgets()
        self.state.set('Generating audio file...')


        # print(str(((self.file_name, self.languages[self.file_language.get()],self.languages[self.first_language.get()],
        #                                                      self.languages[self.second_language.get()],
        #                                                      bool(self.first_slow.get()),
        #                                                      bool(self.second_slow.get())))))

        try:
            self.language_reader.create_audio_file_from_file(self.file_name,
                                                             file_language=self.languages[self.file_language.get()],
                                                             language_first=self.languages[self.first_language.get()],
                                                             language_second=self.languages[self.second_language.get()],
                                                             slow_first=bool(self.first_slow.get()),
                                                             slow_second=bool(self.second_slow.get()))
        except Exception as e:
            self.state.set('Error: ' + str(e))

        self.enable_widgets()








#=====================================================================================================================

# lr = LanguageReader()
# print(lr.read_file('test_text.txt'))
# lr.create_audio_file_from_file('test_text.txt', 'de', language_first='ru', language_second='es',
#                                slow_first=False, slow_second=True)

root = tk.Tk()
gui = TtsGui(root)

root.mainloop()