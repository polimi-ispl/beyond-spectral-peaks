# Beyond Spectral Peaks: Interpreting the Cues Behind Synthetic Image Detection

Sara Mandelli, Diego Vila-Portela, David Vázquez-Padín, Fernando Pérez-González, Paolo Bestagini

[Image and Sound Processing Lab - Politecnico di Milano](http://ispl.deib.polimi.it/)

atlanTTic Research Center, University of Vigo, E.E. de Telecomunicacion - Vigo, Spain

### Remove frequency peaks from an image

_Remove frequency peaks from the Fourier spectrum of an image with periodicity P = 8 or P = 16._
#### Input arguments

1. `--in_path` specifies the path to the input image
2. `--out_dir` specifies the output directory where to save the peak-removed image
3. `--mask_radius` specifies the radius of the disk-element used for the dilation of the binary mask.
4. `--grid_step` specifies the periodicity of the grid built to remove the peaks (this correponds to $P$).

#### Example of test with P = 8
```bash
python rm_peaks.py --in_path $PATH_TO_INPUT_IMAGE
```
### Additional results on real and laundered images

Additional results of state-of-the-art detectors on real images and their laundered versions can be found in [additional_results_real_laundered](#additional_results_real_laundered)
