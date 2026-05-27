## Usage
1. Download the repo using the green `Code` button -> Download ZIP or using git clone
2. Extract the zip
3. Put the unmodified shader zip in the extracted folder
    * The folder should contain the diffs, `shader-patch.py`, and the shader zip
4. Open a terminal in the folder or cd to it (`cd path/to/extracted/folder`)
5. Run the command below. You might need to do it using bash (you can get it from [git](https://git-scm.com/install/windows)) instead of windows cmd if you get a file not found error. Use `itrp-patch-22.diff` for 0.8.22, `itrp-patch-18.diff` for 0.8.18, `itrp-patch-16.diff` for 0.8.13~0.8.16 (does not implement toggleable settings)

```python shader-patch.py "iterationRP Alpha (ver).zip" "itrp-patch-(ver).diff" "(ver)-patched.zip"```

> ### **Important for the convolution bloom release:** Download the kernelTex.bin file and drop it into shaders/texture in the zip file. 
> Or you can **generate your own bloom kernels [here](https://huj31415.github.io/fft2d-webgpu/)!** (Requires WebGPU support in your browser, and **use the normalize option**)
> Without kernelTex there will be nothing to convolve!

6. Move the patched shader output to your shaderpacks folder and enjoy!

### Technical details of the convolution bloom implementation

* Uses radix-4 packed RGBA Cooley-Tukey FFT for size 1024 with radix-2 prepass for non-power-of-4 (2048)
  * All channels are independent so dispersed (rainbow diffraction) kernels are supported
* Directly samples, filters, and complex multiplies scene and kernel textures as inputs to FFT/IFFT passes without writing to intermediate textures
* 2 setup passes run once - kernel row and column FFT
* 4 extra passes per frame
  1. Sample and filter scene and do row FFT
  2. Column FFT
  3. Unpack channels, complex multiply with kernel spectrum, repack channels, and do row IFFT
  4. Column IFFT
* In my testing the performance impact was &le;5% with Nsight profiler overhead

## Generating a diff
Now uses gnu diff

```diff -rua --strip-trailing-cr "original-unzipped-folder" "patched-unzipped-folder" > patch.diff```

## Changelog
### v2026.5.26 Convolution bloom release
* Add convolution bloom support. **Ver. 0.8.22 Only**

### v2026.5.10
* Add support for IterationRP Alpha 0.8.22
* Fix clouds rendering behind terrain based on [Erykuuu's work](https://github.com/Erykuuu/IterationRp-SoczystaWolowina-edits) (currently 0.8.22 only)
### v2026.4.22
* Daily variable cloud cover for both volumetric and 2D clouds independently
* Cloud shadows from sun and moon affecting both ground and volumetric fog
  * Limit cloud shadow height to bottom of the cloud layer to prevent infinite shadow columns
  * Also apply to diffuse lighting
* World time based cloud movement (clouds movement based on tick speed)
* Moon phase rendering and lighting, can be toggled and adjusted in settings
* Fix lighting on voxy LODs (fixed in base shader as of 0.8.19)
* Blend noise fog with height based fog
* Fix DOF for stained glass (focuses and blurs based on background depth instead of glass depth)
* Add leaves SSS mult (adjusts how far light penetrates into leaves), default to 2.5* original
* Supports IterationRP Alpha 0.8.10~0.8.22, future versions may require manual patching