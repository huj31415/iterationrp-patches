## Patching a shader
You might need to do it using bash instead of windows cmd

```python shader-patch.py "iterationRP Alpha 0.8.18.zip" "itrp-patch-18.diff" "0.8.18-patched.zip"```

Use `itrp-patch-18.diff` for 0.8.18, `itrp-patch-16.diff` for 0.8.13~0.8.16 (does not implement settings)

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