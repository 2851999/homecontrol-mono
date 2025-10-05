from pydantic import BaseModel

from homecontrol_controller.devices.hue.api.schemas import XYGet, XYPut


class HueColour(BaseModel):
    r: float
    g: float
    b: float

    def to_xy(self) -> XYPut:
        """See https://developers.meethue.com/develop/application-design-guidance/color-conversion-formulas-rgb-to-xy-and-back/#xy-to-rgb-color"""
        red = pow((self.r + 0.055) / (1.0 + 0.055), 2.4) if (self.r > 0.04045) else (self.r / 12.92)
        green = pow((self.g + 0.055) / (1.0 + 0.055), 2.4) if (self.g > 0.04045) else (self.g / 12.92)
        blue = pow((self.b + 0.055) / (1.0 + 0.055), 2.4) if (self.b > 0.04045) else (self.b / 12.92)

        X = red * 0.4124 + green * 0.3576 + blue * 0.1805
        Y = red * 0.2126 + green * 0.7152 + blue * 0.0722
        Z = red * 0.0193 + green * 0.1192 + blue * 0.9505

        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        # brightness = Y

        # TODO: Check against capabilities of given light and select closest - see above link (xy to RGB)

        return XYPut(x=x, y=y)

    @staticmethod
    def from_xy(xy: XYGet):
        """See https://developers.meethue.com/develop/application-design-guidance/color-conversion-formulas-rgb-to-xy-and-back/#xy-to-rgb-color"""

        z = 1.0 - xy.x - xy.y
        Y = 1  # Y = brightness
        X = (Y / xy.y) * xy.x
        Z = (Y / xy.y) * z

        r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
        b = X * 0.051713 - Y * 0.121364 + Z * 1.011530

        r = 12.92 * r if r <= 0.0031308 else (1.0 + 0.055) * r ** (1.0 / 2.4) - 0.055
        g = 12.92 * g if g <= 0.0031308 else (1.0 + 0.055) * g ** (1.0 / 2.4) - 0.055
        b = 12.92 * b if b <= 0.0031308 else (1.0 + 0.055) * b ** (1.0 / 2.4) - 0.055

        maxValue = max(r, g, b)
        r /= maxValue
        g /= maxValue
        b /= maxValue

        return HueColour(r=r, g=g, b=b)
