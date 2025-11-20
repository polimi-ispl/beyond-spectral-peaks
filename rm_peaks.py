import os
import argparse
from PIL import Image
import numpy as np
from skimage.morphology import binary_dilation, disk


def grid_mask_circles(H, W, grid_step, mask_radius):

    # NB: we suppose to work with squared images, where H = W

    # build a binary mask that works in the fft-shifted domain
    binary_mask = np.zeros(shape=(H, W), dtype=bool)

    # if the grid_step is 8, it means that we need to insert the grid every img_size // grid_step
    binary_mask[H//grid_step::H//grid_step, W//grid_step::W//grid_step] = True

    binary_mask[H // 2, W // 2] = False # We want to keep the (0, 0) frequency

    # build the disk around the dots
    # radius = 10 is ok for squared images with size 1024 x 1024
    # if image-size is bigger, the radius is automatically tuned (e.g., if H = 2048, radius = 20)
    disk_f = disk(mask_radius * (H // 1024))
    binary_mask = binary_dilation(binary_mask, footprint=disk_f)

    # reverse the mask, as we want to keep everything apart from the grid pattern
    binary_mask = 1 - binary_mask

    return binary_mask


def remove_pattern(img_path, mask):

    # load image
    img = np.array(Image.open(img_path).convert("RGB"))

    # compute the image spectrum (fft-shifted)
    fft_img = np.fft.fftshift(np.fft.fft2(img, axes=(0, 1), norm='ortho'), axes=(0, 1))

    abs_masked_fft = np.abs(fft_img)
    phase_masked_fft = np.angle(fft_img)

    # Apply mask to all color channels
    for c in range(fft_img.shape[2]):
        # modify both magnitude and phase
        abs_masked_fft[:, :, c] = abs_masked_fft[:, :, c] * mask
        phase_masked_fft[:, :, c] = phase_masked_fft[:, :, c] * mask

    peal_removed_fft = abs_masked_fft * np.exp(1j * phase_masked_fft)

    # go back to the image domain
    peak_removed_img = np.real(np.fft.ifft2(np.fft.fftshift(peal_removed_fft, axes=(0, 1)), axes=(0, 1), norm='ortho'))

    # match the input dynamic range and convert into uint8
    peak_removed_img = np.uint8(np.round(((peak_removed_img - peak_removed_img.min()) / (peak_removed_img.max() -
                                                                                         peak_removed_img.min()) *
                                          (np.float32(img).max() - np.float32(img).min()) + np.float32(img).min())))

    return peak_removed_img


def main(args):

    img_size = Image.open(args.in_path).size

    output_folder = os.path.join(args.out_dir, 'step-{}'.format(args.grid_step))
    os.makedirs(output_folder, exist_ok=True)

    # create the binary mask for removing the peaks
    binary_mask = grid_mask_circles(H=img_size[1], W=img_size[0], grid_step=args.grid_step, mask_radius=args.mask_radius)

    # remove the pattern
    peak_removed_np = remove_pattern(args.in_path, binary_mask)

    # save the final image
    peak_removed_img = Image.fromarray(peak_removed_np)
    peak_removed_img.save(os.path.join(output_folder, os.path.basename(args.in_path)))

    return 0


if __name__ == '__main__':

    # --- Setup an argument parser --- #
    parser = argparse.ArgumentParser()

    parser.add_argument('--in_path', help='Path of the input image', type=str, required=True)
    parser.add_argument('--out_dir', help='Output data dir', type=str, default='peak_removed')
    parser.add_argument('--mask_radius', help='Radius of the mask to apply to remove the peaks '
                                              '(default value is for 1024 x 1024 images)', type=int, default=10)
    parser.add_argument('--grid_step', help='Periodicity of the grid built to remove the peaks', type=int,
                        default=8)
    args = parser.parse_args()

    main(args)
















