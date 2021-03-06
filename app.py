# -----------------------------------------------------------------------------
# Copyright (c) 2019 Brennan Goewert

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import os
import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.simpledialog as tkSimpleDialog
import logging
import sys
import ctypes
import platform
import time
import subprocess
import copyuserfiles as cuf
from hostnameselect import HostnameSelect
from usernameselect import UsernameSelect

# tkinter root vars
root = tk.Tk()
root.title('Copy User Files')
root.geometry('720x540')
root.minsize(300, 300)
root.resizable(True, True)
root.focus()

# tkinter string values
str_src_dir = tk.StringVar()
str_dest_dir = tk.StringVar()
str_aduser = tk.StringVar()
str_username = tk.StringVar()
str_hostname = tk.StringVar()
str_docs_loc = tk.StringVar()

# tkinter integers and booleans
bool_copy_downloads = tk.BooleanVar()
bool_documents_loc = tk.BooleanVar()

# ldap vars
host = HostnameSelect(root)


# Checks to see if user is administrator
def is_admin():
    logging.info('Checking user privledges...')
    try:
        # Requests administrator permission for the python script
        logging.info('Checking if user is admin...')
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        logging.info('User is not admin!')
        return False


def cmd_select_dir(str_var):
    """ Opens a file dialog to select a source directory."""
    str_var.set(tkFileDialog.askdirectory())


def cmd_get_listselect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    return w.selection_set(0)


def cmd_select_hostname(frame):
    host.get_name(frame, str_hostname)


def cmd_select_username(frame):
    UsernameSelect(frame, str_username, str_hostname.get())


def cmd_start():
    """ try:
        start = subprocess.call(['py', 'copyuserfiles.py',
                                 '-u', os.path.basename(str_src_dir.get()),
                                 '-d', str_dest_dir.get(),
                                 '-H', str_hostname.get(),
                                 '-D', str_docs_loc.get()])
    except:
        logging.exception('Unable to run subprocess') """
    cuf.copyuserfiles(str_dest_dir.get(),
                      str_src_dir.get(),
                      str_username.get(),
                      str_hostname.get())


def dir_select_label_group(frame):
    # Directory selection group
    grp_dirs = tk.LabelFrame(frame)
    grp_dirs.grid(row=0, column=0, pady=(0, 5), sticky='we')
    grp_dirs.grid_columnconfigure(2, weight=1)

    # Remote hostname entry
    rm_host_label = tk.Label(grp_dirs, text='Remote Hostname: ', )
    rm_host_entry = tk.Entry(grp_dirs, textvariable=str_hostname)
    rm_host_btn = tk.Button(grp_dirs,
                            text='Select Host',
                            command=lambda: cmd_select_hostname(frame))
    rm_host_label.grid(row=0, column=1, sticky='e')
    rm_host_entry.grid(row=0, column=2, sticky='we')
    rm_host_btn.grid(row=0, column=0, sticky='we')

    # Username
    username_label = tk.Label(grp_dirs, text='Username: ', )
    username_entry = tk.Entry(grp_dirs, textvariable=str_username)
    username_btn = tk.Button(grp_dirs,
                             text='Select Username',
                             command=lambda: cmd_select_username(frame))
    username_label.grid(row=1, column=1, sticky='e')
    username_entry.grid(row=1, column=2, columnspan=2,
                        sticky='we', padx=(0, 5))
    username_btn.grid(row=1, column=0, sticky='we')

    # Source directory
    src_dir_label = tk.Label(grp_dirs, text='Source Directory: ', )
    src_dir_entry = tk.Entry(grp_dirs, textvariable=str_src_dir)
    src_dir_btn = tk.Button(grp_dirs,
                            text='Select Source',
                            command=lambda: cmd_select_dir(str_src_dir))
    src_dir_label.grid(row=2, column=1, sticky='e')
    src_dir_entry.grid(row=2, column=2, columnspan=2, sticky='we', padx=(0, 5))
    src_dir_btn.grid(row=2, column=0, sticky='we')

    # Destination directory
    dest_dir_label = tk.Label(grp_dirs, text='Destination Directory: ', )
    dest_dir_entry = tk.Entry(grp_dirs, textvariable=str_dest_dir)
    dest_dir_btn = tk.Button(grp_dirs,
                             text='Select Destintation',
                             command=lambda: cmd_select_dir(str_dest_dir))
    dest_dir_label.grid(row=3, column=1, sticky='e')
    dest_dir_entry.grid(row=3, column=2, columnspan=2, sticky='we',
                        padx=(0, 5))
    dest_dir_btn.grid(row=3, column=0, sticky='we')


def remote_actions_label_group(frame):
    # Remote actions frame
    grp_remote = tk.LabelFrame(frame)
    grp_remote.grid(row=1, column=0, pady=(0, 5), sticky='we')
    grp_remote.columnconfigure(0, weight=1)

    # Remote actions sub-frame
    grp_remote_actions = tk.LabelFrame(grp_remote)
    grp_remote_actions.grid(row=1, column=0, pady=(0, 5), sticky='we')
    grp_remote_actions.columnconfigure(0, weight=0)
    grp_remote_actions.columnconfigure(1, weight=1)
    grp_remote_actions.config(bd=0)

    # Remote documents folder location checkbox
    chk_documents_loc = tk.Checkbutton(grp_remote,
                                       text='Set remote documents folder' +
                                       ' location',
                                       variable=bool_documents_loc,
                                       command=lambda:
                                       grp_remote_actions.grid() if
                                       bool_documents_loc.get() else
                                       grp_remote_actions.grid_remove())
    chk_documents_loc.grid(row=0,
                           column=0,
                           sticky='w',
                           padx=(1, 15))

    # Remote hostname entry
    """
    rm_host_label = tk.Label(grp_remote_actions, text='Remote Hostname: ', )
    rm_host_entry = tk.Entry(grp_remote_actions, textvariable=str_hostname)
    rm_host_btn = tk.Button(grp_remote_actions,
                            text='Remote Hosts',
                            command=lambda: cmd_select_hostname(frame))
    rm_host_label.grid(row=0, column=0, sticky='e')
    rm_host_entry.grid(row=0, column=1, sticky='we')
    rm_host_btn.grid(row=0, column=2, sticky='we')
    """

    # Remote documents folder target location entry
    rm_docs_label = tk.Label(grp_remote_actions, text='Documents ' +
                             'Target Location: ', )
    rm_docs_entry = tk.Entry(grp_remote_actions, textvariable=str_docs_loc)
    rm_docs_label.grid(row=1, column=0, sticky='e')
    rm_docs_entry.grid(row=1, column=1, sticky='we')

    grp_remote_actions.grid_remove()


def action_label_group(frame):
    # Action button group
    grp_actions = tk.LabelFrame(frame)
    grp_actions.grid(row=2, column=0, pady=(0, 5), sticky='we')

    # Start button
    btn_start = tk.Button(grp_actions,
                          text='Start',
                          bg='#209920',
                          width=5)
    btn_start.bind('<Button-1>',
                   lambda e: cmd_start())
    btn_start.grid(row=0, column=0, sticky='we')

    # Stop button
    btn_stop = tk.Button(grp_actions,
                         text='Stop',
                         bg='#aa2020',
                         width=5,
                         command=cuf.stop)
    btn_stop.grid(row=0, column=1, sticky='we')

    # Copy Downloads checkbox
    chk_copy_downloads = tk.Checkbutton(grp_actions,
                                        text='Copy Downloads Folder (Limited' +
                                        ' to 50 most recent files)',
                                        variable=bool_copy_downloads)
    chk_copy_downloads.grid(row=0, column=2, sticky='w',
                            padx=(15, 15))


def header():
    """ Header frame """

    fra_header = tk.Frame(root)
    fra_header.grid_columnconfigure(0, weight=1)
    fra_header.grid_rowconfigure(0, weight=1)

    dir_select_label_group(fra_header)

    remote_actions_label_group(fra_header)

    action_label_group(fra_header)

    # Pack all the widgets
    fra_header.pack(side='top', padx=10, pady=10, fill='x')


def body():
    """ Body frame """

    fra_body = tk.Frame(root)
    fra_body.grid_columnconfigure(0, weight=1)
    fra_body.grid_rowconfigure(0, weight=1)

    txt_results = tk.Text(fra_body, width=20, height=5)
    txt_results_scroll = tk.Scrollbar(fra_body,
                                      orient='vertical',
                                      command=txt_results.yview)
    txt_results.config(state='disabled', yscrollcommand=txt_results_scroll.set)

    txt_results.grid(row=0, column=0, sticky='nswe')

    # Pack all the widgets
    fra_body.pack(side='top', fill='both', expand=True)


def footer():
    """ Footer frame """

    fra_footer = tk.Frame(root, height=15)
    fra_footer.grid_columnconfigure(0, weight=1)
    fra_footer.grid_rowconfigure(0, weight=1)

    lbl_version = tk.Label(fra_footer, text='Ver: ' +
                           cuf.__version__)
    lbl_version.grid(row=0, column=0)

    # Pack all the widgets
    fra_footer.pack(side='bottom')


def check_python():
    if sys.version_info[0] is 3:
        logging.info('Running correct version of python!')
    else:
        logging.warning('Running older version of python!')
        logging.warning('Some features might not work with older versions!')


def init():
    logging.info('Started application at: ' + time.ctime())
    logging.info('-===========- [ INIT ] -===========-')
    logging.info('-==- [ SYS INFO ] -==-')
    logging.info('system    : ' + platform.system())
    logging.info('release   : ' + platform.release())
    logging.info('version   : ' + platform.version())
    logging.info('node      : ' + platform.node())
    logging.info('machine   : ' + platform.machine())
    logging.info('processor : ' + platform.processor())
    logging.info('-==- [ SYS INFO ] -==-')
    logging.info('-==- [ APP INFO ] -==-')
    logging.info('python    : ' + platform.python_version())
    logging.info('version   : ' + cuf.__version__)
    logging.info('-==- [ APP INFO ] -==-')
    check_python()
    if is_admin():
        logging.info('User is admin! Proceeding through the application...')
        logging.info('-===========- [ INIT ] -===========-')
        main()
    else:
        logging.error('User is not admin! Prompting UAC elevation...')
        logging.error('This will restart the application!')
        logging.error('Stopped application at: ' + time.ctime())
        logging.info('-===========- [ INIT ] -===========-')
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable,
                                            __file__, None, 1)


def app():
    """ The main UI and application """

    header()
    logging.info('Header created!')

    body()
    logging.info('Body created!')

    footer()
    logging.info('Footer created!')


def main():
    """Main guts for the application and the process that keeps it alive"""
    logging.info('Starting GUI...')
    app()
    logging.info('GUI started!')
    root.mainloop()


if __name__ == "__main__":
    init()
