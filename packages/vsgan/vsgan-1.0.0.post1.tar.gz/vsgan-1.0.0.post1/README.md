# VSGAN
VapourSynth GAN Implementation, based on ESRGAN's implementation

# Installation
`pip3 install vsgan`

PyTorch and CUDA needs to be installed seperately.

# Usage
```
import vsgan as VSGAN
(...)
result = VSGAN.Start(clip=clip, model=[string: path to .pth], scale=[int: model's scale], old_arch=[bool: only set to true for models not working with the current arch])
result.set_output()
```
The resulting video will be the same color space format as your input clip, BUT, it's currently assuming its matrix is 709, if your inputs matrix is different, please change it [at this line of code](https://github.com/imPRAGMA/VSGAN/blob/master/vsgan.py#L55). :(

Enjoy!
Thanks to:
- [xinntao](https://github.com/xinntao/ESRGAN) For RRDBNet_arch
- [VideoHelp.com](https://videohelp.com) For helping me
