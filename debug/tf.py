# This is a dummy tf module to allow module testing outside of TinyFugue.

def err( argstr ):
	print("tf.err  |", argstr)

def eval( argstr ):
	print("tf.eval |", argstr)
	return ""

def getvar( var, default="" ):
	print("tf.getvar |", var, default)
	return default

def out( argstr ):
	print("tf.out  |", argstr)

def send( text, world="<current>" ):
	print("tf.send %s |" % test)
	
def world():
	return "Dummy"

