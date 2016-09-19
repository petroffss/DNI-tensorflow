'''
Using CIFAR10
data download in :https://www.cs.toronto.edu/~kriz/cifar.html
data -- a 10000x3072 numpy array of uint8s. Each row of the array stores a 
		32x32 colour image. The first 1024 entries contain the red channel 
		values, the next 1024 the green, and the final 1024 the blue. The 
		image is stored in row-major order, so that the first 32 entries of
		 the array are the red channel values of the first row of the image.
labels -- a list of 10000 numbers in the range 0-9. The number at index i 
		indicates the label of the ith image in the array data.
'''
import tensorflow as tf
import os
from data_loader import cifar
import pprint
import classifier
import numpy as np
flags = tf.app.flags
pp = pprint.PrettyPrinter().pprint

tf.app.flags.DEFINE_integer('max_step', 50000, 'Number of batches to run.')
tf.app.flags.DEFINE_string('model_name', 'cnn', 'model used here')
tf.app.flags.DEFINE_string('checkpoint_dir', './checkpoint', 'save the ckpt model')
tf.app.flags.DEFINE_string('gpu_fraction', '1/2', 'define the gpu fraction used')
tf.app.flags.DEFINE_integer('batch_size', 256, '')
tf.app.flags.DEFINE_integer('test_batch_size', 256, '')
tf.app.flags.DEFINE_integer('hidden_size', 1000, '')
tf.app.flags.DEFINE_integer('output_size', 10, '')
tf.app.flags.DEFINE_integer('test_per_iter', 1000, '')
tf.app.flags.DEFINE_integer('max_to_keep', 20, '')
tf.app.flags.DEFINE_string('optim_type', 'adam', '[exp_decay, adam]')
# exponetial decay
#tf.app.flags.DEFINE_float('init_lr', 0.1, '')
tf.app.flags.DEFINE_float('decay_factor', 0.1, '')
tf.app.flags.DEFINE_integer('num_epoch_per_decay', 350, '')
# adam optimizer
tf.app.flags.DEFINE_float('init_lr', 3e-5, '')

conf = flags.FLAGS
# set random seed
append = lambda x: '/data2/andrewliao11/cifar-10-batches-py/data_batch_'+x
train_filename = [ append(str(i+1)) for i in range(5)]
test_filename = '/data2/andrewliao11/cifar-10-batches-py/test_batch'

def calc_gpu_fraction(fraction_string):
	idx, num = fraction_string.split('/')
	idx, num = float(idx), float(num)

	fraction = 1 / (num - idx + 1)
	print "[*] GPU : %.4f" % fraction
	return fraction

def main(_):

	attrs = conf.__dict__['__flags']
	pp(attrs)
	conf.checkpoint_dir = os.path.join(conf.checkpoint_dir, conf.model_name)
	dataset = cifar()
	
	gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=calc_gpu_fraction(conf.gpu_fraction))
	with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
		model = classifier.mlp(sess, dataset, conf, num_train=dataset.num_train, input_size=dataset.input_size)
		if conf.model_name == 'cnn':
			model.build_cnn_model()
		elif conf.model_name == 'mlp':
			model.build_mlp_model()
		else:
			assert()
		model.train()	

if __name__ == '__main__':
	tf.app.run()
