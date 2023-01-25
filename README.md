# google-font-to-fpm

#How to use font: [Read this documentation](https://fpm.dev/how-to/create-font-package/)

Lets try to add fifthtry.github.io/roboto font in a fpm package

1. In FPM.ftd file, add the following line

```ftd
-- fpm.dependency: fifthtry.github.io/roboto
```

2. In the file, lets say foo.ftd, where you want to use it, add this at the 
   beginning of the file
   
```ftd
-- import: fifthtry.github.io/roboto/assets as font-assets

-- fpm.font-display: $font-assets.fonts.Roboto
```

The above will update the variable `font-display`. There are other two 
such variables: `font-copy` and `font-code`. `font-copy` is used for font family in
body type variables (`body-large`, `body-medium` and `body-small`), 
`font-display` for rest of the variables and `font-code` (right now not in use) 
with default value as `sans-serif`. The above code update the `font-display` 
variable with the value `Roboto`.

3. In foo.ftd, use font:

```ftd
--- ftd.text: Hello World
role: $fpm.type.headline-large
```
