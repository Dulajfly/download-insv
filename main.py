import os
from lxml import html
import requests
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo, showerror

def download_insv_files(url_content, req: object, path: str) -> None:
    """
    Downloads all .insv files from a given url

    Returns
    -------
    'None'
        Returns none, only create .insv files in entered path

    """
    for item in url_content:
        if os.path.splitext(item)[1] == '.insv':
            file_name = os.path.split(item)[1]
            item_url = requests.get(req.url + item, stream=True)
            os.chdir(path)
            with open(file_name, 'wb') as file:
                for chunk in item_url.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)


def get_url_content() -> tuple[object, object]:
    """
    Get links from webpage content

    Returns
    -------
    'str'


    """
    req = requests.get('http://192.168.42.1/DCIM/Camera01/')
    # req = requests.get('http://127.0.0.1:5500/DCIM/Camera01/')
    page = html.fromstring(req.content)
    result = page.xpath('//a/@href')
    return result, req


def run_script():
    """
    Run script

    Returns
    -------
    None
        Running script

    """
    try:
        content = get_url_content()
        download_insv_files(content[0], content[1], app.folder_path.get())
        showinfo('Success', 'Successfully downloaded the files')
    except Exception as e:
        showerror('Error', 'Failed to download files, there is a problem')


def set_download_path():
    """
    Sets the path where the files should be extracted

    Returns
    -------

    """
    path_entry.delete(0, 'end')
    app.folder_path.set(askdirectory(mustexist=True))
    path_entry.insert(0, app.folder_path.get())


# Tkinter Settings Section
app = Tk()
app.title('Download .insv files')
app.geometry('400x170')

# Variables Section
app.folder_path = StringVar()
Label(app, text='Select the path where to \nsave the .insv files.').grid(padx=20, pady=10)
path_entry = Entry(app, textvariable='http://127.0.0.1:5500', width=40)
select_path_button = Button(app, text='Browse path', command=set_download_path)
run_script_button = Button(app, text='Run', command=run_script)

# Grid Section
path_entry.grid(row=1, column=0, pady=20, padx=10)
select_path_button.grid(row=1, column=1, pady=20, padx=10)
run_script_button.grid(row=2, column=0, pady=10, padx=10)

app.mainloop()
