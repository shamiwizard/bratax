from pathlib import Path

from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode.geometry import Vector
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.formulas import linear_map


class CustomInterface(interfaces.Gcode):

    # Override the laser_off method such that it also powers off the fan.
    def laser_off(self):
        return "M5;"  # Turn off the fan + turn off the laser

    # Override the set_laser_power method
    def set_laser_power(self, power):
        return f"M3 S{linear_map(0, 1000, power)};"  # Turn on the fan + change laser power

    def set_origin_at_position(self):
        self.position = Vector(0, 0)
        return "G90 X0 Y0 F1000;"

def generate_gcode(image, movement_speed=1000, cutting_speed=300, pass_depth=0):  # Дифолті налаштування
    gcode_compiler = Compiler(
        CustomInterface,
        movement_speed=movement_speed,
        cutting_speed=cutting_speed,
        pass_depth=pass_depth
    )
    image_path = Path(image).resolve()
    curves = parse_file(image_path)
    gcode_compiler.append_curves(curves)
    gcode_compiler.compile_to_file('test.gco')


if __name__ == '__main__':
    generate_gcode('Logo 1d12.svg')
