## Usage
1. Download the repo using the green `Code` button -> Download ZIP or using git clone
2. Extract the zip
3. Put the unmodified shader zip in the extracted folder
    * The folder should contain the diffs, `shader-patch.py`, and the shader zip
4. Open a terminal in the folder or cd to it (`cd path/to/extracted/folder`)
5. Run the command below. You might need to do it using bash (you can get it from [git](https://git-scm.com/install/windows)) instead of windows cmd if you get a file not found error. Use `itrp-patch-18.diff` for 0.8.18, `itrp-patch-16.diff` for 0.8.13~0.8.16 (does not implement settings)

```python shader-patch.py "iterationRP Alpha (ver).zip" "itrp-patch-(ver).diff" "(ver)-patched.zip"```

6. Move the patched shader output to your shaderpacks folder and enjoy!


## Generating a diff
Requires git, you don't need to do this if you are using the provided patches

```git diff --no-index "original-unzipped-folder" "patched-unzipped-folder" > patch.diff```

## Patches (2026.4.22)
* Daily variable cloud cover for both volumetric and 2D clouds independently
* Cloud shadows from sun and moon affecting both ground and volumetric fog
  * Limit cloud shadow height to bottom of the cloud layer to prevent infinite shadow columns
* World time based cloud movement (clouds movement based on tick speed)
* Moon phase rendering and lighting, can be toggled and adjusted in settings
* Fix lighting on voxy LODs
* Blend noise fog with height based fog
* Fix DOF for stained glass (focuses and blurs based on background depth instead of glass depth)
* Supports IterationRP Alpha 0.8.10~0.8.18, future versions may require manual patching