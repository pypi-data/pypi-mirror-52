# crsEpsg

This is a simple python package that contains two dictionaries - i.e., `crs2epsg` and `epsg2crs`- with the correspondences between the CRS names and EPSG codes. For instance,

```python
crs2epsg = {
"Anguilla 1957 / British West Indies Grid":"2000",
"Antigua 1943 / British West Indies Grid":"2001",
"Dominica 1945 / British West Indies Grid":"2002",
...
}

epsg2crs = {
"2000":"Anguilla 1957 / British West Indies Grid",
"2001":"Antigua 1943 / British West Indies Grid",
"2002":"Dominica 1945 / British West Indies Grid",
"2003":"Grenada 1953 / British West Indies Grid",
...
}
```

I created this package to use it with las/LIDAR files, so, I included the function `getEPSG(filename, default)` that return the EPSG code from a las/LIDAR file. Some files contains larger CRS name (e.g., "ETRS89 / UTM zone 30N + Geoid" when the documented name is only "ETRS89 / UTM zone 30N"), so, this function will be cutting the last word until achieve the good portion of the CRS name.

```python
from crsEpsg import getEPSG
print("EPSG:", getEPSG("data/209341.las","32718"))
```

# Requirements

```bash
pip3 install liblas
pip3 install crsepsg
```

With this you should be ready to use this module. However, you have the alternative,
```bash
sudo apt-get install python-liblas
```

