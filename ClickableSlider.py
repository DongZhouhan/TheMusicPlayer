
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # 调用父类的事件处理以保持滑块拖动功能
        try:
            if event.button() == Qt.LeftButton:  # 仅在左键点击时处理
                val = self.pixelPosToRangeValue(event.pos())
                self.setValue(int(val))
                self.sliderReleased.emit()

        except Exception as e:
            print(f"mousePressEvent: {e}")

    def pixelPosToRangeValue(self, pos):
        # 计算点击的像素位置对应的滑块值
        if self.orientation() == Qt.Horizontal:
            valueRange = self.maximum() - self.minimum()
            sliderLength = self.width()
            clickPos = pos.x()
        else:  # 垂直滑块的情况
            valueRange = self.maximum() - self.minimum()
            sliderLength = self.height()
            clickPos = pos.y()
        # 将点击位置转换为滑块的值
        value = self.minimum() + (clickPos / sliderLength) * valueRange
        return value
