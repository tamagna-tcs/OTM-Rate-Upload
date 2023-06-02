import logging

def get_logger():
    logger = logging.getLogger('general')
    return logger

def error(message):
    get_logger().error(message)
    print("ERROR " + message)

def info(message):
  get_logger().info(message)
  print("INFO " + message)

