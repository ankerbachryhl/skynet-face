import json
import argparse
import sys
import pdb
import glob
import base64
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials)


def detect_face(face_file, max_results=1):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """
    image_content = face_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('utf-8')
            },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    if 'faceAnnotations' in response['responses'][0]:
        return response['responses'][0]['faceAnnotations']

    else:
        print('The image didn*t contained a face...')
        return ''

for fname in glob.glob('niels.jpg'):
    print fname

    with open(fname, 'r') as fimage:
        data = detect_face(fimage)

    with open('{}.json'.format(fname), 'w') as fjson:
        print('Writing json')

        fjson.write(json.dumps(data))
