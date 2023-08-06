import torch
import cv2
import time
import argparse
import subprocess

from rectifai.models import posenet, posturenet
from rectifai.models.posenet.decode import *
from rectifai.tools.utils.posenet import *
from rectifai.models.posturenet.config import input_size

parser = argparse.ArgumentParser()
parser.add_argument('--no-preview',action='store_true')
args = parser.parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():
    print("***********************************************")
    print("Loading posenet model for keypoint detection...")
    posenet_model = posenet.load_model().to(device)

    cap = cv2.VideoCapture(0)  # Initial Camera
    cap.set(3, 1280)
    cap.set(4, 720)

    print("Loading Posture Detection model..")

    posturenet_model = posturenet.load_model().to(device)
    prev_heading = ""
    while True:
        input_image, display_image, output_scale = read_cap(cap)

        with torch.no_grad():
            input_image = torch.Tensor(input_image).to(device)
            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = posenet_model(input_image)

            pose_scores, keypoint_scores, keypoint_coords = decode_multiple_poses(
                heatmaps_result.squeeze(0),
                offsets_result.squeeze(0),
                displacement_fwd_result.squeeze(0),
                displacement_bwd_result.squeeze(0)
                )

        keypoint_coords *= output_scale

        overlay_image, keypoint_coords, status = draw_skeleton_and_keypoints(
            display_image, pose_scores, keypoint_scores, keypoint_coords
            )
        

        with torch.no_grad():
            key_points_input = torch.Tensor(keypoint_coords).reshape(-1, input_size).to(device)
            output = posturenet_model(key_points_input)
            _, predicted = torch.max(output.data, 1)

            op = predicted.sum()//len(predicted)
            posture_status = 'bad' if op.data.tolist() == 0 else 'good'

        if not args.no_preview:
            cv2.imshow('posenet', overlay_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if posture_status == 'bad':
            heading = 'Bad Pose Detected!'
            msg = 'Please Rectify!!'
        else:
            heading = 'Great!'
            msg = 'Your posture looks good..'
        if not prev_heading == heading:
            print(heading,msg)
            subprocess.call(['notify-send',heading,msg,'--urgency=critical', '--expire-time=100'])
            prev_heading = heading


if __name__ == "__main__":
    main()