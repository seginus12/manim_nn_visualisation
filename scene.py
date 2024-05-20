from manim import *


HIDDEN_LAYERS = 2
HIDDEN_LAYERS_NEURONS = 3
INPUT_NEURONS = 2
OUTPUT_NEURONS = 1
NEURON_RADIUS = 0.2
COLORS = {'input': GREEN, 'hidden': YELLOW, 'output': BLUE, 'bias': RED}

class NeuralNetworkVisualisation(Scene):
    def create_layers(self):
        network = VGroup()
        network.add(self.create_layer(
            num_nodes       = INPUT_NEURONS,
            include_bias    = True, 
            layer_type      = 'input', 
            layer_idx       = 0,
        ))
        network.add(*[self.create_layer(
            num_nodes       = HIDDEN_LAYERS_NEURONS,
            include_bias    = True, 
            layer_type      = 'hidden', 
            layer_idx       = i,) for i in range(HIDDEN_LAYERS)])
        network.add(self.create_layer(
            num_nodes       = OUTPUT_NEURONS,
            include_bias    = False, 
            layer_type      = 'output', 
            layer_idx       = 2,
        ))
        network.arrange(RIGHT, buff=1.5)
        self.network = network

        return network


    def create_connections(self):
        all_connections = []
        for layer, next_layer in zip(self.network, self.network[1:]):
            all_connections += self.create_connections_between_layers(layer[0], next_layer[0])
        return all_connections
    

    def create_layer(
        self,
        num_nodes, 
        include_bias    = True, 
        layer_type      = 'hidden', 
        node_buffer     = 0.75, 
        add_node_labels = True,
        font_size       = 30,
        add_layer_label = True,
        layer_font_size = 35,
        layer_idx       = None,
        shape_params:dict = {},
        ):

        layer = VGroup()
        layer_nodes = VGroup(*[Circle(color=COLORS[layer_type], radius=0.3) for _ in range(num_nodes)])
        layer.add(layer_nodes)

        if include_bias:
            bias_node = Circle(color=COLORS['bias'], radius=0.3)
            bias_node.is_bias_node = True
            layer_nodes.add(bias_node)

        if layer_type == 'input':
            label = Text(
                'Input layer',
                font_size=14,
                stroke_width=1
                )
            node_labels = VGroup(*[MathTex(fr"(i_{i})", font_size=16) for i in range(num_nodes)])
        elif layer_type == 'hidden':
            label = Text(
                f'Hidden layer {layer_idx+1}',
                font_size=14,
                stroke_width=1
                )
            node_labels = VGroup(*[MathTex(fr"i_{i}", font_size=16) for i in range(num_nodes)])
        elif layer_type == 'output':
            label = Text(
                'Output layer',
                font_size=14,
                stroke_width=1
                )
            node_labels = VGroup(*[MathTex(fr"i_{i}", font_size=16) for i in range(num_nodes)])
            
        layer_nodes.arrange(DOWN, buff=node_buffer)
        label.next_to(layer, UP, buff=node_buffer / 2)
        layer.add(label)
        
        for label, node in zip(node_labels, layer_nodes):
            label.move_to(node)
        layer.add(node_labels)

        return layer


    def create_connections_between_layers(self, source_layer:VGroup, target_layer:VGroup, arrow_width=1):
        connections = VGroup() 

        for j, node in enumerate(target_layer):
            if hasattr(node,'is_bias_node'):
                continue
            for i, source_node in enumerate(source_layer):
                arrow = Line(
                    source_layer[i].get_right(), 
                    target_layer[j].get_left(),
                )
                arrow.stroke_width = 0.5
                arrow.add_tip(
                    tip_length=0.15, 
                    tip_width=0.15)
                connections.add(arrow)

        return connections

        # neurons = VGroup(*[
        #     Circle(
        #         radius=0.15,
        #         stroke_color=YELLOW,
        #         stroke_width=2,
        #         fill_color=BLACK,
        #         fill_opacity=1,
        #     )
        #     for x in range(3)
        # ])
        return layer

    def construct(self):
        self.play(Create(self.create_layers(), run_time=3))
        all_connections = self.create_connections()
        for connection in all_connections:
            self.play(Create(connection), run_time=0.2)
        # self.play(input_layer.animate.shift(LEFT * _shift_val))    
        # self.wait(0.5)
 
        # self.play(*[Create(item, run_time=_run_time) for item in hidden_layer]) 
        # self.wait(0.5) 
 
        # output_layer.shift(RIGHT * _shift_val).shift(UP * 0.75) 
        # self.play(*[Create(item, run_time=_run_time) for item in output_layer])    
        self.wait(1)
