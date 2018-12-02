"""
Define ConvNet as a model to be imported by main.py in order to fit a convolutional network. 
"""
from torch.nn import Module, Sequential, Conv1d, ReLU, MaxPool1d, Dropout, Linear

class ConvNet(Module):
    '''Define network structure in the constructor; then specify the logic of the forward pass 
    in a method called forward.
    '''
    def __init__(self, input_height, kernel_size, stride, padding):
        '''1. Convolve the single channel tensor into 8 and 16 channels respectively.
           2. Define how the amount of downsampling, spatial size of input, etc, map into the FC input dimension.
           3. Specify FC network with a hidden layer of width 10.
        '''
        super().__init__()
        
        ## 1. Convolve the tensor using 2 convolutional layers
        self.conv_layers = Sequential(Conv1d(300, 
                                             8, 
                                             kernel_size, 
                                             stride, 
                                             padding
                                            ),
                                      ReLU(),
                                      MaxPool1d(2),
                                      ## layer 1

                                      Conv1d(8, 
                                             16, 
                                             kernel_size,
                                             stride, 
                                             padding
                                            ),
                                      ReLU(),
                                      MaxPool1d(2),
                                      ## layer 2
                                      
                                      Conv1d(16, 
                                             64, 
                                             kernel_size,
                                             stride, 
                                             padding
                                            ),
                                      ReLU(),
                                      MaxPool1d(2)
                                      ## layer 3
                                     )
        self.dropout = Dropout()
        
        ## 2. Define FC input dimension
        def n_extracted_features(conv_layers, input_height, last_out_channel):
            N_LAYERS = len(conv_layers) / 3
            POOLED_DIM = input_height / 2**N_LAYERS  ##! check that evenly divides
            return int(last_out_channel * POOLED_DIM)   

        ## 3. Specify FC network
        self.N_EXTRACTED_FEATURES = n_extracted_features(self.conv_layers, input_height, 64)
        self.fc_layers = Sequential(
                                    Linear(self.N_EXTRACTED_FEATURES, 100),
                                    Linear(100, 20)
                                   )

    def forward(self, _input):
        '''1. Extract features by convolving raw tensor into features.
           2. Flatten the tensor; then feed into fully connected layers.
        '''
        print(self.conv_layers(_input).shape)
        
        _output = (self.conv_layers(_input)
                       .reshape(-1, self.N_EXTRACTED_FEATURES)
                  )
        _output = self.dropout(_output)
        return self.fc_layers(_output)