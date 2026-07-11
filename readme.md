## Usage
1. Download the repo using the green `Code` button -> Download ZIP or using git clone
2. Extract the zip
3. Put the unmodified shader zip in the extracted folder
    * The folder should contain the diffs, `texture` folder, `shader-patch.py`, and the shader zip
4. Open a terminal in the folder or cd to it (`cd path/to/extracted/folder`)
5. Run this command:  
```python shader-patch.py "iterationRP Alpha (ver).zip" "itrp-patch-(ver).diff" "(ver)-patched.zip"```  
You might need to do it using bash (you can get it from [git](https://git-scm.com/install/windows)) instead of windows cmd if you get a file not found error.  
Use `itrp-patch-24.diff` for 0.8.24, `itrp-patch-23.diff` for 0.8.23, `itrp-patch-22.diff` for 0.8.22, `itrp-patch-18.diff` for 0.8.18, `itrp-patch-16.diff` for 0.8.13~0.8.16 (does not implement toggleable settings). **All new releases will generally be for the most recent shader version only.** 

> ### Patcher now automatically copies textures into the shader!
> Make sure the textures folder is in the same directory as the python file.  
> You can **generate your own bloom kernels [here](https://huj31415.github.io/fft2d-webgpu/)!** (Requires WebGPU support in your browser, and **use the normalize option**)  
> Without kernelTex there will be nothing to convolve!

6. Move the patched shader output to your shaderpacks folder and enjoy!

## Generating a diff
Now uses gnu diff

```diff -rua --strip-trailing-cr "original-unzipped-folder" "patched-unzipped-folder" > patch.diff```

## Changelog
### v2026.7.11 Initial update to 0.8.24
* **Update to ver. 0.8.24**
* Convolution bloom now **requires Iris 1.10.5+** due to the base shader using more custom image slots, haven't tested older versions with it off.
  * Might look into a workaround
* Known issue: blue lines from convolution bloom in dark environments
* Possible todo: move cloud shadow texture to colortex23 instead of custom image, however would cause the whole patch to require Iris 1.10.5+

### v2026.7.5 Atmospherics overhaul
* **Update to ver. 0.8.23**
* Port Revelation's cloud system
  * Rendered at 1/(2 * FSR scale) resolution
  * Texture based cloud shadows, Added temporal reprojection
  * Integrated into ambient lighting
  * Added cloud self-shadow softening
  * Should be a bit faster than before
* Original planar clouds kept
* Fix cloud lighting to be based on cloud altitude instead of player position
  * Clouds are now illuminated before sunrise/after sunset
* Adjusted weather based coverage
  * Rainstorms will have some breaks in the clouds
  * Thunderstorms have 100% coverage with darker/denser clouds
* Apply cloud shadows to particles
* Dynamic fog thickness (varies based on world day)
* Rain/Fog dispersion effects
  * Rainbows based on geometric optics
  * Fog glories, corona on cirrus clouds based on Mie scattering
* Adjusted underwater volumetric caustic rays
* Fixed star rotation to follow planet rotation axis (based on sun path angle)
* Minor fix for TACZ 3rd person rendering

Cloud textures and code based on Revelation by HaringPro (Apache 2.0 License)

### v2026.5.26 Convolution bloom release
* Add convolution bloom support. **Ver. 0.8.22 Only**

### v2026.5.10
* Add support for IterationRP Alpha 0.8.22
* Fix clouds rendering behind terrain based on [SoczystaWolowina edit](https://github.com/Erykuuu/IterationRp-SoczystaWolowina-edits) (currently 0.8.22 only)
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
* Supports IterationRP Alpha 0.8.10~0.8.23, future versions may require manual patching


## Technical details of the convolution bloom implementation

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
