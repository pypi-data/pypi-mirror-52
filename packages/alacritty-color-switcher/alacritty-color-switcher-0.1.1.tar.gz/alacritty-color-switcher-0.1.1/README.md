# Alacritty Color Switcher

## Example
```
> acs --list
one_dark
tomorrow_night
solarized_light
solarized_dark
nord

> acs --apply nord
nord # -> ~/.config/alacritty/alacritty.yml is updated

> acs --switch
one_dark #
```

**Warning**: please make a backup of your `alacritty.yml` since `acs` overwrites
the content with the changed color file! **Also the formatting will be lost
partially!**


## Install
```
pip install alacritty-color-switcher
```

Create a directory with all your color schemes
```
mkdir ~/.config/alacritty-colors
mv your_color_scheme.yaml ~/.config/alacritty-colors/
```

`acs` will find all files with `yaml` or `yml` as suffix.
The color schemes should have the same structure as showed on the [Alacritty
Wiki](https://github.com/jwilm/alacritty/wiki/Color-schemes).
