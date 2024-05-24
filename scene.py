from manim import *
import random
import copy


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
        all_connections = VGroup()
        for layer, next_layer in zip(self.network, self.network[1:]):
            # all_connections += self.create_connections_between_layers(layer[0], next_layer[0])
            connections = self.create_connections_between_layers(layer[0], next_layer[0])
            all_connections.add(connections)
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
            node_labels = VGroup(*[MathTex(fr"x_{i}", font_size=24) for i in range(num_nodes)])
            if include_bias:
                bias_label = MathTex(fr"b_i", font_size=24)
                node_labels.add(bias_label)
        elif layer_type == 'hidden':
            label = Text(
                f'Hidden layer {layer_idx+1}',
                font_size=14,
                stroke_width=1
                )
            node_labels = VGroup(*[MathTex(fr"a_{i}^{{({layer_idx})}}", font_size=24) for i in range(num_nodes)])
            if include_bias:
                bias_label = MathTex(fr"b^{{({layer_idx})}}", font_size=24)
                node_labels.add(bias_label)
        elif layer_type == 'output':
            label = Text(
                'Output layer',
                font_size=14,
                stroke_width=1
                )
            node_labels = VGroup(*[MathTex(fr"y_{i}", font_size=24) for i in range(num_nodes)])
            
        layer_nodes.arrange(DOWN, buff=node_buffer)
        label.next_to(layer, UP, buff=node_buffer / 2)
        layer.add(label)
        
        for label, node in zip(node_labels, layer_nodes):
            label.move_to(node)
        layer.add(node_labels)

        return layer


    def create_connections_between_layers(self, source_layer:VGroup, target_layer: VGroup, arrow_width=1):
        connections = VGroup() 

        for j, node in enumerate(source_layer):
            node_connections = VGroup()
            for i, target_node in enumerate(target_layer):
                if hasattr(target_node,'is_bias_node'):
                    continue
                arrow = Line(
                    start=source_layer[j].get_right(), 
                    end=target_layer[i].get_left(),
                )
                arrow.stroke_width = 0.5
                arrow.add_tip(
                    tip_length=0.15, 
                    tip_width=0.15)
                node_connections.add(arrow)
            connections.add(node_connections)

        return connections


    # def create_node_labels(self, network: VGroup):
    #     input_labels = VGroup(*[MathTex(fr"x_{i}", font_size=24) for i in range(num_nodes)])
    #     if include_bias:
    #         bias_label = MathTex(fr"b_i", font_size=24)
    #         node_labels.add(bias_label)
    #             elif layer_type == 'hidden':
    #                 label = Text(
    #                     f'Hidden layer {layer_idx+1}',
    #                     font_size=14,
    #                     stroke_width=1
    #                     )
    #                 node_labels = VGroup(*[MathTex(fr"a_{i}^{{({layer_idx})}}", font_size=24) for i in range(num_nodes)])
    #                 if include_bias:
    #                     bias_label = MathTex(fr"b^{{({layer_idx})}}", font_size=24)
    #                     node_labels.add(bias_label)
    #             elif layer_type == 'output':
    #                 label = Text(
    #                     'Output layer',
    #                     font_size=14,
    #                     stroke_width=1
    #                     )
    #                 node_labels = VGroup(*[MathTex(fr"y_{i}", font_size=24) for i in range(num_nodes)])
                    
    #             layer_nodes.arrange(DOWN, buff=node_buffer)
    #             label.next_to(layer, UP, buff=node_buffer / 2)
    #             layer.add(label)
                
    #             for label, node in zip(node_labels, layer_nodes):
    #                 label.move_to(node)
    #             layer.add(node_labels)



    def create_input_values_labels(self, input_layer: VGroup):
        input_values = [random.uniform(0, 1) for _ in range(len(input_layer))]
        self.input_values = input_values
        input_labels = VGroup(*[Text(str(round(value, 2)), font_size=14) for value in input_values])
        for input_node, label in zip(input_layer[0], input_labels):
            label.move_to(input_node)
        input_layer.add(input_labels)
        return input_labels
    
    def create_connection_weights(self, all_connections):
        weights = []
        weights_labels = VGroup()

        input_weights = [[random.uniform(0, 1) for _ in range(len(self.network[1][0]))] for _ in range(len(self.network[0][0]))]
        self.input_weights = input_weights 
        input_weights_grpoup = VGroup()
        for prev in range(len(self.network[0][0])):
            node_weight_group = VGroup()
            for next_ in range(len(self.network[1][0])):
                if hasattr(self.network[1][0][next_], 'is_bias_node'):
                    continue
                weight_label = Text(str(round(input_weights[prev][next_], 2)), font_size=12)
                middle_of_line = (all_connections[0][prev][next_].get_start() + all_connections[0][prev][next_].get_end()) / 2
                label_position = (all_connections[0][prev][next_].get_start() + middle_of_line) / 2
                weight_label.move_to(label_position)
                node_weight_group.add(weight_label)
            input_weights_grpoup.add(node_weight_group)
        weights.append(input_weights)
        weights_labels.add(input_weights_grpoup)
        return weights_labels


        hidden_weights = []
        for layer in range(1, HIDDEN_LAYERS):
            for prev in range(len(self.network[prev][0])):
                for next_ in range(len(self.network[next_][0])):
                    hidden_weights[layer][prev][next_] = random.uniform(0, 1)
            # hidden_weights = [[random.uniform(0, 1) for _ in range(len(self.network[i][0]))] for _ in range(len(self.network[i][0]))]
        weights.append(hidden_weights)

        output_weights = []
        for prev in range(len(self.network[-2][0])):
            for next_ in range(len(self.network[-1][0])):
                output_weights[prev][next_] = random.uniform(0, 1)
        # output_weights = [[random.uniform(0, 1) for _ in range(len(self.network[-2][0]))] for _ in range(len(self.network[-1][0]))]
        weights.append(output_weights)
        self.weights = weights


    def add_multiplication_to_weights(self, prev_layer, next_layer, connections):
        labels_group = VGroup()
        for prev in range(len(prev_layer)):
            node_group = VGroup()
            for next_ in range(len(next_layer)):
                if hasattr(next_layer[next_], 'is_bias_node'):
                    continue
                string_value = str(round(self.input_weights[prev][next_], 2)) + f"*{round(self.input_values[prev], 2)}"
                weight_label = Text(string_value, font_size=12)
                middle_of_line = (connections[prev][next_].get_start() + connections[prev][next_].get_end()) / 2
                label_position = (connections[prev][next_].get_start() + middle_of_line) / 2
                weight_label.move_to(label_position)
                node_group.add(weight_label)
            labels_group.add(node_group)
        return labels_group


    def multiply_weights(self, prev_layer, next_layer, connections):
        labels_group = VGroup()
        for prev in range(len(prev_layer)):
            node_group = VGroup()
            for next_ in range(len(next_layer)):
                if hasattr(next_layer[next_], 'is_bias_node'):
                    continue
                string_value = str(round(self.input_weights[prev][next_] * self.input_values[prev], 2))
                weight_label = Text(string_value, font_size=12)
                middle_of_line = (connections[prev][next_].get_start() + connections[prev][next_].get_end()) / 2
                label_position = (connections[prev][next_].get_start() + middle_of_line) / 2
                weight_label.move_to(label_position)
                node_group.add(weight_label)
            labels_group.add(node_group)
        return labels_group


    def move_multiplication_to_nodes(self, multiplications, prev_layer, next_layer):
        for prev in range(len(prev_layer)):
            for next_ in range(len(next_layer)):
                # multiplications[]
                pass



    def construct(self):
        layers = self.create_layers()
        self.play(Create(layers, run_time=3))
        input_labels = self.create_input_values_labels(layers[0])

        # layers[0][2].save_state()
        # input_labels.save_state()
        # self.play(Transform(layers[0][2], input_labels, run_time=1))
        # self.play(FadeOut(input_labels, run_time=0.4))
        # self.play(Restore(layers[0][2], run_time=1))

        all_connections = self.create_connections()
        # for connection in all_connections:
        self.play(Create(all_connections), run_time=2)
        weights = self.create_connection_weights(all_connections)
        print(weights[0])
        self.play(Create(weights[0]), run_time=1)
        self.wait(0.5)

        mult_weights = self.add_multiplication_to_weights(self.network[0][0], self.network[1][0], all_connections[0])
        self.play(Transform(weights[0], mult_weights))
        self.wait(0.5)

        sum_weights = self.multiply_weights(self.network[0][0], self.network[1][0], all_connections[0])
        self.play(Transform(weights[0], sum_weights))
        # self.play(Transform(self.multiply_weights_labels(weights[0], self.input_values), weights[0]), run_time=1)






        # self.play(input_layer.animate.shift(LEFT * _shift_val))    
        # self.wait(0.5)
 
        # self.play(*[Create(item, run_time=_run_time) for item in hidden_layer]) 
        # self.wait(0.5) 
 
        # output_layer.shift(RIGHT * _shift_val).shift(UP * 0.75) 
        # self.play(*[Create(item, run_time=_run_time) for item in output_layer])    
        self.wait(1)
