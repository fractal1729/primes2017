import argparse
import os.path
import re
import sys
import tarfile
import time

import numpy as np
from six.moves import urllib
import tensorflow as tf

FLAGS = None
DEFAULT_MODEL_DIR = '/tmp/imagenet'

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# pylint: enable=line-too-long

class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          DEFAULT_MODEL_DIR, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          DEFAULT_MODEL_DIR, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.

    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.

    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      DEFAULT_MODEL_DIR, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image): # function decomissioned; use run_inference_on_images() instead.
  """Runs inference on an image.

  Args:
    image: Image file name.

  Returns:
    Nothing
  """
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # Creates graph from saved GraphDef.
  create_graph()

  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('pool_3:0')
    predictions = sess.run(softmax_tensor,
                            {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)

    return predictions

    # # Creates node ID --> English string lookup.
    # node_lookup = NodeLookup()

    # top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
    # for node_id in top_k:
    #   human_string = node_lookup.id_to_string(node_id)
    #   score = predictions[node_id]
    #   print('%s (score = %.5f)' % (human_string, score))

def run_inference_on_images(images):
	images_data = []
	for image in images:
	  if not tf.gfile.Exists(image):
	    tf.logging.fatal('File does not exist %s', image)
	  image_data = tf.gfile.FastGFile(image, 'rb').read()
	  images_data.append(image_data)
	create_graph()
	m = len(images)
	with tf.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name('pool_3:0')
		features = np.zeros((m, 2048))
		start = time.time()
		for j in range(m):
			prediction = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': images_data[j]})
			prediction = np.squeeze(prediction)
			features[j] = prediction
			sys.stdout.write("\r"+str(j)+" of "+str(m)+" complete.   ")
			sys.stdout.flush()
		print ""
		end = time.time()
		print "total time: "+str(end-start)
		return features

def maybe_download_and_extract():
  """Download and extract model tar file."""
  dest_directory = DEFAULT_MODEL_DIR
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    def _progress(count, block_size, total_size):
      sys.stdout.write('\r>> Downloading %s %.1f%%' % (
          filename, float(count * block_size) / float(total_size) * 100.0))
      sys.stdout.flush()
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
    print()
    statinfo = os.stat(filepath)
    print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
  tarfile.open(filepath, 'r:gz').extractall(dest_directory)

def main(n): # function decomissioned; use compileAll instead.
  # n = '17'
  m = 5
  maybe_download_and_extract()
  # print(run_inference_on_image('nn/cropped_panda.jpg'))
  # for j in range(m):
  #   start = time.time()
  #   imgfile = 'cairo/test_cases/svmdata/'+n+'-'+str(j)+'.png'
  #   f = run_inference_on_image(imgfile)
  #   features[j] = f
  #   print imgfile+" done"
  #   end = time.time()
  #   print "time: "+str(end-start)
  #   time.sleep(0.5)
  start = time.time()
  imgfiles = []
  for j in range(m):
  	imgfiles.append('cairo/test_cases/svmdata/'+n+'-'+str(j)+'.png')
  features = run_inference_on_images(imgfiles)
  print n+" done"
  end = time.time()
  print "time: "+str(end-start)
  np.save("nn/inceptionfeatures/"+n, features)



def compileAll(n=18,m=5):
	maybe_download_and_extract()
	imgfiles = []
	for i in range(n):
		for j in range(m):
			imgfiles.append('cairo/test_cases/svmdata/'+'{:02}'.format(i)+'-'+str(j)+'.png')
	print "Images loaded"
	features = run_inference_on_images(imgfiles)
	print "Inference complete"
	np.save("nn/inceptionfeatures/allfeatures", features)
	print "Save complete"


# def run(n):
#   parser = argparse.ArgumentParser()
#   # classify_image_graph_def.pb:
#   #   Binary representation of the GraphDef protocol buffer.
#   # imagenet_synset_to_human_label_map.txt:
#   #   Map from synset ID to a human readable string.
#   # imagenet_2012_challenge_label_map_proto.pbtxt:
#   #   Text representation of a protocol buffer mapping a label to synset ID.
#   # parser.add_argument(
#   #     '--model_dir',
#   #     type=str,
#   #     default='/tmp/imagenet',
#   #     help="""\
#   #     Path to classify_image_graph_def.pb,
#   #     imagenet_synset_to_human_label_map.txt, and
#   #     imagenet_2012_challenge_label_map_proto.pbtxt.\
#   #     """
#   # )
#   # # parser.add_argument(
#   # #     '--image_file',
#   # #     type=str,
#   # #     default='',
#   # #     help='Absolute path to image file.'
#   # # )
#   # parser.add_argument(
#   #     '--num_top_predictions',
#   #     type=int,
#   #     default=5,
#   #     help='Display this many predictions.'
#   # # )
#   # FLAGS, unparsed = parser.parse_known_args()
#   # #unparsed.append(str(n))
#   # print FLAGS

#   tf.app.run(main=main, argv=[sys.argv[0], n])

# if __name__ == '__main__':
#  	run(3)