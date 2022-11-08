# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

#App Vars

myTerm = 'alacritty'


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = ["㊀", "㊁", "㊂", "㊃", "㊄", "㊅", "㊆", "㊇", "㊈", "X"]
group_labels = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadwide",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":3,
            "border_focus": "#B05E63",
            "border_normal": "#1B365422"
            }

layout_theme = init_layout_theme()


layouts = [
    #layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    #layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
def init_colors():
    return [["#1B3654"],   	 # color 0 	BG
            ["#B05E63"],     # color 1 	
            ["#544C6E"],     # color 2 	
            ["#9993B9"],     # color 3 	
            ["#D7A67E"],     # color 4 	
            ["#85213D"],     # color 5 	
            ["#465457"],     # color 6 
            ["#883920"],     # color 7
            ['#1B3654']]   	 # Color 8  FG

colors = init_colors()

# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Teko",
                fontsize = 20,
				)
widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
	    widget.CurrentLayoutIcon(
			foreground = '#1B3654',
			background = '#b05e63',
			width = 80,
			padding = 5,
			scale=0.80
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/icon-page.png',
		),
		widget.GroupBox(
			font="RobotoSlab Bold",
			borderwidth = 0,
			disable_drag = True,
			active = colors[4],
			inactive = colors[0],
			rounded = True,
			highlight_method = "text",
			this_current_screen_border = colors[5],
			background = '#c07568'
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/page-sys.png',
		),
		widget.Systray(
			background='#cd8d71',
			icon_size=20,
			width = 150,
			padding = 0,
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/sys-update.png',
		),
		widget.Image(
			filename='~/.config/qtile/icons/status/pac.png',
		),
		widget.CheckUpdates(
			colour_have_updates=colors[0],
			colour_no_updates=colors[0],
			background='#d7a67e',
			distro = 'Arch_checkupdates',
			display_format = '{updates} Updates',
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
            no_update_string = 'Up to date',
            initial_text = 'Searching',
            width = 115,
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/update-end.png',
		),
			
			
		widget.TextBox(
			font="FontAwesome",
			text="",
			foreground=colors[0],
			background=colors[8],
			fontsize=16,
			width=80,
			),
			
		widget.Image(
			filename='~/.config/qtile/icons/seperators/down-end.png',
		),
		widget.TextBox(
			font="FontAwesome",
			text="  ",
			foreground='#f8f8f8',
			background=colors[1],
			padding = 0,
			fontsize=16
			),
		widget.Net(
			foreground='#f8f8f8',
			background=colors[1],
			format = '{down}',
			padding = 0,
			width = 60
			),
		widget.Clock(
			font = 'RobotoSlab Bold',
			fontsize = 16,
			foreground = '#f8f8f8',
			background = colors[7],
			format="%A %d %B %Y  %X",
			width = 290
			),
		widget.TextBox(
			font="FontAwesome",
			text="  ",
			foreground='#f8f8f8',
			background=colors[2],
			padding = 0,
			fontsize=16
			),
		widget.Net(
			foreground='#f8f8f8',
			background=colors[2],
			format = '{up}',
			padding = 0,
			width = 70,
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/up-end.png',
		),
			
		widget.TextBox(
			font="FontAwesome",
			text="",
			foreground=colors[8],
			background=colors[8],
			fontsize=16,
			width=80,
			),
			
		widget.Image(
			filename='~/.config/qtile/icons/seperators/temp-end.png',
		),
		widget.Image(
			filename='~/.config/qtile/icons/status/temp.png',
		),
		widget.ThermalSensor(
			foreground = colors[0],
			foreground_alert = colors[1],
			background = '#d7a67e',
			metric = True,
			threshold = 50,
			padding = 3,
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/bat-temp.png',
		),
		widget.Image(
			filename='~/.config/qtile/icons/status/bat.png',
		),
			widget.Battery(
			update_interval = 1,
			format = '{percent: 2.0%}',
			low_percentage=20.0,
			low_forground=colors[1],
			foreground = colors[0],
			background = '#cd8d71',
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/cpu-bat.png',
		),
		widget.Image(
			filename='~/.config/qtile/icons/status/intel-cpu.png',
		),
		widget.CPU(
			foreground = colors[0],
			background='#c07568',
			core = "all",
			width = 125,
			),
		widget.Image(
			filename='~/.config/qtile/icons/seperators/ram-cpu.png',
		),
		widget.Image(
			filename='~/.config/qtile/icons/status/ram.png',
		),
		widget.Memory(
			format = '{MemUsed: .0f}MB ',
			update_interval = 1,
			foreground = colors[0],
			background = '#b05e63',
            		),
        	widget.TextBox(
			font="FontAwesome",
			text="",
			foreground=colors[0],
			background='#b05e63',
			padding = 0,
			fontsize=16
			),
        	widget.Memory(
			format = '{MemTotal: .0f}MB',
			update_interval = 1,
			foreground = colors[0],
			background = '#b05e63',
			width = 100,
            )    
    ]
    return widgets_list

widgets_list = init_widgets_list()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()


def init_screens():
    return [
    Screen(
		top=bar.Bar(
			widgets=widgets_screen1,
			background = '#000000',
			size = 25,
			opacity = 1,
			margin = [7, 7, 2, 7],
			border_color ='#1B3654',
			border_width = [2, 0, 2, 0],
			),
		),
    ]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
 #@hook.subscribe.client_new
# def assign_app_group(client):
     #d = {}
     #####################################################################################
     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
     #####################################################################################
     #d[group_names[0]] = ["Firefox"]
     #d[group_names[1]] = ["Geany"]
     #d[group_names[2]] = ["steam"]
     #d[group_names[3]] = ["thunar", "Thunar"]
     #d[group_names[4]] = ["Gimp", "gimp"]
     #d[group_names[5]] = ["Vlc","vlc"]
     #d[group_names[6]] = [""]
     #d[group_names[7]] = [""]
     #d[group_names[8]] = ["Alacritty", "Alacritty"]
     #d[group_names[9]] = ["apple-music-for-linux", "apple-music-for-linux"]
     ######################################################################################

# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='archlinux-logout.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class='nitrogen'),



],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "Qtile"
