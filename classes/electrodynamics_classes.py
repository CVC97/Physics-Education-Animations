from manim import *


# main color of the animation (opposite of the background color)
# main_color = BLACK
# red_color = PURE_RED
# blue_color = PURE_BLUE
# grey_color = DARK_GREY

main_color = WHITE
red_color = RED
blue_color = BLUE
grey_color = GREY


class ElectricField(Mobject):
    def __init__(self, center = np.array([0, 0, 0]), list_of_charges = [(1, np.array([0, 0, 0]))], **kwargs):
        super().__init__(**kwargs)
        self.list_of_charges = list_of_charges

        # coordinate system
        x_range = np.array([-10, 10, 1])
        y_range = np.array([-5, 5, 1])
        x_length = 20
        y_length = 20
        self.npla = NumberPlane(
            x_range = x_range, y_range = y_range, x_length = x_length, y_length = y_length,
            x_axis_config = {"stroke_opacity": 0.215, "stroke_color": BLACK}, y_axis_config = {"stroke_opacity": 0.125, "stroke_color": BLACK}, background_line_style = {"stroke_opacity": 0.125}).move_to(center)
        self.add(self.npla)


    # returns list of point charge mobjects
    def get_charge(self, radius = 0.5):
        charge_list = []
        for charge in self.list_of_charges:
            q = charge[0]
            charge_position = charge[1]
            if q > 0:   
                charge_circle = Circle(radius = radius, stroke_opacity = 0, fill_color = red_color, fill_opacity = 0.5).move_to(self.npla.c2p(*charge_position))
                charge_text = MathTex(r"+", color = main_color).move_to(self.npla.c2p(*charge_position))
            elif q < 0:
                charge_circle = Circle(radius = radius, stroke_opacity = 0, fill_color = blue_color, fill_opacity = 0.5).move_to(self.npla.c2p(*charge_position))
                charge_text = MathTex(r"-", color = main_color).move_to(self.npla.c2p(*charge_position))
            single_charge = VGroup(charge_circle, charge_text)  
            single_charge.z_index = 1  
            charge_list.append(single_charge)
        return charge_list
    

    # returns pootential value at 'position'
    def get_potential(self, position):
        x = position[0]
        y = position[1]
        potential = 0
        for charge in self.list_of_charges:
            q = charge[0]
            pos_in_coord = self.npla.c2p(*charge[1])
            x_i = pos_in_coord[0]
            y_i = pos_in_coord[1]
            potential += q / np.sqrt((x-x_i)**2 + (y-y_i)**2)
        return potential

    
    # returns electric vector field 
    def get_efield(self):
        # function defining the vector field for given 'position'
        def field_func(position):
            x = position[0]
            y = position[1]
            field = 0
            for charge in self.list_of_charges:
                q = charge[0]
                pos_in_coord = self.npla.c2p(*charge[1])
                x_i = pos_in_coord[0]
                y_i = pos_in_coord[1]
                field += q / np.sqrt((x-x_i)**2 + (y-y_i)**2)**3 * ((x-x_i)*RIGHT + (y-y_i)*UP)
            return field
        return ArrowVectorField(field_func)