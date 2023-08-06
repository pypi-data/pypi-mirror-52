
## About
Python library for reading, modifying and writing Agisoft Photoscan/Metashape PSX projects. Unofficial.

Pretty rough at the moment. 

Questions? Contributions? Bug reports? Open an issue on the [gitlab page for the project](https://gitlab.com/dodgyville/pypsxlib).
I am very interested in hearing your use cases for `pypsxlib` to help drive the roadmap.

### Contributors
* Luke Miller

### Thanks

`pypsxlib` made for 'Project 39', a creative art project supported by Creative Victoria. 

### Roadmap
* Test suite to find where the psx specification is unsupported
* Create transformation objects for manipulation instead of strings
* Add texture support
* Add mask support
* Add dense cloud support
* Add depth maps support
* Copy images+masks across chunks

## Quickstart

### Installing
```
pip install pypsxlib
```

### How do I...

#### Load a .PSX project
```python3
from pypsxlib import Project 

project = Project().load_psx("myProject.psx")  # not all features supported
```

#### Save a .PSX project
```python3
project = Project("myProject")
project.path = "/path/for/project"
project.save()  # project.name and project.path must be set
```


#### Add a Chunk
```python3
p = Project("myProject")
p.defaults()  # create a new app and document
p.add_chunk()  # add an empty chunk
```

#### Access a chunk
```python3
chunk = p.apps[0].documents[0].chunks[0]
```

#### Access thumbnails
```python3
chunk.frames[0].thumbnails
```

#### Copy a chunk's bounding box to all other chunks
```python3
doc = project.apps[0].documents[0]  # or project.document shortcut
boundingbox =  copy.copy(doc.chunks[0].region)
for chunk in doc.chunks[1:]:
    chunk.region = boundingbox
```

#### Duplicate a Chunk
```python3
from pypsxlib import utils
p = Project().load("projects/sample.psx")
assert len(p.document.chunks) == 1
utils.duplicate_chunk(p, 0)
assert len(p.document.chunks) == 2
```


#### Access the point data of a mesh
```python3
doc = project.apps[0].documents[0]
mesh = doc.chunks[0].frames[0].model.mesh
print(mesh.faceCount)
# uses plyfile module to load data
print([x for x in doc.plydata])  # all the vertices
```

### Source
```
git clone https://gitlab.com/dodgyville/pypsxlib.git
```

## Reference

### .psx project layout

```
myProject.psx
myProject.files/
myProject.files/project.zip
myProject.files/<chunkid>/
myProject.files/<chunkid>/chunk.zip
myProject.files/<chunkid>/<frameid>/
myProject.files/<chunkid>/<frameid>/frame.zip
myProject.files/<chunkid>/<frameid>/thumbnails/
myProject.files/<chunkid>/<frameid>/thumbnails/thumbnails.zip
```

## Changelog
### v0.1.8
* fix bugs
* add better path support
* add utils
* add utils.duplicate_chunk
* add Project.delete and Project.document

### v0.1.5
* fix packaging issue

### v0.1.4
* add calibration support to Sensor
* add params support to Sensor
* add loading and saving for model and mesh data
* fix minor bugs

### v0.1.3
* add loading and saving for point cloud data
* add covariance support to Sensor
* fix minor bugs

### v0.1.2
* improve support for loading and saving thumbnails
* add loading and saving for camera transformations
* add loading and saving of bounding boxes
* add chunk transform, region and meta saving
* fix bugs

### v0.1.1
* improve support for loading project with multiple chunks and cameras
* improve support for loading models
* improve support for loading frames
* improve support for loading aligned photos

### v0.1.0
* initial release
