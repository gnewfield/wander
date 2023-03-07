import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np

def get_image(tokenId):
    url = f'https://d1ghtrcnyzigje.cloudfront.net/{tokenId}.png'
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def get_images(start_id, end_id):
    if 0 < start_id < end_id <= 38045:
        for tokenId in range(start_id, end_id + 1):
            url = f'https://d1ghtrcnyzigje.cloudfront.net/{tokenId}.png'
            print('Downloading ' + url)
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save(f'images/crowd_{tokenId}.png')

def wander(start_id, end_id):
    NUM_TRANSITION_STEPS = 100
    FRAMES_PER_SECOND = 30
    PAUSE_LENGTH_SECONDS = 1
    NUM_PAUSE_FRAMES = FRAMES_PER_SECOND * PAUSE_LENGTH_SECONDS

    IMAGE_WIDTH = 4000
    IMAGE_HEIGHT = 3891

    # cv2.VideoWriter(fileName, codex, fps, dimensions)
    video = cv2.VideoWriter('wander.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FRAMES_PER_SECOND, (IMAGE_WIDTH, IMAGE_HEIGHT))

    curr_image = cv2.imread(f'images/crowd_{start_id}.png')
    curr_image_array = np.array(curr_image)
    for tokenId in range(start_id + 1, end_id):
        # Pause on curr image before transitioning to next
        for pause_frame in range(NUM_PAUSE_FRAMES):
            video.write(curr_image_array.astype('uint8'))

        # Load next image and transition
        next_image = cv2.imread(f'images/crowd_{tokenId + 1}.png')
        next_image_array = np.array(next_image)

        # Calculate the RGB values for each intermediate step
        for i in range(NUM_TRANSITION_STEPS):
            # Calculate the interpolation factor for this step
            alpha = i / (NUM_TRANSITION_STEPS - 1)

            # Interpolate between the two images
            interpolated_array = (1 - alpha) * curr_image_array + alpha * next_image_array

            # Save the interpolated image
            video.write(interpolated_array.astype('uint8'))

        curr_image_array = next_image_array

    cv2.destroyAllWindows()
    video.release()

if __name__ == '__main__':
    START_ID = 1
    END_ID = 100
    get_images(START_ID, END_ID)
    wander(START_ID, END_ID)
