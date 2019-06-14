from os import path, getcwd

import subprocess

from tkinter import *


'''
This is meant to serve as a rapid prototype/proof-of-concept for using the Docker setup on Windows.
It is not pretty and by no means complete, but it gets the job done.

Known Issues:

* When building, the window becomes Unresponsive. This is normal, it will respond when the build is finished.

* When running, the window becomes Unresponsive. This is normal as well. It will respond when the build is finished.
'''


def main():
    window = Tk()
    window.title("NPS Docker Helper")
    window.geometry('600x300')

    '''
    THE BUILD BUTTON
    '''
    buildbutton = Button(window, text="Build", font=('Arial Bold', 10), background='yellow',
                         command=lambda: (update_build_button(buildbutton, buildlabel),
                                          update_run_button(runbutton, runlabel)))
    buildbutton.grid(column=0, row=0, padx=10, pady=10)

    buildlabel = Label(window, text="Not Built.", font=('Arial Bold', 10))
    buildlabel.grid(column=1, row=0, padx=10, pady=10)
    if is_image_built():
        buildlabel.configure(text="Image is built.")
        buildbutton.configure(background='yellow', text='Built', state=DISABLED, command=do_nothing)

    '''
    THE RUN BUTTON
    '''
    runbutton = Button(window, text="Run", font=('Arial Bold', 10), background='green')
    runbutton.grid(column=0, row=1, padx=10, pady=10)
    runbutton.configure(
        command=lambda: do_run(upload=upchk.get(), uname=uname.get(), token=token.get(), config=configchk.get(),
                               dump=dumpchk.get()))

    runlabel = Label(window, text="Ready to Run.", font=('Arial Bold', 10))
    runlabel.grid(column=1, row=1, padx=10, pady=10)

    update_run_button(runbutton, runlabel)

    '''
    THE REFRESH BUTTON
    '''
    refreshbutton = Button(window, text="Refresh", font=('Arial Bold', 10), background='green',
                           command=lambda: update_run_button(runbutton, runlabel))
    refreshbutton.grid(column=0, row=5, padx=10, pady=10)
    refreshlabel = Label(window, text="Check for mountdata or ENVIRONMENTS.zip.", font=('Arial Bold', 10))
    refreshlabel.grid(column=1, row=5, padx=10, pady=10)

    '''
    THE CONFIG OPTIONS
    '''
    # Upload
    upchk = IntVar()
    uploadbutton = Checkbutton(window, text="Upload", font=('Arial Bold', 10), variable=upchk)
    uploadbutton.grid(column=0, row=2, padx=10, pady=10)

    uname = Entry(window)
    uname.grid(column=1, row=2, padx=10, pady=10)
    uname.insert(0, 'username')
    uname.configure(background='light grey')

    token = Entry(window)
    token.insert(0, 'token')
    token.grid(column=2, row=2, padx=10, pady=10)
    token.configure(background='light grey')

    # Config File
    configchk = IntVar()
    configbutton = Checkbutton(window, text="Use Config.txt", font=('Arial Bold', 10), variable=configchk)
    configbutton.grid(column=0, row=3, padx=10, pady=10)

    # Create Dump
    dumpchk = IntVar()
    dumpbutton = Checkbutton(window, text="Dump output", font=('Arial Bold', 10), variable=dumpchk)
    dumpbutton.grid(column=0, row=4, padx=10, pady=10)

    window.mainloop()


def is_image_built():
    process = subprocess.Popen(['C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe',
                                'docker image ls | Select-String -Pattern "^npsbe" -quiet'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    out = out.decode("utf-8")
    err = err.decode("utf-8")

    if err != '':
        print("err:", err)

    if 'True' in out:
        return True

    return False


def build_image():
    subprocess.call(['C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe',
                     'docker build -t npsbe .'])
    return is_image_built()


def update_build_button(buildbutton, buildlabel):
    buildlabel.configure(text="Building image...")
    if build_image():
        buildlabel.configure(text="Image is built.")
        buildbutton.configure(background='yellow', text='Built', state=DISABLED, command=do_nothing)


def do_run(upload=0, uname='', token='', config=0, dump=0):
    envstr = ''
    if upload == 1:
        envstr += " --env MB_USER_ENV={} --env MB_TOKEN_ENV={}".format(uname, token)
    if config == 1:
        envstr += " --env DUMP_ENV=true"
    if dump == 1:
        envstr += " --env CONFIG_ENV=true"

    mdat = '/mountdata'
    cmnd = "docker run -it {} --mount type=bind,source={},target=/app/data npsbe --rm".format(envstr, getcwd() + mdat)
    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", cmnd])


def update_run_button(runbutton, runlabel):
    zipready = True
    mountready = True
    buildready = True

    if not is_zip_there():
        runlabel.configure(text="No ENVIRONMENTS.zip found.")
        runbutton.configure(background='yellow', text='Run', state=DISABLED)
        zipready = False

    if not is_mountdata_there():
        runlabel.configure(text="No mountdata folder detected.")
        runbutton.configure(background='yellow', text='Run', state=DISABLED)
        mountready = False

    if not is_image_built():
        runlabel.configure(text="No Image Has been built.")
        runbutton.configure(background='yellow', text='Run', state=DISABLED)
        buildready = False

    if zipready and mountready and buildready:
        runlabel.configure(text="Ready to Run.")
        runbutton.configure(background='green', text='Run', state=NORMAL)


def is_mountdata_there():
    if path.exists('mountdata') and path.isdir('mountdata'):
        return True
    return False


def is_zip_there():
    if path.exists('mountdata/ENVIRONMENTS.zip') and path.isfile('mountdata/ENVIRONMENTS.zip'):
        return True
    return False


def do_nothing():
    pass


if __name__ == '__main__':
    main()
