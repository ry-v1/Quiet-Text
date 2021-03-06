import tkinter as tk
import yaml
import os, sys
from tkinter.colorchooser import askcolor
from quiet_syntax_highlighting import SyntaxHighlighting


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        self.default_theme = parent.loader.load_default_theme()
        self.settings = parent.loader.load_settings_data()
        self.settings['menubar_active_bg'] = self.default_theme['menu_bg_active']
        self.settings['menubar_active_fg'] = self.default_theme['menu_fg_active']
        self.settings['menu_fg'] = self.default_theme['comment_color']
        self.settings['menu_bg'] = self.default_theme['bg_color']
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(parent.master,
                          font=font_specs,
                          fg=self.settings['menu_fg'],
                          bg=self.settings['menu_bg'],
                          activeforeground= self.settings['menubar_active_fg'],
                          activebackground= self.settings['menubar_active_bg'],
                          activeborderwidth=0,
                          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # adding features file dropdown in menubar
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        # new file creation feature
        file_dropdown.add_command(label='New File',
                                   accelerator='Ctrl+N',
                                   command=parent.new_file)
        # open file feature
        file_dropdown.add_command(label='Open File',
                                   accelerator='Ctrl+O',
                                   command=parent.open_file)
        # save file feature
        file_dropdown.add_command(label='Save',
                                   accelerator='Ctrl+S',
                                   command=parent.save)
        # Save as feature
        file_dropdown.add_command(label='Save As',
                                   accelerator='Ctrl+Shift+S',
                                   command=parent.save_as)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.on_closing)

        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(label='Edit Settings',
                                      command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(label='Reset Settings to Default',
                                      command=parent.reset_settings_file)

        #view dropdown menu
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(label='Toggle Menu Bar',
                                  accelerator='Alt',
                                  command=self.hide_menu)
        view_dropdown.add_command(label='Hide Status Bar',
                                  command=parent.hide_status_bar)
        view_dropdown.add_command(label='Toggle Line Numbers',
                                  accelerator='Ctrl+Shift+L',
                                  command=parent.toggle_linenumbers)
        view_dropdown.add_command(label='Toggle Text Border',
                                  command=self.toggle_text_border)
        view_dropdown.add_command(label='Toggle Horizontal Scrollbar',
                                  command=self.toggle_scroll_x)
        view_dropdown.add_command(label='Toggle Vertical Scrollbar',
                                  command=self.toggle_scroll_y)
        view_dropdown.add_command(label='Enter Quiet Mode',
                                  accelerator='Ctrl+Q',
                                  command=self.enter_quiet_mode)

        #tools dropdown menu
        tools_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(label='Open Color Selector',
                                   accelerator='Ctrl+M',
                                   command=self.open_color_picker)
        tools_dropdown.add_command(label='Run Selected File',
                                   accelerator='Ctrl+R',
                                   command=parent.run)

        #theme dropdown menu
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(label='Monokai',
                                   command=self.load_monokai)
        theme_dropdown.add_command(label='Monokai Pro',
                                   command=self.load_monokai_pro)
        theme_dropdown.add_command(label='Gruvbox',
                                   command=self.load_gruvbox)
        theme_dropdown.add_command(label='Solarized',
                                   command=self.load_solarized)
        theme_dropdown.add_command(label='Dark Heart',
                                   command=self.load_darkheart)
        theme_dropdown.add_command(label='Githubly',
                                   command=self.load_githubly)
        theme_dropdown.add_command(label='Dracula',
                                   command=self.load_dracula)
        theme_dropdown.add_command(label='Pumpkin',
                                   command=self.load_pumpkin)


        syntax_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        syntax_dropdown.add_command(label='Python3',
                                    command=self.syntax.load_python3_syntax)
        syntax_dropdown.add_command(label='JavaScript',
                                    command=self.syntax.load_javascript_syntax)
        syntax_dropdown.add_command(label='C',
                                    command=self.syntax.load_c_syntax)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='Tools', menu=tools_dropdown)
        menubar.add_cascade(label='Syntax', menu=syntax_dropdown)
        menubar.add_cascade(label='Color Schemes', menu=theme_dropdown)
        # menubar.add_cascade(label='About', menu=about_dropdown)

        self.menu_fields = [field for field in (file_dropdown, view_dropdown, syntax_dropdown,
                                                settings_dropdown, tools_dropdown, theme_dropdown)]

        self.default_settings = parent.default_theme
        for field in self.menu_fields:
            field.configure(bg=parent.default_theme['bg_color'],
                            fg=self.settings['menu_fg'],
                            activeforeground=parent.default_theme['menu_fg_active'],
                            activebackground=parent.default_theme['menu_bg_active'])

        # Settings reconfiguration function
    def reconfigure_settings(self):
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(bg=settings['menu_bg'],
                            fg=settings['menu_fg'],
                            activeforeground=settings['menu_active_fg'],
                            activebackground=settings['menu_active_bg'],
                            background = settings['textarea_background_color'],)

        self._menubar.configure(bg=settings['menu_bg'],
                                fg=settings['menu_fg'],
                                background = settings['textarea_background_color'],
                                activeforeground= settings['menubar_active_fg'],
                                activebackground= settings['menubar_active_bg'],)

    # color to different text tye can be set here
    def open_color_picker(self):
        return askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

    def toggle_text_border(self):
        settings = self._parent.loader.load_settings_data()
        border_status = settings['textarea_border']
        if border_status == 0:
          self._parent.textarea.configure(bd=0.5)
          settings['textarea_border'] = 0.5
        elif border_status > 0:
          self._parent.textarea.configure(bd=0)
          settings['textarea_border'] = 0
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_x(self):
        settings = self._parent.loader.load_settings_data()
        scrollx_width = settings['horizontal_scrollbar_width']
        if scrollx_width > 0:
          self._parent.scrollx.configure(width=0)
          settings['horizontal_scrollbar_width'] = 0
        elif scrollx_width == 0:
          self._parent.scrollx.configure(width=8)
          settings['horizontal_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_y(self):
        settings = self._parent.loader.load_settings_data()
        scrolly_width = settings['vertical_scrollbar_width']
        if scrolly_width > 0:
          self._parent.scrolly.configure(width=0)
          settings['vertical_scrollbar_width'] = 0
        elif scrolly_width == 0:
          self._parent.scrolly.configure(width=8)
          settings['vertical_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    # quiet mode is defined here
    def enter_quiet_mode(self):
        self._parent.enter_quiet_mode()

    # hiding the menubar
    def hide_menu(self):
        self._parent.master.config(menu='')

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)

    def load_monokai_pro(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/monokai_pro.yaml'))
        self.syntax.load_new_theme(theme)

    def load_monokai(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/monokai.yaml'))
        self.syntax.load_new_theme(theme)

    def load_gruvbox(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/gruvbox.yaml'))
        self.syntax.load_new_theme(theme)

    def load_solarized(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/solarized.yaml'))
        self.syntax.load_new_theme(theme)

    def load_darkheart(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/dark-heart.yaml'))
        self.syntax.load_new_theme(theme)

    def load_githubly(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/githubly.yaml'))
        self.syntax.load_new_theme(theme)

    def load_dracula(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/dracula.yaml'))
        self.syntax.load_new_theme(theme)

    def load_pumpkin(self):
        theme = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/Python3/pumpkin.yaml'))
        self.syntax.load_new_theme(theme)
