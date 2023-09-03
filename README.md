# google-font-to-fpm

**How to use font**: [Read this documentation](https://fastn.com/create-font-package/)

Lets try to add fifthtry.github.io/roboto font in a fastn package

1. In FASTN.ftd file, add the following line

```ftd
-- fastn.dependency: fifthtry.github.io/roboto
```

2. In the file, lets say foo.ftd, where you want to use it, add this at the 
   beginning of the file
   
```ftd
-- import: fifthtry.github.io/roboto/assets as font-assets

-- ftd.type dtype:
size.px: 40
weight: 900
font-family: $font-assets.fonts.Roboto
line-height.px: 65
letter-spacing.px: 5
```

The above will create a variable `dtype` with font-family as `Roboto`

3. In foo.ftd, use font:

```ftd
--- ftd.text: Hello World
role: $dtype
```
