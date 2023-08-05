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
