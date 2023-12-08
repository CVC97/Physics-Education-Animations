from manim import *


# main color of the animation (opposite of the background color)
main_color = WHITE


# class creating a box displaying signal in real and fourier space
class IncomingSignal(Mobject):
    def __init__(self, position, height, width, **kwargs):
        super().__init__(**kwargs)
        rectangle = Rectangle(height = height, width = width, stroke_width = 2, color = main_color).move_to(position)
        separator = Line(start = position - np.array([width/2, 0, 0]), end = position + np.array([width/2, 0, 0]), stroke_width = 1, color = main_color)
        self.add(rectangle, separator)
        text_real_space = Tex(r"Ortsraum", font_size = 24, color = main_color).next_to(separator, 0.5*DOWN + LEFT).shift(height/2 * UP).shift(width * RIGHT)
        text_fourier_space = Tex(r"Frequenzraum", font_size = 24, color = main_color).next_to(separator, 0.5*DOWN + LEFT).shift(width * RIGHT)
        self.add(text_real_space, text_fourier_space)
        # number plane for the untransformed signal
        self.signal_npla = NumberPlane(
            x_range = [-1, 1, 0.1], y_range = [-height / 3.5 * 2.5, height, 1], x_length = 9.5/10*width, y_length = 9/10*height/2,
            x_axis_config = {"stroke_opacity": 0.215, "stroke_color": main_color}, y_axis_config = {"stroke_opacity": 0.125, "stroke_color": main_color}, background_line_style = {"stroke_opacity": 0.125}
        ).move_to(position + np.array([0, height/4, 0]))
        self.add(self.signal_npla)
        # coordinate system for the FT signal
        self.ft_signal_npla = NumberPlane(
            x_range = [128, 512, 32], y_range = [-3, 6, 1], x_length = 9/10*width, y_length = 9/10*height/2,
            x_axis_config = {"stroke_opacity": 0.215, "stroke_color": main_color}, y_axis_config = {"stroke_opacity": 0.125, "stroke_color": main_color}, background_line_style = {"stroke_opacity": 0.125}
        ).move_to(position - np.array([0, height/4, 0]))
        #self.add(self.ft_signal_npla)
        self.ft_signal_nl = NumberLine(
            x_range = [128, 512, 32], length = 9/10*width, include_numbers = True, font_size = 16, stroke_width = 1,
        ).move_to(position - np.array([0, height/4 + height/8 - height/128, 0])).set_color(main_color)
        self.add(self.ft_signal_nl)

    # return untransformed signal
    def get_signal(self, omega_xyc):
        omega_x = omega_xyc[0]
        omega_y = omega_xyc[1]
        omega_c = omega_xyc[2]
        # superposition of the 3 waves
        correction_factor = 8
        def signal_wave(t):
            return (np.cos(omega_x * t / correction_factor) + np.cos(omega_y * t / correction_factor) + np.cos(omega_c * t / correction_factor)) * np.exp(-PI*t**2)
        return self.signal_npla.plot(signal_wave, x_range = [-1, 1], stroke_width = 2, stroke_color = main_color)

    # returns transformed signal
    def get_ft_signal(self, omega_xyc):
        omega_x = omega_xyc[0]
        omega_y = omega_xyc[1]
        omega_c = omega_xyc[2]
        # creates the fourier transform of the given signal
        def ft_signal_wave(omega):
            def get_ft_signal_wave(omega_0):
                return 4*(np.exp(-(omega-omega_0)**2/(4*PI)) + np.exp(-(omega+omega_0)**2/(4*PI)))
            return get_ft_signal_wave(omega_x) + get_ft_signal_wave(omega_y) + get_ft_signal_wave(omega_c)
        # frequencies determined by fourier analysis
        omega_xplot = self.ft_signal_npla.plot(ft_signal_wave, x_range = [128, 256], stroke_width = 2, color = RED)
        omega_yplot = self.ft_signal_npla.plot(ft_signal_wave, x_range = [256, 384], stroke_width = 2, color = BLUE)
        omega_cplot = self.ft_signal_npla.plot(ft_signal_wave, x_range = [384, 512], stroke_width = 2, color = GREY)
        return VGroup(omega_xplot, omega_yplot, omega_cplot)
    

# class for the box of the recreated image, including number lines for x-, and y-coordinate
class FTransformedImage(Mobject):
    def __init__(self, position, size, **kwargs):
        super().__init__(**kwargs)
        self.grid_center = position
        self.grid_sidelength = size
        self.grid_pixels = 128
        self.grid_node_dist = self.grid_sidelength / (self.grid_pixels + 1)
        # x-axis
        self.x_ax = NumberLine(
            x_range = [128, 256, 16], length = self.grid_sidelength, include_numbers = True, font_size = 16
            ).set_color(RED).move_to(position - np.array([0, self.grid_sidelength/2+0.5, 0]))
        # y-axis
        self.y_ax = NumberLine(
            x_range = [256, 384, 16], length = self.grid_sidelength, include_numbers = True, font_size = 16, rotation = PI/2, label_direction = LEFT
            ).set_color(BLUE).move_to(position - np.array([self.grid_sidelength/2+0.5, 0, 0]))
        # square with text
        square = Square(side_length = self.grid_sidelength, stroke_width = 2, stroke_color = main_color, **kwargs).move_to(np.array([self.x_ax.n2p(192)[0], self.y_ax.n2p(320)[1], 0]))
        square_text_head = Tex(r"Originales Bild", font_size = 32, color = main_color).next_to(square, 0.5*UP)
        self.add(self.x_ax, self.y_ax, square)

    # function to create a pixel for a given tupel of frequencies (omega_x, omega_y, omega_c)
    def get_pixel(self, omega_xyc):
        omega_x = omega_xyc[0]
        omega_y = omega_xyc[1]
        omega_c = omega_xyc[2] - 3*128
        nl_node_dist = self.x_ax.n2p(1)[0] - self.x_ax.n2p(0)[0]
        node_position = np.array([self.x_ax.n2p(omega_x)[0] + self.grid_node_dist/2, self.y_ax.n2p(omega_y)[1] + self.grid_node_dist/2, 0])
        white_square = Square(side_length = nl_node_dist, color = WHITE, stroke_width = 0.1, stroke_opacity = 0, fill_opacity = omega_c / 128).move_to(node_position)
        #black_square = Square(side_length = nl_node_dist, color = BLACK, stroke_width = 0.1, stroke_opacity = 0, fill_opacity = (128 - omega_c) / 128).move_to(node_position)
        return white_square

    # creates an object pointing towards the frequency tupel
    def get_pixel_arm(self, omega_xyc):
        omega_x = omega_xyc[0]
        omega_y = omega_xyc[1]
        omega_c = omega_xyc[2]
        x_circle = Circle(radius = 0.05, color = main_color).move_to(self.x_ax.n2p(omega_x+0.5))
        y_circle = Circle(radius = 0.05, color = main_color).move_to(self.y_ax.n2p(omega_y+0.5))
        return VGroup(x_circle, y_circle)


# class facilitating the fullscreen superposition of waves
class FullSignal(Mobject):
    def __init__(self, position, **kwargs):
        super().__init__(**kwargs)
        # hidden number plane for the fulls signal displayed at the entire screen
        self.full_signal_npla = NumberPlane(
            x_range = [-1, 1, 0.1], y_range = [-4, 4, 1], x_length = 12, y_length = 8,
            x_axis_config = {"stroke_opacity": 0.215}, y_axis_config = {"stroke_opacity": 0.125}, background_line_style = {"stroke_opacity": 0.125}
        ).move_to(position)
        # baseline for amplitude zero
        line = Line(start = np.array([-10, 0, 0]), end = np.array([10, 0, 0]), stroke_width = 1, stroke_color = main_color).move_to(self.full_signal_npla.c2p(0, 0, 0))
        self.add(line)
        #self.add(self.full_signal_npla)

    # return the superposition of all three waves
    def get_wave(self, omega_xyc, amplitude, wave_opacity):
        omega_x = omega_xyc[0]
        omega_y = omega_xyc[1]
        omega_c = omega_xyc[2]
        # superposition of the 3 waves
        correction_factor = 8
        def signal_wave(t):
            return amplitude * (np.cos(omega_x * t / correction_factor) + np.cos(omega_y * t / correction_factor) + np.cos(omega_c * t / correction_factor)) * np.exp(-PI*t**2)
        return self.full_signal_npla.plot(signal_wave, x_range = [-1.5, 1.5], stroke_width = 2, stroke_color = main_color, stroke_opacity = wave_opacity)
    

class SplitSignal(Mobject):
    def __init__(self, position, height, width, description, color, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        rectangle = Rectangle(height = height, width = width, stroke_width = 2, color = main_color).move_to(position)
        self.add(rectangle)
        description_text = Tex(f"{description}", font_size = 32, color = self.color).next_to(rectangle, 0.5*RIGHT + 0.5*UP).shift(width*LEFT)
        self.add(description_text)
        # number plane for the individual sinal waves
        self.split_signal_npla = NumberPlane(
            x_range = [-1, 1, 0.1], y_range = [-1.25, 1.25, 1], x_length = 9.5/10*width, y_length = 9/10*height,
            x_axis_config = {"stroke_opacity": 0.215, "stroke_color": main_color}, y_axis_config = {"stroke_opacity": 0.125, "stroke_color": main_color}, background_line_style = {"stroke_opacity": 0.125}
        ).move_to(position)
        self.add(self.split_signal_npla)

    # return untransformed signal
    def get_wave(self, omega):
        correction_factor = 8
        return self.split_signal_npla.plot(lambda t: np.cos(omega * t / correction_factor) * np.exp(-PI*t**2), x_range = [-1, 1], stroke_width = 2, stroke_color = self.color)