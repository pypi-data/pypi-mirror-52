"""
Deepstack core.
"""
import requests
from PIL import Image
from typing import Union, List, Set, Dict

## Const
HTTP_OK = 200
DEFAULT_TIMEOUT = 10  # seconds


def format_confidence(confidence: Union[str, float]) -> float:
    """Takes a confidence from the API like 
       0.55623 and returne 55.6 (%).
    """
    return round(float(confidence) * 100, 1)


def get_confidences_above_threshold(
    confidences: List[float], confidence_threshold: float
) -> List[float]:
    """Takes a list of confidences and returns those above a confidence_threshold."""
    return [val for val in confidences if val >= confidence_threshold]


def get_object_labels(predictions: List[Dict]) -> List[str]:
    """
    Get a list of the unique object labels predicted.
    """
    labels = [pred["label"] for pred in predictions]
    return list(set(labels))


def get_label_confidences(predictions: List[Dict], target_label: str):
    """
    Return the list of confidences of instances of target label.
    """
    confidences = [
        pred["confidence"] for pred in predictions if pred["label"] == target_label
    ]
    return confidences


def get_objects_summary(predictions: List[Dict]):
    """
    Get a summary of the objects detected.
    """
    labels = get_object_labels(predictions)
    return {
        label: len(get_label_confidences(predictions, target_label=label))
        for label in labels
    }


def post_image(url: str, image: bytes, api_key: str, timeout: int):
    """Post an image to Deepstack."""
    try:
        response = requests.post(
            url, files={"image": image}, data={"api_key": api_key}, timeout=timeout
        )
        return response
    except requests.exceptions.Timeout:
        raise DeepstackException(
            f"Timeout connecting to Deepstack, current timeout is {timeout} seconds"
        )


class DeepstackException(Exception):
    pass


class DeepstackObject:
    """The object detection API locates and classifies 80 
    different kinds of objects in a single image.."""

    def __init__(
        self,
        ip_address: str,
        port: str,
        api_key: str = "",
        timeout: int = DEFAULT_TIMEOUT,
    ):

        self._url_object_detection = "http://{}:{}/v1/vision/detection".format(
            ip_address, port
        )
        self._api_key = api_key
        self._timeout = timeout
        self._predictions = []

    def process_file(self, file_path: str):
        """Process an image file."""
        with open(file_path, "rb") as image_bytes:
            self.process_image_bytes(image_bytes)

    def process_image_bytes(self, image_bytes: bytes):
        """Process an image."""
        self._predictions = []

        response = post_image(
            self._url_object_detection, image_bytes, self._api_key, self._timeout
        )

        if response.status_code == HTTP_OK:
            if response.json()["success"]:
                self._predictions = response.json()["predictions"]
            else:
                error = response.json()["error"]
                raise DeepstackException(f"Error from Deepstack: {error}")

    @property
    def predictions(self):
        """Return the classifier attributes."""
        return self._predictions
