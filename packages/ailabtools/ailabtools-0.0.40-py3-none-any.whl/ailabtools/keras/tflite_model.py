import os, sys
import numpy as np
import cv2
    
class TFLiteModel:
    
    def __init__(self, tf, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
        self.target_img_size = tuple(self.input_shape[1:3])

    def preprocess(self, input):
        return np.array(input).astype(np.float32) / 127.5 - 1

    def predict(self, image, color_mode='rgb'):
        assert color_mode in ['bgr', 'rgb']
        image = cv2.resize(image, self.target_img_size)
        if color_mode == 'bgr':
            image = image[:,:,::-1]
        
        image = self.preprocess(image)[np.newaxis,:,:,:]

        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()

        outputs = [self.interpreter.get_tensor(out['index']) for out in self.output_details]

        if len(outputs) == 1:
            return outputs[0]
        else:
            return outputs