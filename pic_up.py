# -*- coding: utf-8 -*-
# @File  : pic_up.py
# @Author: Linfree
# @Date  : 2018-10-27
# @Desc  :

# -*- coding: utf-8 -*-


import wx
import wx.xrc
import os
import requests
from urllib.request import urlopen
from urllib.parse import quote

url = 'https://sm.ms/api/upload'


def up_file(url, filepath, data):
    '''
        文件上传
    :param url: 'https://sm.ms/api/upload'
    :param filepath: upload file path ,C:/picture/123.jpg
    :param data: 
    :return: requests json
    '''
    files = {'smfile': (quote(os.path.basename(filepath)), open(filepath, 'rb'))}
    response = requests.post(url, files=files, data=data)
    res_json = response.json()
    return res_json


# Drag the file
class FileDrop(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, filePath):  # 当文件被拖入后，会调用此方法
        filename = filePath[0]
        result = up_file(url, filename, {})
        self.parent.UpEnd(result, filename)
        return True
        # self.grid.SetCellValue(cellCoords.GetRow(), cellCoords.GetCol(), filename)  # 将文件名赋给被拖入的cell


class MyFrame(wx.Frame):
    """
    A Frame that says Hello World
    """
    lock = "index"
    result = {}

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MyFrame, self).__init__(*args, **kw)
        # create a panel in the frame
        self.makeBase()
        # create a menu bar
        self.makeMenuBar()
        # create result page
        self.makeResultPage2()

        # set page status，default :index
        self.setLock()

    def makeBase(self):
        '''
        create index page
        :return: 
        '''
        pnl = wx.Panel(self)
        # Create a hidden button,Assist in the implementation of 'ctrl+v'
        button = wx.Button(pnl, wx.ID_ANY, size=(0, 0))
        # add sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(pnl, label="\n\n将文件拖放到此区域\n或复制文件后粘贴\n（Ctrl+V）")
        # set big font
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)
        # align center
        border = (self.GetSize()[0] - st.GetSize()[0]) / 2.2
        sizer.Add(st, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER, border=border)

        # 文件拖动功能 file drop
        self.fileDrop = FileDrop(self)  # 第1步，创建FileDrop对象，并把self传给初始化函数
        pnl.SetDropTarget(self.fileDrop)  # 第2步，调用grid的SetDropTarget函数，并把FileDrop对象传给它

        # 以下两行为设置快捷键代码 Set Accelerator Table
        accelTbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('V'), button.GetId())])
        self.SetAcceleratorTable(accelTbl)

        # 绑定事件
        # self.pnl.Bind(wx.EVT_SIZE, self.OnChange)
        self.Bind(wx.EVT_BUTTON, self.OnCopyFile, button)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        pnl.SetSizer(sizer)

        self.pnl = pnl

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        # helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
        #                             "Help string shown in status bar for this menu item")

        indexItem = fileMenu.Append(-1, "&首页...\tCtrl-I")
        historyItem = fileMenu.Append(-1, "&历史...\tCtrl-H")

        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT, '退出')

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, "关于作者")
        softItem = helpMenu.Append(-1, "关于软件")
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&菜单")
        menuBar.Append(helpMenu, "&帮助")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHistory, historyItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnIndex, indexItem)
        self.Bind(wx.EVT_MENU, self.OnSoft, softItem)

    def makeResultPage(self):
        '''
        Discard!!
        :return: 
        '''
        self.pnl2 = wx.Panel(self, -1, size=self.pnl.GetSize())

        pnl2_width, pnl2_height = self.pnl2.GetSize()
        border = 5
        line_height = 28  #
        title_width = 70  # 文本标题的宽度
        button_width = 70  # copy按钮的宽度
        sys_button_width = 90  # 底部按钮的宽度

        # 底部按钮的高度
        pos_height_sys = pnl2_height - (border + line_height)
        # url行的高度
        pos_height_line1 = pos_height_sys - (2 * (line_height + border))
        # markdown行的高度
        pos_height_line2 = pos_height_sys - (line_height + border)
        # 图片的大小
        image_size = (pnl2_width - (2 * border), pos_height_line1 - 2 * border)
        print(image_size)
        pic_url = 'https://i.loli.net/2018/11/02/5bdc579114633.jpg'
        buf = urlopen(pic_url).read()
        # sbuf = StringIO(buf)
        # print(type(sbuf))
        file = './tou.png'
        bmp = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bmp = bmp.ConvertToImage().Scale(*image_size)
        # img = wx.Image('D:\我的资料库\Pictures\滑稽.jpg', wx.BITMAP_TYPE_ANY)
        bmp = bmp.ConvertToBitmap()

        success_img = wx.StaticBitmap(self.pnl2, -1, bmp, (border, border),
                                      image_size, style=wx.ALIGN_CENTRE)

        wx.StaticText(self.pnl2, label="URL :", pos=(border, pos_height_line1), size=(title_width, line_height),
                      style=wx.ALIGN_CENTRE)

        self.url_text = wx.TextCtrl(self.pnl2, wx.ID_ANY, wx.EmptyString, pos=(border + title_width, pos_height_line1),
                                    size=(pnl2_width - (2 * border) - (title_width + button_width), line_height))
        self.copy_url = wx.Button(self.pnl2, label='copy', pos=(pnl2_width - button_width, pos_height_line1),
                                  size=(button_width - border, line_height))

        wx.StaticText(self.pnl2, label="Markdowr:", pos=(border, pos_height_line2),
                      size=(title_width, line_height), style=wx.ALIGN_CENTRE)
        self.mark_text = wx.TextCtrl(self.pnl2, wx.ID_ANY, wx.EmptyString, pos=(border + title_width, pos_height_line2),
                                     size=(pnl2_width - (2 * border) - (title_width + button_width), line_height))
        self.copy_make = wx.Button(self.pnl2, label='copy', pos=(pnl2_width - button_width, pos_height_line2),
                                   size=(button_width - border, line_height))

        self.del_item = wx.Button(self.pnl2, label="撤销上传", pos=(
            pnl2_width - (2 * (border + sys_button_width)), pos_height_sys), size=(sys_button_width, line_height))
        self.index_item = wx.Button(self.pnl2, label='返回首页', pos=(
            pnl2_width - ((border + sys_button_width)), pos_height_sys), size=(sys_button_width, line_height))

        self.pnl2.Show()

        self.Bind(wx.EVT_BUTTON, self.OnIndex, self.index_item)

    def makeResultPage2(self):
        '''
        create result page ，
        '''
        border = 5
        pnl2 = wx.Panel(self, -1, size=self.pnl.GetSize())
        # a boxsizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # add a picture
        file = './pic.png'
        bmp = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        img_w, img_h = pnl2.GetSize()
        bmp = bmp.ConvertToImage().Scale(img_w - 2 * border, img_h * 6 / 9).ConvertToBitmap()
        success_img = wx.StaticBitmap(pnl2, 0, bmp)

        vbox.Add(success_img, proportion=6, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=border)

        # add url line
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        url_tit = wx.StaticText(pnl2, 0, label="URL:  ")
        url_text = wx.TextCtrl(pnl2, 0, wx.EmptyString)
        url_copy = wx.Button(pnl2, wx.ID_ANY, label='复制')

        # push to boxsizer
        hbox1.Add(url_tit, 0, wx.ALIGN_LEFT, border=border)
        hbox1.Add(url_text, 1, wx.EXPAND, border=border)
        hbox1.Add(url_copy, 0, wx.ALIGN_RIGHT, border=border)

        # add line 2
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        md_tit = wx.StaticText(pnl2, 0, label="MD:   ")
        md_text = wx.TextCtrl(pnl2, 0, wx.EmptyString)
        md_copy = wx.Button(pnl2, wx.ID_ANY, label='复制')

        hbox2.Add(md_tit, 0, wx.ALIGN_LEFT, border=border)
        hbox2.Add(md_text, 1, wx.EXPAND, border=border)
        hbox2.Add(md_copy, 0, wx.ALIGN_RIGHT, border=border)

        # add line 3
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        index_btn = wx.Button(pnl2, wx.ID_ANY, label='返回首页')
        recall_btn = wx.Button(pnl2, wx.ID_ANY, label='撤回上传')

        hbox3.Add(index_btn, 1, wx.ALL | wx.ALIGN_RIGHT)
        hbox3.Add(recall_btn, 0, wx.ALL | wx.ALIGN_RIGHT)

        vbox.Add(hbox1, proportion=1, flag=wx.TOP | wx.EXPAND, border=border)
        vbox.Add(hbox2, proportion=1, flag=wx.TOP | wx.EXPAND, border=border)
        vbox.Add(hbox3, proportion=1, flag=wx.TOP | wx.EXPAND, border=border)

        pnl2.SetSizerAndFit(vbox)

        # set action
        self.Bind(wx.EVT_BUTTON, self.OnIndex, index_btn)
        self.Bind(wx.EVT_BUTTON, self.OnReCall, recall_btn)
        self.Bind(wx.EVT_BUTTON, self.CopyUrl, url_copy)
        self.Bind(wx.EVT_BUTTON, self.CopyMd, md_copy)

        # turn variables into global
        self.success_img = success_img
        self.url_text = url_text
        self.md_text = md_text
        self.pnl2 = pnl2

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHistory(self, event):
        """Say hello to the user."""
        wx.MessageBox("功能待开发")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("linfree\nBlog：https://fbi.st \nEmail: admin@fbi.st",
                      "关于作者",
                      wx.OK | wx.ICON_INFORMATION)

    def OnSoft(self, event):
        """Display an About Dialog"""
        wx.MessageBox("1.本工具纯属初学练手所做\n2.默认图床使用的http://sm.ms \n3.使用时遇到问题请联系作者",
                      "关于软件",
                      wx.OK | wx.ICON_INFORMATION)

    def OnIndex(self, event):
        self.setLock('index')

    def OnReCall(self, event):
        '''
        recall uploaded picture
        :param event: 
        :return: 
        '''
        if self.result != {}:
            url = self.result['data']['delete']
            result = requests.get(url)
            if result.status_code == 200:
                wx.MessageBox('成功撤回')

    def OnCopyFile(self, event):
        '''
        从剪切板粘贴文件
        :param event: 
        :return: 
        '''
        if self.lock == 'index':
            data = wx.FileDataObject()
            if wx.TheClipboard.Open():
                success = wx.TheClipboard.GetData(data)  # 从剪贴板得到数据
                wx.TheClipboard.Close()
            if success:
                filename = data.GetFilenames()[0]
                res = up_file(url, filename, {})
                self.UpEnd(res, filename)
                # wx.MessageBox('复制')

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        # print(key)
        if key == wx.WXK_ESCAPE and self.lock == 'index':
            ret = wx.MessageBox('确定要退出么?', '提醒',
                                wx.YES_NO | wx.NO_DEFAULT, self)
            if ret == wx.YES:
                self.Close()
        elif key == wx.WXK_ESCAPE and self.lock == 'result':
            # 返回首页
            self.setLock('index')

    def OnChange(self, e):
        pass

    def setLock(self, type=''):
        self.lock = type
        if type == 'result':
            self.pnl.Hide()
            self.pnl2.Show()
        else:
            self.pnl2.Hide()
            self.pnl.Show()
            self.lock = 'index'

    def CopyUrl(self, event):
        value = self.url_text.GetValue()
        self.CopySomething(value)

    def CopyMd(self, event):
        value = self.md_text.GetValue()
        self.CopySomething(value)

    # copy
    def CopySomething(self, text):
        text_obj = wx.TextDataObject()
        wx.TheClipboard.Open()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            text_obj.SetText(text)
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()
            wx.MessageBox('复制成功')

    # Upload result processing
    def UpEnd(self, res, filePath):
        self.result = res
        if res['code'] == 'success':
            url = res['data']['url']
            md = "![%s](%s)" % (os.path.basename(filePath), url)
            self.setLock('result')
            self.url_text.SetValue(url)
            self.md_text.SetValue(md)
            self.ReSetImg(filePath)
        else:
            wx.MessageBox(res['msg'], '上传失败')

    # rewrite page2 image
    def ReSetImg(self, filePath):
        border = 5
        img_w, img_h = self.pnl2.GetSize()
        image = wx.Image(filePath, wx.BITMAP_TYPE_ANY).Rescale(img_w - 2 * border, img_h * 6 / 9).ConvertToBitmap()
        self.success_img.SetBitmap(wx.Bitmap(image))


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MyFrame(None, size=(300, 400), style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    frm.SetIcon(wx.Icon("./app.ico"))
    frm.SetTitle('PIC_UP')
    frm.Show()
    app.MainLoop()
