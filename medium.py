from manim import *

class TestNetwork(Scene):
    def construct(self,):
 
        #--Constants and Stuff
        _shift_val = 4
        _run_time  = 1
 
        #--Create the layers
        input_layer = generate_network_layer(
            num_nodes       = 2,
            include_bias    = True, 
            layer_type      = 'input', 
            layer_idx       = 0,
        )
 
        hidden_layer = generate_network_layer(
            num_nodes       = 3,
            include_bias    = True, 
            layer_type      = 'hidden', 
            layer_idx       = 1,
        )
 
        output_layer = generate_network_layer(
            num_nodes       = 1,
            include_bias    = False, 
            layer_type      = 'output', 
            layer_idx       = 2,
        )
 
        #-- Draw the layers
        self.play(*[Create(item, run_time=1) for item in input_layer]) 
        self.play(input_layer.animate.shift(LEFT * _shift_val))    
        self.wait(0.5)
 
        self.play(*[Create(item, run_time=_run_time) for item in hidden_layer]) 
        self.wait(0.5) 
 
        output_layer.shift(RIGHT * _shift_val).shift(UP * 0.75) 
        self.play(*[Create(item, run_time=_run_time) for item in output_layer])    
        self.wait(0.5)
 
        #----------------------------
        #-- Create arrows 
        input_hidden_arrows  = generate_layer_connections(input_layer[0], hidden_layer[0])
        hidden_output_arrows = generate_layer_connections(hidden_layer[0], output_layer[0])
 
        self.play(*[GrowArrow(arrow) for arrow in input_hidden_arrows])
        self.wait()
 
        self.play(*[GrowArrow(arrow) for arrow in hidden_output_arrows])
        self.wait(2)
 
        #------------------------------
        #-- add labels to connections
        self.play(Uncreate(input_hidden_arrows), Uncreate(hidden_output_arrows))
        self.wait()
 
        labeled_input_hidden_arrows = generate_random_labeled_layer_connections(input_layer[0], hidden_layer[0], font_size=15, add_frame=True,)
        self.play(*[GrowArrow(arrow) for arrow in labeled_input_hidden_arrows])
        self.wait(0.4)
 
        labeled_hidden_output_arrows = generate_random_labeled_layer_connections(hidden_layer[0], output_layer[0], font_size=15, add_frame=True,)
        self.play(*[GrowArrow(arrow) for arrow in labeled_hidden_output_arrows])
        self.wait()


def generate_network_layer(
    num_nodes, 
    include_bias    = True, 
    layer_type      = 'hidden', 
    orientation     = 'vertical',
    node_buffer     = 0.75, 
    add_node_labels = True,
    font_size       = 30,
    add_layer_label = True,
    layer_font_size = 35,
    layer_idx       = None,
    shape_params:dict = {},
    ):


    node_shape = None
    if layer_type.lower() == 'input':
        node_shape = Square
        default_shape_params = {
            'side_length'  : 1,
            'fill_opacity' : 0.6,
            'color'        : GREEN
        }

        shape_params = default_shape_params | shape_params

    elif layer_type.lower() == 'hidden':
        node_shape = Circle
        default_shape_params = {
            'radius'       : 0.6,
            'fill_opacity' : 0.6,
            'color'        : BLUE
        }

        shape_params = default_shape_params | shape_params

    elif layer_type.lower() == 'output':
        node_shape = Circle 
        default_shape_params = {
            'radius'       : 0.6,
            'fill_opacity' : 0.6,
            'color'        : BLUE
        }

        shape_params = default_shape_params | shape_params

    else:
        node_shape = Circle
        default_shape_params = {
            'radius'       : 0.6,
            'fill_opacity' : 0.6,
            'color'        : BLUE
        }
        
        shape_params = default_shape_params | shape_params


    layer_group = VGroup()  #this group will contain everything here to return

    #-- Create regular nodes and add them to a group
    layer_nodes = VGroup(*[node_shape(**shape_params) for i in range(num_nodes)])
    
    layer_group.add(layer_nodes)

    #-- Create bias node and add it to the group
    if include_bias:
        bias_node = input_bias  = Circle(color=RED, fill_opacity=0.6, radius=0.35)
        bias_node.is_bias_node = True   #add custom attribute to check layer
        layer_nodes.add(bias_node)  #add temporarily here to make arrangement easier


    #-- Arrange the nodes either in a vertical column or in a horizontal row
    if orientation.lower() == 'horizontal' or orientation.lower() == 'h':
        layer_nodes.arrange(LEFT, buff=node_buffer)
    elif orientation.lower() == 'vertical' or orientation.lower() == 'v':
        layer_nodes.arrange(DOWN, buff=node_buffer)


    #-- remove bias node to make labeling simpler
    if include_bias:
        layer_nodes -= bias_node
        #layer_group.add(bias_node)

    #-- add main label to layer
    if add_layer_label:
        if layer_idx is None:
            if layer_type.lower()[0] == 'i':
                layer_idx=0
            else:
                layer_idx='n'
            
        layer_label = Tex(fr"{layer_type.capitalize()} Layer (\(L_{layer_idx}\))", font_size=layer_font_size)
        layer_label.next_to(layer_nodes, UP, buff=0.25)

        layer_group.add(layer_label)

    #-- add labels to main nodes
    if add_node_labels:
        label_letter = layer_type.lower()[0]    #use the first letter of the layer type
        node_labels = VGroup(*
            [
                Tex(
                    fr"\({label_letter}_{i}\)", 
                    font_size=font_size
                )
                for i in range(num_nodes)
            ]           
        )
        
        for label, node in zip(node_labels, layer_nodes):
            label.move_to(node)

        layer_group.add(node_labels)

        if include_bias:
            bias_label = Tex(r"b", font_size=font_size)
            bias_label.move_to(bias_node)
            layer_group.add(bias_label)

    # add bias node back into the layer_nodes group
    if include_bias:
        layer_nodes.add(bias_node)


    #-- Return the group containing all the nodes and labels
    return layer_group


def generate_layer_connections(source_layer:VGroup, target_layer:VGroup, arrow_width=2.5):
    '''source_layer and target_layer are both VGroups containing only nodes and bias'''
    arrow_group = VGroup() 

    for j, target_node in enumerate(target_layer):
        if hasattr(target_node,'is_bias_node'): #skip bias nodes for incoming arrows from previous layer
            continue

        for i, source_node in enumerate(source_layer):
            arrow = Arrow(
                source_layer[i].get_right(), 
                target_layer[j].get_left(), 
                stroke_width=arrow_width,
            )
            arrow_group.add(arrow)

    return arrow_group

def generate_random_labeled_layer_connections(
        source_layer:VGroup, 
        target_layer:VGroup, 
        arrow_width=2.5, 
        label_position=0.15, 
        font_size=10, 
        add_frame=True, 
        weights:np.ndarray|list[list] = None):
    
    """
    
    Parameters
    ----------
    weights: np.array | list[list]
        A 2d array with shape = (len(source_layer) , len(target_layer))
    """
    
    arrow_group = VGroup()

    if weights is None:
        weights = np.random.uniform(-0.6, 0.6, size=(len(source_layer), len(target_layer)))
    elif isinstance(weights, np.array):
        assert(weights.shape == (len(source_layer), len(target_layer)))
    elif isinstance(weights, list):
        assert( (len(weights), len(weights[0])) == (len(source_layer), len(target_layer))    )
        weights = np.array(weights)
    else:
        print(f"Unsupported type `{weights.type}` for 'weights'.")
        raise TypeError

    for j, target_node in enumerate(target_layer):
        if hasattr(target_node, 'is_bias_node'):
            continue 

        for i, source_node in enumerate(source_layer):
            arrow = LabeledArrow(
                #label = f"{np.random.uniform(-0.6, 0.6):.2f}",
                label = f"{weights[i,j]:.2f}",
                label_position = label_position,
                font_size = font_size,
                label_frame = add_frame,
                start = source_layer[i].get_right(),
                end   = target_layer[j].get_left(),
                stroke_width = arrow_width
            )
            arrow_group.add(arrow)

    return arrow_group