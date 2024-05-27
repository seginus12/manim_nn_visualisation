from manim import *
import random
from math import tanh
from pprint import pprint


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


    def create_input_values(self):
        input_values = [random.uniform(0, 1) for _ in range(INPUT_NEURONS + 1)]
        self.input_values = input_values
        return input_values
    
    
    def create_node_labels(self, layer: VGroup, values):
        labels = VGroup(*[Text(str(round(value, 2)), font_size=14) for value in values])
        for input_node, label in zip(layer[0], labels):
            label.move_to(input_node)
        layer.add(labels)
        return labels
    

    def create_connection_weights(self, network):
        weights = []
        for layer in range(len(network) - 1):
            weights.append([[random.uniform(0, 1) for _ in range(len(self.network[layer+1][0]))] for _ in range(len(self.network[layer][0]))])
        return weights

    
    def create_connection_labels(self, all_connections, weights):
        weights_labels_group = VGroup()

        for layer in range(len(all_connections)):
            weights_layer_group = VGroup()
            for prev in range(len(self.network[layer][0])):
                weights_node_group = VGroup()
                for next_ in range(len(self.network[layer+1][0])):
                    if hasattr(self.network[layer+1][0][next_], 'is_bias_node'):
                        continue
                    weight_label = Text(str(round(weights[layer][prev][next_], 2)), font_size=12)
                    middle_of_line = (all_connections[layer][prev][next_].get_start() + all_connections[layer][prev][next_].get_end()) / 2
                    label_position = (all_connections[layer][prev][next_].get_start() + middle_of_line) / 2
                    weight_label.move_to(label_position)
                    weights_node_group.add(weight_label)
                weights_layer_group.add(weights_node_group)
            weights_labels_group.add(weights_layer_group)

        return weights_labels_group


    def add_multiplication_to_weights(self, prev_layer, next_layer, connections, weights, values):
        labels_group = VGroup()
        for prev in range(len(prev_layer)):
            node_group = VGroup()
            for next_ in range(len(next_layer)):
                if hasattr(next_layer[next_], 'is_bias_node'):
                    continue
                string_value = str(round(weights[prev][next_], 2)) + f"*{round(values[prev], 2)}"
                weight_label = Text(string_value, font_size=12)
                middle_of_line = (connections[prev][next_].get_start() + connections[prev][next_].get_end()) / 2
                label_position = (connections[prev][next_].get_start() + middle_of_line) / 2
                weight_label.move_to(label_position)
                node_group.add(weight_label)
            labels_group.add(node_group)
        return labels_group


    def multiply_weights(self, prev_layer, next_layer, connections, weights, values):
        labels_group = VGroup()
        for prev in range(len(prev_layer)):
            node_group = VGroup()
            for next_ in range(len(next_layer)):
                if hasattr(next_layer[next_], 'is_bias_node'):
                    continue
                string_value = str(round(weights[prev][next_] * values[prev], 2))
                weight_label = Text(string_value, font_size=12)
                middle_of_line = (connections[prev][next_].get_start() + connections[prev][next_].get_end()) / 2
                label_position = (connections[prev][next_].get_start() + middle_of_line) / 2
                weight_label.move_to(label_position)
                node_group.add(weight_label)
            labels_group.add(node_group)
        return labels_group


    def move_multiplication_to_nodes(self, multiplications, prev_layer, next_layer):
        print(multiplications)
        # print(next_layer)
        for prev in range(len(prev_layer)):
            
            for next_ in range(len(next_layer)):
                if hasattr(next_layer[next_], 'is_bias_node'):
                    continue
                print(prev, next_)
                self.play(multiplications[prev][next_].animate.move_to(next_layer[next_]), runtime=0.1)
                self.play(multiplications[prev][next_].animate.fade(1), runtime=0.1)

        # for node in range(len(multiplications)):
        #     print(multiplications[node])
        #     for conn in range(len(multiplications[node])):
        #         print(node, conn, multiplications[node], next_layer[node])
        #         self.play(multiplications[conn][node].animate.move_to(next_layer[node]), runtime=0.1)
        #         self.play(multiplications[conn][node].animate.fade(1), runtime=0.1)
            

    def calc_sum(self, weights, prev_layer, next_layer):
        sums = []
        next_layer_len = 0
        for i in range(len(next_layer)):
            if not hasattr(next_layer[i], 'is_bias_node'):
                next_layer_len += 1
        for next_ in range(next_layer_len):
            sum = 0
            for prev in range(len(prev_layer)):
                sum += weights[prev][next_] * prev_layer[prev]
            sums.append(sum)
        return sums


    def create_sum_labels(self, sums, layer):
        layer_len = 0
        for i in range(len(layer)):
            if not hasattr(layer[i], 'is_bias_node'):
                layer_len += 1
        sums_group = VGroup()
        for node in range(layer_len):
            sum_label = Text(str(round(sums[node], 2)), font_size=12)
            sum_label.move_to(layer[node])
            sums_group.add(sum_label)
        return sums_group


    def calc_neuron_activations(self, sums):
        neuron_activations = []
        for sum in sums:
            neuron_activations.append(tanh(sum))
        return neuron_activations
    

    def create_activations_labels(self, neuron_activations, layer):
        layer_len = 0
        for i in range(len(layer)):
            if not hasattr(layer[i], 'is_bias_node'):
                layer_len += 1
        activations_group = VGroup()
        for node in range(layer_len):
            activations_label = Text(str(round(neuron_activations[node], 2)), font_size=12)
            activations_label.move_to(layer[node])
            activations_group.add(activations_label)
        return activations_group
    

    def change_bias_node_label(self, bias_label, bias_value):
        value_label = Text(str(bias_value), font_size=12)
        self.play(FadeOut(bias_label), run_time=0.2)
        value_label.move_to(bias_label)
        self.play(Create(value_label))


    def construct(self):
        layers = self.create_layers()
        self.play(Create(layers, run_time=3))
        input_values = self.create_input_values()
        input_labels = self.create_node_labels(layers[0], input_values)

        self.play(Transform(layers[0][2], input_labels, run_time=1))

        all_connections = self.create_connections()
        self.play(Create(all_connections), run_time=2)
        weights = self.create_connection_weights(self.network)
        connection_labels = self.create_connection_labels(all_connections, weights)
        self.play(Create(connection_labels), run_time=1)
        self.wait(0.5)


        mult_weights = self.add_multiplication_to_weights(self.network[0][0], self.network[1][0], all_connections[0], weights[0], input_values)
        self.play(Transform(connection_labels[0], mult_weights))
        self.wait(0.5)

        mult_weights_result = self.multiply_weights(self.network[0][0], self.network[1][0], all_connections[0], weights[0], input_values)
        self.play(Transform(connection_labels[0], mult_weights_result))

        for node_label in range(len(self.network[1][2])):
            if not hasattr(self.network[1][0][node_label], 'is_bias_node'):
                self.play(FadeOut(self.network[1][2][node_label]), run_time=0.2)
            else:
                bias2 = round(random.uniform(0, 1))
                self.change_bias_node_label(self.network[1][2][node_label], bias2)

        self.move_multiplication_to_nodes(mult_weights_result, self.network[0][0], self.network[1][0])

        sums = self.calc_sum(weights[0], input_values, self.network[1][0])
        sums_labels = self.create_sum_labels(sums, self.network[1][0])
        self.play(Create(sums_labels), runtime=1)
        self.wait(1)
        self.play(FadeOut(sums_labels), runtime=1)

        activations = self.calc_neuron_activations(sums)
        activations_labels = self.create_activations_labels(activations, self.network[1][0])
        self.play(Create(activations_labels), runtime=1)


        activations.append(bias2)
        mult_weights = self.add_multiplication_to_weights(self.network[1][0], self.network[2][0], all_connections[1], weights[1], activations)
        self.play(Transform(connection_labels[1], mult_weights))
        self.wait(0.5)

        mult_weights_result = self.multiply_weights(self.network[1][0], self.network[2][0], all_connections[1], weights[1], activations)
        self.play(Transform(connection_labels[1], mult_weights_result))

        for node_label in range(len(self.network[2][2])):
            if not hasattr(self.network[2][0][node_label], 'is_bias_node'):
                self.play(FadeOut(self.network[2][2][node_label]), run_time=0.2)
            else:
                bias3 = round(random.uniform(0, 1), 2)
                self.change_bias_node_label(self.network[2][2][node_label], bias3)

        self.move_multiplication_to_nodes(mult_weights_result, self.network[1][0], self.network[2][0])

        sums = self.calc_sum(weights[1], activations, self.network[2][0])
        sums_labels = self.create_sum_labels(sums, self.network[2][0])
        self.play(Create(sums_labels), runtime=1)
        self.wait(1)
        self.play(FadeOut(sums_labels), runtime=1)

        activations = self.calc_neuron_activations(sums)
        activations_labels = self.create_activations_labels(activations, self.network[2][0])
        self.play(Create(activations_labels), runtime=1)


        activations.append(bias3)
        mult_weights = self.add_multiplication_to_weights(self.network[2][0], self.network[3][0], all_connections[2], weights[2], activations)
        self.play(Transform(connection_labels[2], mult_weights))
        self.wait(0.5)

        mult_weights_result = self.multiply_weights(self.network[2][0], self.network[3][0], all_connections[2], weights[2], activations)
        self.play(Transform(connection_labels[2], mult_weights_result))

        for node_label in range(len(self.network[3][2])):
            if not hasattr(self.network[3][0][node_label], 'is_bias_node'):
                self.play(FadeOut(self.network[3][2][node_label]), run_time=0.2)
            else:
                bias3 = round(random.uniform(0, 1), 2)
                self.change_bias_node_label(self.network[3][2][node_label], bias3)

        self.move_multiplication_to_nodes(mult_weights_result, self.network[2][0], self.network[3][0])

        sums = self.calc_sum(weights[2], activations, self.network[3][0])
        sums_labels = self.create_sum_labels(sums, self.network[3][0])
        self.play(Create(sums_labels), runtime=1)
        self.wait(1)
        self.play(FadeOut(sums_labels), runtime=1)

        activations = self.calc_neuron_activations(sums)
        activations_labels = self.create_activations_labels(activations, self.network[3][0])
        self.play(Create(activations_labels), runtime=1)


        self.wait(1)

