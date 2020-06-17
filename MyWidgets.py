# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk


class MultiListbox(tk.Frame):
    def __init__(self, master, lists):
        tk.Frame.__init__(self, master)
        self.lists = []
        for l,w in lists:
            frame = tk.Frame(self); frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
            tk.Label(frame, text=l, borderwidth=1, relief=tk.FLAT, bg='tomato', fg='#fffffe').pack(fill=tk.X)
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=tk.FLAT, exportselection=tk.FALSE)
            lb.pack(expand=tk.YES, fill=tk.BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = tk.Frame(self); frame.pack(side=tk.LEFT, fill=tk.Y)
        #tk.Label(frame, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
        self.sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self._scroll)
        self.sb.pack(expand=tk.YES, fill=tk.Y)
        self.lists[0]['yscrollcommand']= self.sb.set
        # for l in self.lists:
        #     l.bind('<MouseWheel>', self._scroll)
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, tk.END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
            #self.sb.config(command = l.yview) 
            #tk.Apply(l.yview, args)

    def curselection(self):
        return self.lists[0].curselection(  )

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size(  )

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)


    
class ScrolledWindow(tk.Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected 
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars
        self.xscrlbr = ttk.Scrollbar(self.parent, orient = 'horizontal')
        #self.xscrlbr.grid(column = 0, row = 1, sticky = 'ew', columnspan = 2)
                 
        self.yscrlbr = ttk.Scrollbar(self.parent)
        #self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')      
        self.yscrlbr.pack(side='right', expand=True, fill='y')
        # creating a canvas
        self.canv = tk.Canvas(self.parent)
        self.canv.config(relief = 'flat',
                         width = 10,
                         heigh = 10, bd = 2)
        # placing a canvas into frame
        #self.canv.grid(column = 0, row = 0, sticky = 'nsew')
        self.canv.pack(side='left', expand=True, fill='both')
        # accociating scrollbar comands to canvas scroling
        self.xscrlbr.config(command = self.canv.xview)
        self.yscrlbr.config(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = ttk.Frame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(xscrollcommand = self.xscrlbr.set,
                         yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, 100, 100))

        self.yscrlbr.lift(self.scrollwindow)        
        self.xscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)  
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")  

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width = self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height = self.scrollwindow.winfo_reqheight())

if __name__ == '__main__':
    root = tk.Tk()
    tk.Label(root, text='MultiListbox').pack()
    mlb = MultiListbox(root, (('Subject', 40), ('Sender', 20), ('Date', 10)))
    for i in range(1000):
      mlb.insert(tk.END, 
          ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
    mlb.pack(expand=tk.YES,fill=tk.BOTH)
    root.mainloop(  )