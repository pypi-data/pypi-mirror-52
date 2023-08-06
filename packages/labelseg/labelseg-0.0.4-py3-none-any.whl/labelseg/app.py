import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QFileDialog, QMessageBox, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QColor
from labelseg.mainwindow import Ui_MainWindow
import cv2 as cv
from enum import Enum
import os
from pathlib import Path
import labelseg.util as util
from PyQt5.Qt import QMouseEvent
from labelseg.app_dialog import PixelRangeDialog
import logging
import numpy as np


class OPEN_MODE(Enum):
    OPEN_FILE = 1
    OPEN_DIR = 2


class STATE(Enum):
    NORMAL = 1
    DRAW_POLYGON = 2
    DRAW_RECTANGLE = 3
    DRAW_ELLIPSE = 4


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.img_area.setScaledContents(False)
        self.ui.img_area.setStyleSheet('border: 1px solid red')
        self.add_tool_bar()
        self.bind_actions()
        self.init_vars()

    def init_vars(self):
        self.open_mode = OPEN_MODE.OPEN_FILE
        self.opened_files = []
        self.cur_img = None
        self.panel_pic = None  # 用来在上面绘制矩阵等形状
        self.origin_img = None  # 保留原始大小的图片
        self.labelimg = None
        self.scale = 1
        self.cur_rect_list = []
        self.cur_label_list = []
        self.histroty = []
        self.fill_color = QColor('green')
        self.pixel_range = [-5, 5]
        self.state = STATE.NORMAL
        self.start_point = None
        self.end_point = None
        self.polygon_points = None
        self.ellipse_points = None
        self.modified = False
        self.saved = False

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s %(funcName)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def refresh_vars(self):
        self.cur_img = None
        self.panel_pic = None  # 用来在上面绘制矩阵等形状
        self.origin_img = None  # 保留原始大小的图片
        self.labelimg = None
        self.scale = 1
        self.cur_rect_list = []
        self.cur_label_list = []
        self.histroty = []
        self.state = STATE.NORMAL
        self.ui.actionRectangle.setChecked(False)
        self.ui.actionPolygon.setChecked(False)
        self.ui.actionEllipse.setChecked(False)
        self.start_point = None
        self.end_point = None
        self.polygon_points = None
        self.ellipse_points = None
        self.modified = False
        self.saved = False

    def bind_actions(self):
        self.ui.actionOpen_File.triggered.connect(self.open_file)
        self.ui.actionOpen_Dir.triggered.connect(self.open_dir)
        self.ui.file_list.itemClicked.connect(self.file_list_item_changed)
        self.ui.actionZoom_In.triggered.connect(self.zoom_in_pic)
        self.ui.actionZoom_Out.triggered.connect(self.zoom_out_pic)
        self.ui.img_area.mouse_pressed.connect(self.mouse_pressed)
        self.ui.img_area.mouse_move.connect(self.mouse_move)
        self.ui.img_area.mouse_release.connect(self.mouse_release)
        self.ui.actionfill_color.triggered.connect(self.set_fill_color)
        self.ui.actionSet_Pixel_Range.triggered.connect(self.set_pixel_range)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionPolygon.triggered.connect(self.create_polygon)
        self.ui.actionRectangle.triggered.connect(self.create_rectangle)
        self.ui.actionEllipse.triggered.connect(self.create_ellipse)

    def save(self):
        name = str(self.selected_filename.absolute())
        items = name.split('.')
        output_filename = '.'.join(items[:-1]) + '.npy'
        np.save(output_filename, self.labelimg)
        self.saved = True
        self.modified = False

    def undo(self, checked):
        if self.state == STATE.DRAW_POLYGON and self.polygon_points is not None and self.polygon_points[
                'finish'] is False:
            if len(self.polygon_points['points']) == 1:
                self.polygon_points = None
            elif len(self.polygon_points['points']) > 1:
                self.polygon_points['points'].pop(-1)
                self.draw_lines(self.polygon_points['points'], False)
                if self.labelimg is not None:
                    pic = self.draw_points()
                    self.show_pic(file_name=None, content=pic)
                else:
                    self.show_pic(file_name=None, content=self.panel_pic)
        else:
            if len(self.histroty) == 0:
                return
            x, y = self.histroty.pop(-1)
            self.labelimg[x, y] = 0
            pic = self.draw_points()
            self.show_pic(file_name=None, content=pic)
            self.modified = True

    def set_fill_color(self, checked):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color

    def set_pixel_range(self, checked):
        dialog = PixelRangeDialog()
        if dialog.exec_():
            v1, v2 = dialog.get_result()
            self.pixel_range = [v1, v2]
            self.logger.debug(self.pixel_range)

    def create_polygon(self, checked):
        if checked:
            self.state = STATE.DRAW_POLYGON
            self.ui.actionEllipse.setChecked(False)
            self.ui.actionRectangle.setChecked(False)
        else:
            self.state = STATE.NORMAL

    def create_rectangle(self, checked):
        if checked:
            self.state = STATE.DRAW_RECTANGLE
            self.ui.actionEllipse.setChecked(False)
            self.ui.actionPolygon.setChecked(False)
        else:
            self.state = STATE.NORMAL

    def create_ellipse(self, checked):
        if checked:
            self.state = STATE.DRAW_ELLIPSE
            self.ui.actionPolygon.setChecked(False)
            self.ui.actionRectangle.setChecked(False)
        else:
            self.state = STATE.NORMAL

    def pos_in_img_area(self, pos: PyQt5.QtCore.QPoint):
        if self.cur_img is None:
            return False, None
        width = self.ui.img_area.width()
        height = self.ui.img_area.height()
        img_height, img_width, _ = self.cur_img.shape
        w = (width - img_width) // 2
        h = (height - img_height) // 2
        x_valid = w <= pos.x() <= w + img_width
        y_valid = h <= pos.y() <= h + img_height
        valid = x_valid and y_valid
        if valid:
            return True, (pos.x() - w, pos.y() - h)
        else:
            return False, None

    def mouse_pressed(self, ev: QMouseEvent):
        if self.state == STATE.NORMAL:
            return
        if ev.button() == Qt.LeftButton:
            pos = ev.pos()
            valid, relative_pos = self.pos_in_img_area(pos)
            self.logger.debug(valid)
            if valid:
                self.logger.debug(relative_pos)
                point = (
                    int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
                if self.state == STATE.DRAW_RECTANGLE:
                    self.start_point = point
                    self.end_point = None
                    self.logger.debug(self.start_point)
                elif self.state == STATE.DRAW_POLYGON:
                    if self.polygon_points is None or self.polygon_points['finish'] is True:
                        self.polygon_points = {
                            'finish': False, 'points': [point]}
                    else:
                        p1 = np.array(
                            [
                                self.polygon_points['points'][0][0] *
                                self.scale,
                                self.polygon_points['points'][0][1] *
                                self.scale])
                        p2 = np.array(
                            [point[0] * self.scale, point[1] * self.scale])
                        dis = np.linalg.norm(p1 - p2, 2)
                        if dis < 10:
                            self.polygon_points['finish'] = True
                            self.draw_lines(
                                self.polygon_points['points'], True)
                        else:
                            self.polygon_points['points'].append(point)
                            self.draw_lines(
                                self.polygon_points['points'], False)
                        if self.labelimg is not None:
                            pic = self.draw_points()
                            self.show_pic(file_name=None, content=pic)
                        else:
                            self.show_pic(
                                file_name=None, content=self.panel_pic)
                elif self.state == STATE.DRAW_ELLIPSE:
                    if self.ellipse_points is None:
                        self.ellipse_points = {'points': [point], 'info': None}
                    elif len(self.ellipse_points['points']) == 1:
                        self.ellipse_points['points'].append(point)
                        self.draw_lines(self.ellipse_points['points'], False)
                        if self.labelimg is not None:
                            pic = self.draw_points()
                            self.show_pic(file_name=None, content=pic)
                        else:
                            self.show_pic(
                                file_name=None, content=self.panel_pic)
                    elif len(self.ellipse_points['points']) == 2:
                        self.ellipse_points['points'].append(point)
                        self.ellipse_points['info'] = self.draw_ellipse(
                            self.ellipse_points['points'])
                        if self.labelimg is not None:
                            pic = self.draw_points()
                            self.show_pic(file_name=None, content=pic)
                        else:
                            self.show_pic(
                                file_name=None, content=self.panel_pic)
                    else:
                        self.ellipse_points = {'points': [point], 'info': None}
                else:
                    raise NotImplementedError()
        elif ev.button() == Qt.RightButton:
            pass

    def mouse_move(self, ev: QMouseEvent):
        if self.state == STATE.NORMAL:
            return
        pos = ev.pos()
        valid, relative_pos = self.pos_in_img_area(pos)
        if valid:
            relative_pos = (
                int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
            if self.state == STATE.DRAW_RECTANGLE:
                self.draw_rect(self.start_point, relative_pos)
                if self.labelimg is not None:
                    pic = self.draw_points()
                    self.show_pic(file_name=None, content=pic)
                else:
                    self.show_pic(file_name=None, content=self.panel_pic)
            elif self.state == STATE.DRAW_POLYGON:
                pass
            elif self.state == STATE.DRAW_ELLIPSE:
                pass
            else:
                raise NotImplementedError()

    def draw_ellipse(self, points):
        color_r, color_g, color_b = self.fill_color.red(
        ), self.fill_color.green(), self.fill_color.blue()
        points = list(map(lambda item: (
            int(item[0] * self.scale), int(item[1] * self.scale)), points))
        p1 = np.array(points[0])
        p2 = np.array(points[1])
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        p3 = np.array(points[2])
        center = tuple((p1 + p2) // 2)
        r1 = int(np.linalg.norm(p1 - p2, 2) / 2)
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = p2[0] * p1[1] - p1[0] * p2[1]
        r2 = int(np.abs(a * p3[0] + b * p3[1] + c) / np.sqrt(a ** 2 + b ** 2))
        if r1 > r2:
            theta = -1 * (np.arctan(a / b) * 180) / np.pi
            self.panel_pic = cv.ellipse(self.cur_img.copy(
            ), center, (r1, r2), theta, 0, 360, (color_r, color_g, color_b), 1)
            return ((int(center[0] / self.scale), int(center[1] / self.scale)), (int(r1 / self.scale), int(r2 / self.scale)), theta)
        else:
            theta = (np.arctan(a / b) * 180) / np.pi
            if theta > 0:
                theta = 90 - theta
            else:
                theta = -90 - theta
            self.panel_pic = cv.ellipse(self.cur_img.copy(), center, (r2, r1), theta, 0, 360,
                                        (color_r, color_g, color_b), 1)
            return ((int(center[0] / self.scale), int(center[1] / self.scale)), (int(r2 / self.scale), int(r1 / self.scale)), theta)

    def draw_lines(self, points, end=False):
        b, g, r = self.fill_color.blue(), self.fill_color.green(), self.fill_color.red()
        temp_img = self.cur_img.copy()
        points = list(map(lambda item: (
            int(item[0] * self.scale), int(item[1] * self.scale)), points))
        for i in range(len(points) - 1):
            temp_img = cv.line(
                temp_img, points[i], points[i + 1], (r, g, b), 1)
        if end:
            temp_img = cv.line(temp_img, points[-1], points[0], (r, g, b), 1)
        self.panel_pic = temp_img

    def draw_rect(self, start_point, end_point):
        b, g, r = self.fill_color.blue(), self.fill_color.green(), self.fill_color.red()
        self.fill_color.rgb()
        start_point = (int(start_point[0] * self.scale),
                       int(start_point[1] * self.scale))
        end_point = (int(end_point[0] * self.scale),
                     int(end_point[1] * self.scale))
        self.panel_pic = cv.rectangle(
            self.cur_img.copy(), start_point, end_point, (r, g, b), 1)

    def draw_points(self):
        if self.labelimg is None:
            return
        b, g, r = self.fill_color.blue(), self.fill_color.green(), self.fill_color.red()
        x, y = np.where(self.labelimg == 1)
        temp = self.panel_pic.copy()
        for i in range(x.shape[0]):
            cv.circle(temp, (int(y[i] * self.scale),
                             int(x[i] * self.scale)), 1, (r, g, b), 1)
        return temp

    def mouse_release(self, ev: QMouseEvent):
        if self.state == STATE.NORMAL:
            return
        if ev.button() == Qt.LeftButton:
            if self.state == STATE.DRAW_RECTANGLE:
                pos = ev.pos()
                valid, relative_pos = self.pos_in_img_area(pos)
                self.logger.debug(valid)
                if valid:
                    self.logger.debug(relative_pos)
                    self.end_point = (
                        int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
        elif ev.button() == Qt.RightButton:
            if self.state == STATE.NORMAL:
                return
            if self.state == STATE.DRAW_RECTANGLE:
                if self.start_point is None or self.end_point is None:
                    return
                pos = ev.pos()
                valid, relative_pos = self.pos_in_img_area(pos)
                if valid:
                    click_pos = (
                        int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
                    min_x, max_x = min(
                        self.start_point[0], self.end_point[0]), max(
                        self.start_point[0], self.end_point[0])
                    min_y, max_y = min(
                        self.start_point[1], self.end_point[1]), max(
                        self.start_point[1], self.end_point[1])
                    self.logger.debug(click_pos)
                    if min_x <= click_pos[0] <= max_x and min_y <= click_pos[1] <= max_y:
                        pixel_value = self.origin_img[click_pos[1],
                                                      click_pos[0], 0]
                        low, high = pixel_value + \
                            self.pixel_range[0], pixel_value + \
                            self.pixel_range[1]
                        selected_area = self.origin_img[min_y: max_y +
                                                        1, min_x: max_x + 1, 0]
                        x, y = np.where((selected_area >= low) *
                                        (selected_area <= high))
                        x = x + min_y
                        y = y + min_x
                        self.labelimg[x, y] = 1
                        pic = self.draw_points()
                        self.show_pic(file_name=None, content=pic)
                        self.histroty.append((x, y))
                        self.modified = True
            elif self.state == STATE.DRAW_POLYGON:
                if self.polygon_points is None or self.polygon_points['finish'] is False:
                    return
                pos = ev.pos()
                valid, relative_pos = self.pos_in_img_area(pos)
                if valid:
                    click_pos = (
                        int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
                    self.logger.debug(click_pos)
                    x_pos = np.array([item[0]
                                      for item in self.polygon_points['points']])
                    y_pos = np.array([item[1]
                                      for item in self.polygon_points['points']])
                    min_x, max_x = x_pos.min(), x_pos.max()
                    min_y, max_y = y_pos.min(), y_pos.max()
                    p = np.array(self.polygon_points['points']).reshape(
                        [1, len(self.polygon_points['points']), 2])
                    p[0, :, 0] -= min_x
                    p[0, :, 1] -= min_y
                    mask = np.zeros(
                        [max_y - min_y + 1, max_x - min_x + 1], np.uint8)
                    mask = cv.fillPoly(mask, p, 1)
                    pixel_value = self.origin_img[click_pos[1],
                                                  click_pos[0], 0]
                    low, high = pixel_value + \
                        self.pixel_range[0], pixel_value + self.pixel_range[1]
                    selected_img = self.origin_img[min_y: max_y +
                                                   1, min_x: max_x + 1, 0]
                    x, y = np.where((selected_img >= low) *
                                    (selected_img <= high) * mask)
                    x = x + min_y
                    y = y + min_x
                    self.labelimg[x, y] = 1
                    pic = self.draw_points()
                    self.show_pic(file_name=None, content=pic)
                    self.histroty.append((x, y))
                    self.modified = True
            elif self.state == STATE.DRAW_ELLIPSE:
                if self.ellipse_points is None or len(
                        self.ellipse_points['points']) < 3 or self.ellipse_points['info'] is None:
                    return
                pos = ev.pos()
                valid, relative_pos = self.pos_in_img_area(pos)
                if valid:
                    click_pos = (
                        int(relative_pos[0] / self.scale), int(relative_pos[1] / self.scale))
                    self.logger.debug(click_pos)
                    center, r, theta = self.ellipse_points['info']
                    theta = int(np.around(theta))
                    p = cv.ellipse2Poly(center, r, theta, 0, 360, 1)
                    num_p = p.shape[0]
                    p = p.reshape((1, num_p, 2))
                    min_x, max_x = np.min(p[0, :, 0]), np.max(p[0, :, 0])
                    min_y, max_y = np.min(p[0, :, 1]), np.max(p[0, :, 1])
                    p[0, :, 0] -= min_x
                    p[0, :, 1] -= min_y
                    mask = np.zeros(
                        (max_y - min_y + 1, max_x - min_x + 1), np.uint8)
                    mask = cv.fillPoly(mask, p, 1)
                    pixel_value = self.origin_img[click_pos[1],
                                                  click_pos[0], 0]
                    low, high = pixel_value + \
                        self.pixel_range[0], pixel_value + self.pixel_range[1]
                    selected_img = self.origin_img[min_y: max_y +
                                                   1, min_x: max_x + 1, 0]
                    x, y = np.where((selected_img >= low) *
                                    (selected_img <= high) * mask)
                    x = x + min_y
                    y = y + min_x
                    self.labelimg[x, y] = 1
                    pic = self.draw_points()
                    self.show_pic(file_name=None, content=pic)
                    self.histroty.append((x, y))
                    self.modified = True
                    self.saved = False

    def zoom_in_pic(self, checked):
        self.zoom_pic(True)

    def zoom_out_pic(self, checked):
        self.zoom_pic(False)

    def zoom_pic(self, zoom_in):
        if self.cur_img is None:
            return
        if zoom_in:
            if self.scale >= 5:
                pass
            elif self.scale < 1:
                self.scale += 0.1
            else:
                self.scale += 1
        else:
            if self.scale == 0:
                pass
            elif self.scale <= 1:
                self.scale -= 0.1
            else:
                self.scale -= 1
        self.logger.debug(self.scale)
        height, width, _ = self.origin_img.shape
        self.cur_img = cv.resize(self.origin_img, (int(
            height * self.scale), int(width * self.scale)), cv.INTER_LINEAR)
        if self.state == STATE.DRAW_RECTANGLE:
            if self.start_point is not None and self.end_point is not None:
                self.draw_rect(self.start_point, self.end_point)
                if self.labelimg is not None:
                    pic = self.draw_points()
                    self.show_pic(content=pic)
                else:
                    self.show_pic(file_name=None, content=self.panel_pic)
        elif self.state == STATE.DRAW_POLYGON:
            if self.polygon_points is not None and self.polygon_points['finish'] is True:
                self.draw_lines(self.polygon_points['points'], True)
                if self.labelimg is not None:
                    pic = self.draw_points()
                    self.show_pic(content=pic)
                else:
                    self.show_pic(file_name=None, content=self.panel_pic)
        elif self.state == STATE.DRAW_ELLIPSE:
            if self.ellipse_points is not None and len(
                    self.ellipse_points['points']) == 3:
                self.draw_ellipse(self.ellipse_points['points'])
                if self.labelimg is not None:
                    pic = self.draw_points()
                    self.show_pic(content=pic)
                else:
                    self.show_pic(file_name=None, content=self.panel_pic)
        elif self.labelimg is not None:
            self.panel_pic = self.cur_img.copy()
            pic = self.draw_points()
            self.show_pic(file_name=None, content=pic)
        else:
            self.show_pic(file_name=None)

    def file_list_item_changed(self, item):
        if self.modified and not self.saved:
            res = QMessageBox.warning(
                self,
                'warning',
                'Changes not saved, do you want to save?',
                QMessageBox.Ok | QMessageBox.No,
                QMessageBox.Ok)
            if res == QMessageBox.Ok:
                self.save()
        base_pic_name = item.text()
        for index, filename in enumerate(self.opened_files):
            if filename.name == base_pic_name:
                selected_filename = filename
                break
        self.selected_filename = selected_filename
        self.refresh_vars()
        self.open(self.selected_filename)

    def add_tool_bar(self):
        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addAction(self.ui.actionOpen_File)
        self.toolbar.addAction(self.ui.actionOpen_Dir)
        self.toolbar.addAction(self.ui.actionSave)
        self.toolbar.addAction(self.ui.actionZoom_In)
        self.toolbar.addAction(self.ui.actionZoom_Out)
        self.toolbar.addAction(self.ui.actionfill_color)
        self.toolbar.addAction(self.ui.actionSet_Pixel_Range)
        self.toolbar.addAction(self.ui.actionRectangle)
        self.toolbar.addAction(self.ui.actionEllipse)
        self.toolbar.addAction(self.ui.actionPolygon)
        self.toolbar.addAction(self.ui.actionUndo)

    def show_pic(self, file_name=None, content=None):
        if file_name is not None:
            file_name = str(file_name.absolute())
            img = cv.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
            assert img is not None
            if len(img.shape) == 2:
                img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            height, width, channel = img.shape
            self.cur_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.origin_img = self.cur_img
            self.labelimg = np.zeros(self.origin_img.shape[:2], dtype=np.int)
            qimg = QImage(
                self.cur_img.data,
                width,
                height,
                width * channel,
                QImage.Format_RGB888)
            self.ui.img_area.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
            self.ui.img_area.setPixmap(QPixmap.fromImage(qimg))
            self.ui.img_area.adjustSize()
        elif content is not None:
            height, width, channel = content.shape
            qimg = QImage(
                content.data,
                width,
                height,
                width * channel,
                QImage.Format_RGB888)
            self.ui.img_area.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
            self.ui.img_area.setPixmap(QPixmap.fromImage(qimg))
            self.ui.img_area.adjustSize()
        else:
            height, width, channel = self.cur_img.shape
            qimg = QImage(
                self.cur_img.data,
                width,
                height,
                width * channel,
                QImage.Format_RGB888)
            self.ui.img_area.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
            self.ui.img_area.setPixmap(QPixmap.fromImage(qimg))
            self.ui.img_area.adjustSize()

    def open_file(self, checked):
        if self.modified and not self.saved:
            res = QMessageBox.warning(
                self,
                'warning',
                'Changes not saved, do you want to save?',
                QMessageBox.Ok | QMessageBox.No,
                QMessageBox.Ok)
            if res == QMessageBox.Ok:
                self.save()
        filename, filetype = QFileDialog.getOpenFileName(
            self, '选取文件', '.', 'PNG Files(*.png);;JPG Files(*.jpg)')
        if filename == '':
            return
        filename = Path(filename)
        self.open_mode = OPEN_MODE.OPEN_FILE
        self.opened_files = [filename]
        self.selected_filename = filename
        self.open(self.selected_filename)
        self.refresh_list()

    def open_dir(self, checked):
        if self.modified and not self.saved:
            res = QMessageBox.warning(
                self,
                'warning',
                'Changes not saved, do you want to save?',
                QMessageBox.Ok | QMessageBox.No,
                QMessageBox.Ok)
            if res == QMessageBox.Ok:
                self.save()
        opened_dir = QFileDialog.getExistingDirectory(self, '打开文件夹', '.')
        if opened_dir == '':
            return
        opened_dir = Path(opened_dir)
        self.open_mode = OPEN_MODE.OPEN_DIR
        self.opened_files = list(opened_dir.iterdir())
        self.opened_files = [
            item for item in self.opened_files if util.is_pic(
                item)]
        if len(self.opened_files) == 0:
            QMessageBox.warning(self, 'warning', 'No image found')
        else:
            self.selected_filename = self.opened_files[0]
            self.open(self.selected_filename)
            self.refresh_list()

    def refresh_list(self):
        self.ui.file_list.clear()
        for file_name in self.opened_files:
            base_name = file_name.name
            self.ui.file_list.addItem(base_name)

    def open(self, filename: Path):
        self.setWindowTitle(filename.name)
        self.show_pic(file_name=filename)
        temp = str(filename).split('.')
        npy_filename = '.'.join(temp[:-1]) + '.npy'
        if os.path.exists(npy_filename):
            self.labelimg = np.load(npy_filename)
            self.panel_pic = self.cur_img.copy()
            pic = self.draw_points()
            self.show_pic(file_name=None, content=pic)


def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
