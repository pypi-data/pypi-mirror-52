## The SDK interfaces is shown below:

1. `AnalyzeImages(imageIDList, edaFilterList)`: Analyze images depending on EDA metrics and will return the analyze result.
    - param `imageIDList`: a list of imageIDs(if None, means all images).
    - type `imageIDList`: `list`
    - param `edaFilterList`: a dict of eda filters{edaname: filtercondition}.
    - type `edaFilterList`: `dict`
    - return: the analyze result.
    - rtype: `ImageAnalyzeResult`


2. `AnalyzeImagesByBoundingBoxes(boxIDList, edaFilterList)`: Analyze bounding boxes depending on EDA metrics and will return the analyze result.
    - param `boxIDList`: a list of boxIDs(if None, means all bbox).
    - type `boxIDList`: `list`
    - param `edaFilterList`: a dict of eda filters{edaname: filtercondition}.
    - type `edaFilterList`: `dict`
    - return: the analyze result.
    - rtype: `ImageAnalyzeResult`


3. `SelectImages(imageIDList, boxIDList, edaFilterList)`: People can select images on different rules.
    - param `imageIDList`: a list of imageIDs(if None, means all images).
    - type `imageIDList`: `list`
    - param `boxIDList`: a list of boxIDs(if None, means all bbox).
    - type `boxIDList`: `list`
    - param `edaFilterList`: a dict of eda filters{edaname: filtercondition}.
    - type `edaFilterList`: dict`
    - return: a dict like {ImageID: [bboxID1, bboxID2,...]}.
    - rtype: `dict`


4. `SelectBboxs(boxIDList, edaFilterList)`: People can select bounding box on different rules.
    - param `boxIDList`: a list of boxIDs(if None, means all bbox).
    - type `boxIDList`: `list`
    - param `edaFilterList`: a dict of eda filters{edaname: filtercondition}.
    - type `edaFilterList`: `dict`
    - return: a boxID list of the query results.
    - rtype: `list`
    
    
5. `GetCategories()`: Return all categories.
    - return: a category list.
    - rtype: `list`
  
  
6. `ShowImages(path, imageIDList, boxIDList, limitedNum)`: Show bounding boxes in images and will download images with drawn bounding boxes to local path. 
    - param `path`: local save path.
    - type `path`: `str`
    - param `imageIDList`: a list of imageIDs(if None, select image id by boxIDList).
    - type `imageIDList`: `list`
    - param `boxIDList`: a list of boxIDs(if None, means all bbox).
    - type `boxIDList`: `list`
    - param `limitedNum`: the download image number.
    - type `limitedNum`: `int`
 
 
7. `GetImages(path, imageDict)`: Download images (named by image ids) and a image attribute file (imageid, categorylist, bb-info-list) into local path.
    - param `path`: download path.
    - type `path`: `str`
    - param `imageDict`: a dict like {ImageID: [bboxID1, bboxID2,...]}.
    - type `imageDict`: `dict`

## edaFilterList

The edaFilterList is a dict of eda filters like `{edaname: filtercondition}`,the edaname must be `str` and the filtercondition must be `list`.

There are three types of edaname:

- numericSelection: the element of the corresponding filtercondition must be `int` or `tuple` with len=2
- categorySelection: the element of the corresponding filtercondition must be `str`
- boolSelection: the element of the corresponding filtercondition must be `bool`
- edaname supported in image:
    - numericSelection: `LuminanceMean`, `LuminanceStd`, `Width`, `Height`, `Area`, `BoxNumberPerImage`
    - categorySelection: `Mode`(RGB or L), `Category`
    - example: `{'Category': ['candy', 'ball'], 'Mode': ['RGB'], 'BoxNumberPerImage': [(0,100), 123], 'Height': [(0,100), 1024]}`
- edaname supported in bounding box:
    - numericSelection: `LuminanceMean`, `LuminanceStd`, `Width`, `Height`, `Area`
    - categorySelection: `Category`
    - boolSelection:
        - `IsOccluded`: Indicates that the object is occluded by another object in the image.
        - `IsTruncated`: Indicates that the object extends beyond the boundary of the image.
        - `IsGroupOf`: Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). 
        - `IsDepiction`: Indicates that the object is a depiction (e.g., a cartoon or drawing of the object, not a real physical instance).
        - `IsInside`: Indicates a picture taken from the inside of the object (e.g., a car interior or inside of a building).
    - example: `{'Category': ['cat'], 'IsOccluded': [True], 'IsTruncated': [True], 'Width': [(0, 800), 1024]}`