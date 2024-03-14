import numpy as np
import matplotlib.pyplot as plt    
from PIL import Image
from io import BytesIO


def show_training_metrics(logs):
    """Display training epoch logs, parse accuracy and loss, and plot."""
    
    training_log = logs.split("Monitoring the collections: ")[1].split("\n")[1:]
    training_log = "\n".join(training_log).split("Setting weights to model with maximum val_accuracy at epoch")[0]
    
    training_metrics = {
        "loss": [],
        "accuracy": [],
        "top_5_accuracy": [],
        "val_loss": [],
        "val_accuracy": [],
        "val_top_5_accuracy": [],
    }

    for item in training_log.split(" - "):
        if not ":" in item: # Not a metric
            continue
        metric, value = item.split(": ")
        training_metrics[metric].append(float(value))
        
    print("Training metrics:\n", training_metrics)
    
    fig, ax = plt.subplots(1,2, figsize=(10,4))
    ax[0].plot(training_metrics["accuracy"], color='blue', label="Train")
    ax[0].plot(training_metrics["val_accuracy"], color='orange', label="Val")
    ax[0].set_xlabel("Epoch")
    ax[0].set_ylabel("Accuracy")
    ax[0].legend()

    ax[1].plot(training_metrics["loss"], color='lightblue', label="Train")
    ax[1].plot(training_metrics["val_loss"], color='yellow', label="Val")
    ax[1].set_xlabel("Epoch")
    ax[1].set_ylabel("Loss")
    ax[1].legend()

    plt.show()
    

def read_image_from_s3(key, bucket):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)


def read_image_from_s3_as_bytes(key, bucket):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    bytestring representation of image.
    """
    
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    buffer = BytesIO()
    im.save(buffer, format='JPEG')
    byte_im = buffer.getvalue()

    return byte_im


def write_image_to_s3(img_array, key, bucket):
    """Write an image array into S3 bucket

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    None
    """
    
    object = bucket.Object(key)
    file_stream = BytesIO()
    im = Image.fromarray(img_array)
    im.save(file_stream, format='jpeg')
    object.put(Body=file_stream.getvalue())