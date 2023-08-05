# ImgConvert

ImgConvert is a tool to convert images from an arbitrary format into PNG.

## Installation

```bash
$ pip install foliantcontrib.imgconvert
```

## Config

To enable the preprocessor, add `imgconvert` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - imgconvert
```

The preprocessor has a number of options with the following default values:

```yaml
preprocessors:
    - imgconvert:
        convert_path: convert
        cache_dir: !path .imgconvertcache
        image_width: 0
        formats: {}
```

`convert_path`
:   Path to `convert` binary. By default, it is assumed that you have this command in `PATH`. [ImageMagick](https://imagemagick.org/) must be installed.

`cache_dir`
:   Directory to store processed images. They may be reused later.

`image_width`
:   Width of PNG images in pixels. By default (in case when the value is `0`), the width of each image is set by ImageMagick automatically. Default behavior is recommended. If the width is given explicitly, file size may increase.

`formats`
:   Settings that apply to each format of source images.

The `formats` option may be used to define lists of targets for each format. If targets for a format are not specified explicitly, the preprocessor will be applied to all targets.

Example:

```yaml
formats:
    eps:
        targets:
            - site
    svg:
        targets:
            - docx
```

Formats should be named in lowercase.
