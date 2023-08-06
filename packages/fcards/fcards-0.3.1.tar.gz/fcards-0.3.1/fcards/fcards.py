# Card files are csv files that contain cards. Each card has a front and a back

import curses
import glob
import os
import textwrap as tw
import csv
import math
from copy import copy

HOME_DIR = os.path.expanduser('~')

stdscr = curses.initscr()

menu = ['Practice', 'Edit']
current = 0

if not os.path.isdir(HOME_DIR+"/.cards"):
    os.mkdir(HOME_DIR+"/.cards")

def addwrappedstr(stdscr, y, x, text, color=None, center_y=False, cursor_pos=None):
    
    # If center_y is true, we wrap the text such that lines are added above and below the input
    # coordinates such that the text remains centered on the input coordinates 
    # instead of starting at the coordinates and going down from there.
    # This can cause problems as the text printed may interfere with other text
    # previously printed above the input coordinates, so it should only really be used
    # in situations where the text is being printed to the screen in an area where we can
    # be sure there is nothing close to it
    #
    # If cursor_pos is fed in, we keep track of the coordinates of the character that
    # has cursor_pos as an index in text so that the function can return these coordinates

    h, w = stdscr.getmaxyx()
    text = tw.wrap(text, int(w*0.9), drop_whitespace=False)
    line_lengths = [len(line) for line in text]
    if cursor_pos != None:
        i = 1
        while sum(line_lengths[:i]) < cursor_pos:
            i += 1
        cursor_pos -= sum(line_lengths[:i-1])
        if center_y:
            try:
                cursor_pos = [w//2 - line_lengths[i-1]//2 + cursor_pos, y+i-len(text)//2-1]
            except:
                cursor_pos = [w//2 + cursor_pos, y+i-len(text)//2-1]
        else:
            try:
                cursor_pos = [w//2 - line_lengths[i-1]//2 + cursor_pos, y+i]
            except:
                cursor_pos = [w//2 + cursor_pos, y+i]


    for i, line in enumerate(text):
        if center_y:
            new_x, new_y = w//2-len(line)//2, y+i-len(text)//2
        else:
            new_x, new_y = w//2-len(line)//2, y+i
        if color != None:
            stdscr.addstr(new_y, new_x, line, color)
        else:
            stdscr.addstr(new_y, new_x, line)
    return [len(text), cursor_pos]

def draw_menu(stdscr, menu, current, title=None, info=None):
    
    h, w = stdscr.getmaxyx()
    title_x, title_y, info_x, info_y = w//2, 0, w//2, h
    
    menu_length = sum([len(tw.wrap(item, int(w*0.9))) for item in menu])
    available_space = h-20
    menu_visible = copy(menu)
    i = 0
    while sum([len(tw.wrap(item, int(w*0.9))) for item in menu_visible]) > available_space:
        in_front = sum([len(tw.wrap(item, int(w*0.9))) for item in menu_visible[:current]])
        behind   = sum([len(tw.wrap(item, int(w*0.9))) for item in menu_visible[current:]])
        if in_front > behind:
            if current != 0:
                menu_visible.pop(0)
                current -= 1
        else:
            if current != len(menu_visible)-1:
                menu_visible.pop()
        i+=1
    
    y_offset = 0
    if title != None:
        title_x, title_y = w//2-len(title)//2, h//2-len(menu_visible)//2-2
        addwrappedstr(stdscr, title_y, title_x, title)
    if info != None:
        info_x, info_y = w//2-len(info)//2, h - 3 - len(tw.wrap(info, int(w*0.9)))
        addwrappedstr(stdscr, info_y, info_x, info)
    
    for i, elem in enumerate(menu_visible):
        x, y = w//2-len(elem)//2, h//2-len(menu_visible)//2+y_offset
        if i==current:
            y_offset += addwrappedstr(stdscr, y, x, elem, curses.color_pair(1))[0]
        else:
            y_offset += addwrappedstr(stdscr, y, x, elem)[0]

def interactive_menu(stdscr, menu, current, title=None, delete=False, info=None):
    
    while True:

        stdscr.clear()
        draw_menu(stdscr, menu, current, title, info)
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_UP:
            current = max(0, current-1)
        elif c == curses.KEY_DOWN:
            current = min(len(menu)-1, current+1)
        elif c == curses.KEY_ENTER or c in [10, 13]:
            return current
        elif c == ord('d'):
            if delete and menu[current] not in ["New Card", "New Cardset"]:
                if interactive_menu(stdscr, ["Delete", "Cancel"], 0, title="Are you sure you want to delete that?") == 0:
                    return ["DELETE", current]
        elif c == ord('q'):
            return "BACK"

def input_box(stdscr, title=None, text=''):
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    cursor_pos = len(text)
    while True:
        x, y = w//2-len(text)//2, h//2
        stdscr.clear()
        if title!=None:
            i = len(tw.wrap(title, int(w*0.9))) + max(len(tw.wrap(text, int(w*0.9)))//2+1, 1)
            x_, y_ = w//2-len(title)//2, h//2-i
            addwrappedstr(stdscr, y_, x_, title)
        cx, cy = addwrappedstr(stdscr, y, x, text, center_y=True, cursor_pos=cursor_pos)[1]
        stdscr.move(cy, cx)
        stdscr.refresh()
        c = stdscr.getch()
        if c == curses.KEY_ENTER or c in [10, 13]:
            curses.curs_set(0)
            return text
        elif c == curses.KEY_LEFT:
            cursor_pos = max(0, cursor_pos-1)
        elif c == curses.KEY_RIGHT:
            cursor_pos = min(len(text), cursor_pos+1)
        elif c == curses.KEY_BACKSPACE or c == 127:
            text = text[:max(0, cursor_pos-1)] + text[cursor_pos:]
            cursor_pos = max(0, cursor_pos-1)
        else:
            text = text[:cursor_pos] + chr(c) + text[cursor_pos:]
            cursor_pos += 1

def practice(stdscr):
    
    h, w = stdscr.getmaxyx()

    cardsets = [cardset[len(HOME_DIR)+8:-4] for cardset in glob.glob(HOME_DIR+"/.cards/*.csv")]
    if len(cardsets) == 0:
            stdscr.clear()
            t = "No Cardsets. Create Some In The Edit Menu"
            x, y = w//2-len(t)//2, h//2
            addwrappedstr(stdscr, y, x, t)
            stdscr.getch()
            return

    current = 0
    
    while True:

        i = "Move: [arrow keys], select: [enter], back: [q]"
        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:', info=i)
        if selected == "BACK":
            return
        
        cardfile = HOME_DIR+"/.cards/"+cardsets[selected]+".csv"
        cards = csv.reader(open(cardfile), delimiter=',')
        cards = [row for row in cards]
        if cards == []:
            stdscr.clear()
            t = "No Cards In This Set"
            x, y = w//2-len(t)//2, h//2
            addwrappedstr(stdscr, y, x, t)
            stdscr.getch()
        else:
            i=0
            while True:
                stdscr.clear()
                if i%2==0:
                    t = cards[i//2%len(cards)][0]
                else:
                    t = cards[i//2%len(cards)][1]
                x, y = w//2-len(t)//2, h//2
                addwrappedstr(stdscr, y, x, t, center_y=True)
                stdscr.refresh()
                if stdscr.getch() == ord('q'):
                    break
                i+=1   

def edit(stdscr):

    h, w = stdscr.getmaxyx()

    current = 0
    
    while True:

        cardsets = ["New Cardset"] + [cardset[len(HOME_DIR)+8:-4] for cardset in glob.glob(HOME_DIR+"/.cards/*.csv")]
        i = "Move: [arrow keys], select: [enter], back: [q], delete: [d]"
        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:', delete=True, info=i)
        if type(selected) == list and selected[0] == "DELETE":
            os.remove(HOME_DIR+"/.cards/"+cardsets[selected[1]]+".csv")
            continue
        if selected == "BACK":
            return
        if selected == 0:
            cardfile = HOME_DIR+"/.cards/"+input_box(stdscr, "Select Name:")+".csv"
            cards = []
        else: 
            cardfile = HOME_DIR+"/.cards/"+cardsets[selected]+".csv"
            cards = csv.reader(open(cardfile), delimiter=',')
            cards = [row for row in cards]
        
        menu_cards = ["New Card"] + [' || '.join(elem) for elem in cards]

        while True:

            current = 0
            if menu_cards == ["New Card"]:
                selected = interactive_menu(stdscr, menu_cards, current, title="Cardset Empty:", info=i)
            else:
                selected = interactive_menu(stdscr, menu_cards, current, title="Loaded Cards:", delete=True, info=i)
            if type(selected) == list and selected[0] == "DELETE":
                cards.remove(cards[selected[1]-1]) 
                menu_cards.remove(menu_cards[selected[1]])
                f = open(cardfile, "w")
                f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                [f_writer.writerow(cards) for cards in cards]
                f.close()
                continue
            if selected == "BACK":
                break
            else:
                if selected == 0:
                    f = input_box(stdscr, "Front Of Flashcard:", "")
                    b = input_box(stdscr, "Back Of Flashcard:", "")
                    cards.append([f, b])
                else:
                    f = input_box(stdscr, "Front Of Flashcard:", cards[selected-1][0])
                    b = input_box(stdscr, "Back Of Flashcard:", cards[selected-1][1])
                    cards[selected-1] = [f, b]
                menu_cards = ["New Card"] + [' || '.join(elem) for elem in cards]
                f = open(cardfile, "w")
                f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                [f_writer.writerow(cards) for cards in cards]
                f.close()


def fcards(stdscr, menu, current):

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    while True:
        im = interactive_menu(stdscr, menu, current)
        if im == "BACK":
            break
        elif im == 0:
            practice(stdscr)
        else:
            edit(stdscr)

def main():
    curses.wrapper(fcards, menu, current)

if __name__=="__main__":
    main()

