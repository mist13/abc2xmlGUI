import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage, Toplevel
from tkHyperlinkManager import HyperlinkManager
import configparser
import ctypes
import gettext
import locale
import os
import re
import subprocess
import webbrowser
from functools import partial
from PIL import ImageTk, Image
try:
    import abc2xml
    test = abc2xml.getInfo
    abc2xmlpath = 'import'
except Exception:
    abc2xmlpath = ''
try:
    import xml2abc
    test = xml2abc.vertaal
    xml2abcpath = 'import'
except Exception:
    xml2abcpath = ''


class abc2xmlGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("abc2xml GUI")
        #self.root.geometry("800x520")
        self.root['bg'] = '#4681b3'
        icon64 = '''iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9
kT1Iw0AcxV9TpaVUHCwo4pChOlkQFXGUKhbBQmkrtOpgcukXNGlIUlwcBdeCgx+LVQcXZ10dXAVB
8APE1cVJ0UVK/F9SaBHjwXE/3t173L0DhGaVqWbPBKBqlpFOxMVcflUMvMKPEIIQMCgxU09mFrPw
HF/38PH1LsazvM/9OfqUgskAn0g8x3TDIt4gntm0dM77xBFWlhTic+Jxgy5I/Mh12eU3ziWHBZ4Z
MbLpeeIIsVjqYrmLWdlQiaeJo4qqUb6Qc1nhvMVZrdZZ+578heGCtpLhOs0RJLCEJFIQIaOOCqqw
EKNVI8VEmvbjHv5hx58il0yuChg5FlCDCsnxg//B727N4tSkmxSOA70vtv0xCgR2gVbDtr+Pbbt1
AvifgSut4681gdlP0hsdLXoE9G8DF9cdTd4DLneAoSddMiRH8tMUikXg/Yy+KQ8M3AKhNbe39j5O
H4AsdbV8AxwcAmMlyl73eHewu7d/z7T7+wEEs3J7nqxWzQAAAAlwSFlzAAALEwAACxMBAJqcGAAA
A2BJREFUSMflls9LVFEUxz/vOTPOD3+MY06BITppDZmpmzQXFf3QFu2CaBkREbSUop1Ei1xFf0Et
WkiEO4k0WgiV/aDIrJAUTXHILJlJnBmdGd5r4Zmc3twZp4IKOvBghnPu93vPvd97zoH/zbSNAswJ
NMAJeAA34ALsgE1CUkASiAMxIAqsaA2Yv0wspB4gADTKVwdsAUokbBmYB6aBt/JNAdF85NoGWdYA
LcBeIAhUA37ACzgkPAFEgAUgBIwDI8ArYDZX9loO0hKgFtgPdAHtQCVgyhqt98EtDBPOtd/GVzJg
ZvgWgSfAIDAMfACWreS6ImGnkB4DjgMdgE9A9fRmRz6XM7zgZfJzMxafT9YcF4xawSQnsWRbI5l2
As0ClLVBu76WwJWnbbwJdVsxfbK2U7BqBDubOENILXK8u4GKXOIo1o21CzY0uocP8HL2kjWkQjC6
BNOTSa5bjjggQmoXAeU0h/6jXnoedzC7eNoa5hWsvYLtVBF75LkERUh6PmKbtkZ8sXWMameShKFx
88Vh1VVWCmajcGQRu8VZLQrNa+k73lU9Su/hPkqKDB5/KeXT0omshyKYjcKRReyS4uAvpKLZM47a
X3aHkw0zAMyFA6on6xdsl4rYLhXJWwhx+qjTtm1TCIBYwqUi9gq2XUVsk8LhKKTI20TVaSuS/46i
lFKLgm3LV0AKMrtF1elMve5wQettGb9TUvAT+bMuZTVVT5HlqOeXfABsLptSLUoIdkpFnJQuEwGq
rPdsmH6eTZ/lxmgrM3EHukUFYwtVNJXH8LrvqlQdEeyk6qjj0toWVM9p8O0Fep60MRN3yEbWfUvx
gzz6UkZXQJmtKZjTwpFFHJNeGrJm+zV+lOuvgzlEFuPF7CEcusme2uFcrTck2DEVcVSc49Lavss2
HN2qJN1cnMJdPE/fuyCndkxT7rpnDTEEa1ywoyriFZkcRqSfRtIOn2cq604BzjSNsZqsosqZoGtn
v2pvEcEaEewV5SAg3WM7cET6aXO6Qz2cvMzV562kzLUl53dNcKzpGro2h2FuRdfmrKRhYBToB+4D
7zOHAdUE4gLqpYl3SmvzAvry6j7C0TrKnB8pdw/lem+GZPoaGAIGgEmtYV1YvzX6KJT7U6PPvzPs
/dXx9k8M9P+ffQNgoChVu08xNQAAAABJRU5ErkJggg=='''
        self.icon = PhotoImage(data=icon64)
        self.root.iconphoto(False, self.icon)

        self.pathGUI = os.path.dirname(os.path.realpath(__file__))
        self.pathExe = os.path.realpath('.')
        self.pathXml2Abc = xml2abcpath
        self.pathAbc2Xml = abc2xmlpath
        self.lang = ''
        self.messages = 'on'

        self.collectFiles()
        self.setI18N()

        self.allFiles = _("All files")
        self.fileTypes = (("abc","*.abc *.txt"),("XML","*.mxl *.musicxml *.xml"),(self.allFiles,"*.*"))
        self.fileTypesX = (self.fileTypes[1], self.fileTypes[0], self.fileTypes[2])

        self.labelText = _("This program needs abc2xml and/or xml2abc from wim.vree.org to work.")

        self.installAbcText = _(""" INSTALLATION
 ============
Copy abc2xml.py and/or xml2abc.py into this program's folder:

{folder}

Should you already have the files in a different location,
enter their full path into the ini file in the same folder.

If you are running Windows, make sure that Python is installed
and that the path to Python is in your PATH environment variable.
Alternatively, use abc2xml.exe and xml2abc.exe files instead.""").format(folder=self.pathGUI)

        self.infoAbcText = _(""" INSTRUCTIONS
 ============
1. Paste abc/XML or select file using button 'Open'.
2. Change abc/XML as desired and/or select part of it.
   Changed abc/XML can be saved using button 'Save'.
3. Convert using button 'Convert'.""")

        self.allFiles = _("All files")

        self.labelframe = tk.Frame(self.root, width=760, bg=self.root['bg'])

        # text label + link
        self.textLabel = tk.Text(self.labelframe, height=1, width=68, borderwidth=0, highlightthickness=0, bg=self.root['bg'], font=('Helvetica', 12, 'bold'), fg='#ffdb00')
        self.linkIndex = self.labelText.find("wim.vree.org")
        self.linkStart = '1.' + str(self.linkIndex)
        self.labelText = self.labelText.replace("wim.vree.org", "")
        self.textLabel.insert('1.0', self.labelText)
        self.hyperlink = HyperlinkManager(self.textLabel)
        self.textLabel.insert(self.linkStart, "wim.vree.org",self.hyperlink.add(partial(webbrowser.open,'https://wim.vree.org/svgParse')))
        self.textLabel.pack(side=tk.LEFT, anchor=tk.NW)
        self.textLabel.configure(state="disabled")

        self.versionText = tk.Label(self.labelframe, borderwidth=0, bg=self.root['bg'], font=('Helvetica', 12, 'bold'), fg='#ffdb00', text="V 1.1")
        self.versionText.pack(side=tk.RIGHT, anchor=tk.NE)

        self.labelframe.pack(padx=20, pady=12, fill='both', expand=1)

        # if tkinter is 8.5 or above you'll want the selection background
        # to appear like it does when the widget is activated
        # comment this out for older versions of Tkinter
        self.textLabel.configure(inactiveselectbackground=self.textLabel.cget('selectbackground'))

        self.textboxframe = tk.Frame(self.root, width=760, height=400, bg='white')
        #self.textboxframe.grid(row=0, column=1)
        # allow the column inside the frame to grow
        #self.textboxframe.columnconfigure(0, weight=10)
        # By default the frame will shrink to whatever is inside of it and 
        # ignore width & height. We change that:
        #self.textboxframe.pack_propagate(False)
        self.textboxframe.pack(padx=20, fill='both', expand=1)
        self.abcText = tk.Text(self.textboxframe, borderwidth=0, highlightthickness=0, font='TkFixedFont')
        self.abcText.pack(padx=5, pady=5, fill='both', expand=1)
        self.abcText.insert('1.0', "\n" + self.infoAbcText)
        self.checkPaths()

        self.bottomframe = tk.Frame(self.root, bg=self.root['bg'])
        self.bottomframe.rowconfigure(0, weight=1)
        self.bottomframe.rowconfigure(1, weight=1)
        
        self.scoreLineBreak = tk.StringVar()
        self.lbCheckBox = tk.Checkbutton(self.bottomframe,
                                        text=" " + _("score line-break") + " = $",
                                        highlightthickness=0,
                                        variable=self.scoreLineBreak, onvalue="", offvalue="-b",
                                        bg=self.root['bg'], fg='#ffdb00', font=('Helvetica', 11, 'bold'))
        self.lbCheckBox.grid(row=0, columnspan=2, column=0, sticky=tk.W, padx=0, pady=(5,5))
        self.lbCheckBox.deselect()

        btLogo64 = '''iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAYAAACAl21KAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9
kT1Iw0AcxV9TpaVUHCwo4pChOlkQFXGUKhbBQmkrtOpgcukXNGlIUlwcBdeCgx+LVQcXZ10dXAVB
8APE1cVJ0UVK/F9SaBHjwXE/3t173L0DhGaVqWbPBKBqlpFOxMVcflUMvMKPEIIQMCgxU09mFrPw
HF/38PH1LsazvM/9OfqUgskAn0g8x3TDIt4gntm0dM77xBFWlhTic+Jxgy5I/Mh12eU3ziWHBZ4Z
MbLpeeIIsVjqYrmLWdlQiaeJo4qqUb6Qc1nhvMVZrdZZ+578heGCtpLhOs0RJLCEJFIQIaOOCqqw
EKNVI8VEmvbjHv5hx58il0yuChg5FlCDCsnxg//B727N4tSkmxSOA70vtv0xCgR2gVbDtr+Pbbt1
AvifgSut4681gdlP0hsdLXoE9G8DF9cdTd4DLneAoSddMiRH8tMUikXg/Yy+KQ8M3AKhNbe39j5O
H4AsdbV8AxwcAmMlyl73eHewu7d/z7T7+wEEs3J7nqxWzQAAAAlwSFlzAAALEwAACxMBAJqcGAAA
AhxJREFUOMudk0FLG1EUhb/7CE26CiWGOhkKznQhFJEKNhVJYxfZCLMrzEK6cO9GrP6HQii48QcI
XXcVsgtUhRSEkqwKWUU7mTi1QulSKe91kWlKdEbEA7O497177j3nvhEgv7Gx8TmbzT7nHri8vOzu
7e29VsDi6urqvUgA4tpF2draMgAf3j77fypCP4gAcJ5MA0zGxoyvvvv4DQB1o4UIjYMOzK3B3BrN
wy7Nw+44bhx0QORGmUoat3dyhmVNIwK904jeaYQIWNY0vZOzRIkqTXsURTiOM44dxyGKolSvMknJ
2RmLIBgAoLUe54NgwOyMdUciY/BWFugPjug33vMw9wCAN7UXmN9HvFpZmDA7XVpstkGwpvI8Low+
ayqPQVLNvmWicz61vjL8+QuAUvERS/NP8VImylxdXXVs217oh+c3Dpfm3etd6A9+TGSKxSJhGHYE
oNFoGJ3Q5S5QInielyA2xvLysimXyxO54+Nj2u223Hn9AOVymfX1dUw8qcQ92+124n3xfX/btu36
yGeDGEEDIiMCpRRaa5RKfrvGGMIw3MnYtl13XRdjDNVqla79BY8/BIMKAPv7+3ieR7PZTCRyXReg
njHGUKlUMMagtWY+eMn3eEMAu7u71Go1Li4u8H1/LPUfWq0WSqn0f+06kkgAPM9Daz0yW9KXx+bm
JrlcjkKhkGxyXCu+72+XSqV66juJzb4Nw+Fw5y/6itAbDV2yWAAAAABJRU5ErkJggg=='''
        btLogo = PhotoImage(data=btLogo64)
        self.logoLabel = tk.Label(self.bottomframe, image=btLogo, compound='left',
                                  borderwidth=0, bg=self.root['bg'], 
                                  font=('Helvetica', 12), fg='#ffdb00',
                                  text="   blechtrottel.net")
        self.logoLabel.grid(row=0, column=3, columnspan=2, sticky=tk.NE, padx=10, pady=(8,0))
        wwwlang = 'en/'
        if self.lang.startswith('de'):
            wwwlang = ''
        self.logoLabel.bind("<Button-1>", lambda event: webbrowser.open("https://blechtrottel.net/" + wwwlang))
        self.logoLabel.bind("<Enter>", lambda event: self.logoLabel.config(cursor="hand2"))
        self.logoLabel.bind("<Leave>", lambda event: self.logoLabel.config(cursor=""))

        self.bottomframe.columnconfigure(0, weight=1)
        self.bottomframe.columnconfigure(1, weight=1)
        self.bottomframe.columnconfigure(2, weight=5),
        self.bottomframe.columnconfigure(3, weight=1)
        self.bottomframe.columnconfigure(4, weight=1)

        self.buttonOpenFile = GUIButton(0, self.bottomframe, text=_("Open"), command=self.openFile)
        self.buttonSaveFile = GUIButton(1, self.bottomframe, text=_("Save"), command=self.saveTextBox)
        self.buttonXml2Abc = GUIButton(4, self.bottomframe, text=_("Convert"), command=self.startConversion)

        self.bottomframe.pack(fill='x', padx=20)

        self.root.mainloop()


    def abc2xml(self):
        if (self.pathAbc2Xml != ''):
            if self.pathAbc2Xml == 'import': # If imported run as module, else start process
                xml_docs = abc2xml.getXmlDocs (self.txt, skip = 0, num = 1, rOpt = False, bOpt = False, fOpt = False)
                out = abc2xml.fixDoctype (xml_docs [0])
                msg = abc2xml.getInfo()
            else:
                cmdList = self.prepCmdList(self.pathAbc2Xml)
                proc = subprocess.Popen(cmdList, universal_newlines=True,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, msg = proc.communicate(self.txt)
            self.saveFile(out)
            if self.messages == 'on':
                self.wShowMessage('abc2xml', msg)
        else:
            infotext = _("This function needs abc2xml.\nCopy file into abc2xmlGUI folder\nor enter path into abc2xmlGUI.ini.")
            self.userInfo('showerror', infotext)


    def checkPaths(self): # Check converters
        if (self.pathAbc2Xml == '' or self.pathXml2Abc == ''):
            self.abcText.delete('1.0', tk.END)
            if (self.pathAbc2Xml == '' and self.pathXml2Abc == ''): # Instructions if no converters
                self.abcText.insert('1.0', "\n" + self.installAbcText)
            else:              
                self.abcText.insert('1.0', "\n" + self.infoAbcText)


    def collectFiles(self): # Check for converters in GUI directory
        dirFiles = os.listdir(self.pathGUI)
        for c in ['abc2xml.py', 'abc2xml.exe', 'xml2abc.py', 'xml2abc.exe']:
            if c in dirFiles:
                if 'abc2xml' in c and self.pathAbc2Xml == '':
                    self.pathAbc2Xml = self.pathGUI + '/' + c
                elif self.pathXml2Abc == '':
                    self.pathXml2Abc = self.pathGUI + '/' + c
                    break

        self.readIniFile() # Check ini for language and missing converter paths


    def getLocalPath(self, path): # Remove "file://" from paths and third "/" from paths in Windows
        path = re.sub(r'^(file:\/{2})', '', path)
        if (os.name == "nt"):
            path = re.sub(r'^\/', '', path)
            path = re.sub(r'\\', '/', path)
        return path


    def openFile(self):
        self.fl =  filedialog.askopenfile(mode = 'r', initialdir = self.pathExe, title = _("Select file"), filetypes = (("abc","*.abc *.txt"),("XML","*.mxl *.musicxml *.xml"),(self.allFiles,"*.*")))
        if self.fl is not None:
            text = self.fl.read()
            self.abcText.delete('1.0', tk.END)
            self.abcText.insert(tk.END, text)


    # Prepare paths, command and parameters for running converters 
    def prepCmdList(self, path):
        cmdList = []
        path = self.getLocalPath(path)
        if '.py' in path:
            python = "python" + self.whatPython()
            if python != 'python not found':
                cmdList = [python, "-X utf8"]
            else:
                infotext = _("Python not found!\nPlease check your installation and\nenvironment variables.")
                self.userInfo('showerror', infotext)
                return
        cmdList.append(path)
        lb = self.scoreLineBreak.get()
        pIn = "-" 
        if "xml2abc." in path:
            if lb == "-b":
                lb = "-x"
            pIn = "-i"
        cmdList.extend([lb, pIn])
        return cmdList


    def readIniFile(self):
        if os.path.isfile(self.pathExe + '/abc2xmlGUI.ini'):
            ini = configparser.ConfigParser()
            ini.read(self.pathExe + '/abc2xmlGUI.ini')

            self.lang = ini['Language']['lang']

            if (self.pathAbc2Xml == ''):
                iniabc2xml = ini['Converters']['abc2xml']
                if 'abc2xml.' in iniabc2xml:
                    self.pathAbc2Xml = self.getLocalPath(iniabc2xml.strip())
                        
            if (self.pathXml2Abc == ''):
                inixml2abc = ini['Converters']['xml2abc']
                if 'xml2abc.' in inixml2abc:
                    self.pathXml2Abc = self.getLocalPath(inixml2abc.strip())

            inimessages = ini['Converters']['messages']
            if ('off' in inimessages) or ('0' in inimessages) or ('no' in inimessages):
                self.messages = 'off'

    def saveFile(self, content):
        ifile = ''
        idir = self.pathExe
        if hasattr(self, 'fl') and self.fl is not None:
            filepart = self.fl.name.split('/')[-1]
            idir = self.fl.name.replace('/' + filepart, '')
            ifile = filepart.split('.')[0]
        if content.startswith('<?xml'):
            outFiles = self.fileTypesX
            if ifile != '':
                ifile += ".xml"
        else:
            outFiles = self.fileTypes
            if ifile != '':
                ifile += ".abc"
        filename = filedialog.asksaveasfile(initialfile = ifile, initialdir = idir, title = _("Select file"), filetypes = outFiles)
        if filename is not None:
            filename.write(content)


    def saveTextBox(self):
        try:
            self.txt = self.abcText.selection_get()
        except Exception:
            self.txt = self.abcText.get('1.0', tk.END)
        self.saveFile(self.txt)


    def setI18N(self): # Set Language, ini setting overrides system language 
        if self.lang == '': # if no language in ini
            if os.name == 'posix':
                self.lang = os.getenv('LANG')
            else:
                windll = ctypes.windll.kernel32
                self.lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        pathLocale = os.path.join(self.pathGUI, 'locale')
        try:        
            l_translation = gettext.translation('abc2xmlGUI', localedir=pathLocale, languages=[self.lang])
        except FileNotFoundError:
            l_translation = gettext.translation('abc2xmlGUI', localedir=pathLocale, languages=['en'])
        l_translation.install()


    def startConversion(self): # Look for input and select appropriate converter
        self.txt = self.abcText.get('1.0', tk.END)
        self.txt = self.txt.strip()
        if (self.txt != "" and
            self.txt != self.installAbcText.strip() and
            self.txt != self.infoAbcText.strip()): # Check if abc or xml
            if self.txt.startswith('<?xml'):
                self.xml2abc()
            else:
                self.abc2xml()
        else:
            infotext = _("No abc or XML to convert.")
            self.userInfo('showwarning', infotext)


    def userInfo(self, type, info):
        exec('tk.messagebox.' + type + '(title="abc2xml GUI", message=info)')


    def whatPython(self): # Identify Python call
        pcalls = ["3", ""]
        for i, p in enumerate(pcalls): # Check which one works
            try:
                proc = subprocess.Popen(["python" + p, "-V"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                if (out.startswith("Python")):
                    return p
            except FileNotFoundError:
                if (i == 1):
                    return " not found"


    def wShowMessage(self, src, infotext): # Show converter messages
        mWindow = Toplevel(self.root)
        mWindow.title(src)
        mWindow['bg'] = '#ffdb00'
        mWindow.iconphoto(False, self.icon)

        tLabel = tk.Label(mWindow, text="=== " + src + " ===", bg='#4681b3', fg='white', font=('Helvetica', 13, 'bold'))
        iLabel = tk.Label(mWindow, text=infotext, bg='white', font='TkFixedFont',
                          anchor=tk.W, justify=tk.LEFT, padx=5, pady=10)
        tLabel.pack(fill='x', padx=5, pady=(5,0))
        iLabel.pack(fill='both', padx=5, pady=(0,5))

        mWindow.wait_visibility()
        x = self.root.winfo_x() + self.root.winfo_width()//2 - mWindow.winfo_width()//2
        y = self.root.winfo_y() + self.root.winfo_height()//2 - mWindow.winfo_height()//2
        mWindow.geometry(f'+{x}+{y}')


    def xml2abc(self):
        if (self.pathXml2Abc != ''):
            if (self.pathXml2Abc == 'import'): # If imported run as module, else start process
                lb = self.scoreLineBreak.get() == '-b'  # need a boolean for option x
                out, msg = xml2abc.vertaal(self.txt, x=lb)
            else:
                cmdList = self.prepCmdList(self.pathXml2Abc)
                proc = subprocess.Popen(cmdList, universal_newlines=True,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, msg = proc.communicate(self.txt)
            self.saveFile(out)
            if self.messages == 'on':
                self.wShowMessage('xml2abc', msg)
        else:
            infotext = _("This function needs xml2abc.\nCopy file into abc2xml GUI folder\nor enter path into abc2xmlGUI.ini.")
            self.userInfo('showerror', infotext)


class GUIButton(tk.Button):

    def __init__(self, col, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.col = col
        self['bg'] = '#ffdb00'
        self['font'] = ('Helvetica', 11)
        self['fg'] = 'darkblue'
        self.grid(row=1, column = self.col, sticky=tk.W+tk.E, padx=5, pady=(0,10))


abc2xmlGUI()