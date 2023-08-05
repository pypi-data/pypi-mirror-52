# Publitio Python SDK

Installation:

```bash
pip3 install publitio
```

This SDK works for Python 3.6 and up.

To use the Python SDK:

```python
from publitio import PublitioAPI
publitio_api = PublitioAPI(key='<API key>', secret='<API secret>')
```

For the remaining code samples, these two lines of code will be implied.

The methods used for communicating with the api - `create_file`, `list_files` etc., all return parsed json responses, as if `json.loads` was used on the response content. The only exception to this is the `transformed` method, which returns `bytes`. In all methods, the supported keyword parameters are exactly the same as in the [publitio docs](https://publit.io/docs). You should probably look into that documentation before reading this.

## Exceptions

- `UnknownStatusCode` - raised when the server responds to a request with an unknown status code.
- `TransformationFailed` - raised when the server fails to perform a transformation, i.e. when `publitio_api.transformed` fails.
- `BadJSON` - raised when the server responds with invalid JSON. This may be due to an internal server error.

## Transforming files

```python
publitio_api.transformed('filename.jpeg', extension='png', w=300, h=300)
# If you don't wish to change the extension, you can omit it:
publitio_api.transformed('filename.jpeg', w=300, h=300)
```

This would return the `bytes` of the file named `filename`, now transcoded into a PNG, with dimensions 300x300. The `extension` parameter is optional. The supported parameters are the same as [here](https://publit.io/docs/#url-based-transformations). For example, the above invocation makes a call to this URL:

```url
https://media.publit.io/file/w_300,h_300/filename.png
```

## Documentation

You can view documentation from the source code docstrings using `pydoc`:

```bash
pydoc3 publitio
```

## Creating files

```python
publitio_api.create_file(file=open('path/to/file', 'rb'),
                         title='My title',
                         description='My description')

```

Please do note that the file must be opened for binary reading. **The `publitio_api.create_file` function will not close the file**. Therefore, what you will probably want to do most of the time is:

```python
with open('path/to/file', 'rb') as f:
    publitio_api.create_file(file=f,
                             title='My title',
                             description='My description')
```

If you wish to upload the file from a remote URL, pass the `file_url` keyword parameter instead of
the optional file parameter. For example:

```python
publitio_api.create_file(file_url='https://example.com/image.png',
                         title='My title',
                         description='My description')
```

## Listing files

```python
publitio_api.list_files(offset=1)
```

It's also OK to provide strings as parameters when numbers seem logical. So, also valid:

```python
publitio_api.list_files(offset='1')
```

## Showing files

```python
publitio_api.show_file(file_id)
```

## Updating files

```python
publitio_api.update_file(file_id, title='A better title')
```

## Deleting files

```python
publitio_api.delete_file(file_id)
```

## Getting a file player

```python
publitio_api.get_file_player(file_id, player='myplayerid')
```

## Creating file versions

```python
publitio_api.create_version(file_id, extension='webm')
```

## Listing versions

```python
publitio_api.list_versions(file_id, limit=3)  # Or limit='3'
```

## Showing versions

```python
publitio_api.show_version(version_id)
```

## Updating versions

```python
publitio_api.update_version(version_id)
```

## Reconverting versions

```python
publitio_api.reconvert_version(version_id)
```

## Deleting versions

```python
publitio_api.delete_version(version_id)
```

## Creating folders

```python
publitio_api.create_folder(name='myfolder')
```

## Listing folders

```python
publitio_api.list_folders(limit=10, order='name')
```

## Showing folders

```python
publitio_api.show_folder(folder_id)
```

## Updating folders

```python
publitio_api.update_folder(folder_id, name='mynewname')
```

## Deleting folders

```python
publitio_api.delete_folder(folder_id)
```

## Folders tree

```python
publitio_api.folders_tree()
```

## Creating players

```python
publitio_api.create_player(name='whatever')
```

## Listing players

```python
publitio_api.list_players()
```

## Showing players

```python
publitio_api.show_player(player_id)
```

## Updating players

```python
publitio_api.update_player(player_id, skin='green')
```

## Deleting players

```python
publitio_api.delete_player(player_id)
```

## Creating adtags

```python
publitio_api.create_adtag(name='name', tag='tag')
```

## Listing adtags

```python
publitio_api.list_adtags()
```

## Showing adtags

```python
publitio_api.show_adtag(adtag_id)
```

## Updating adtags

```python
publitio_api.update_adtag(adtag_id, tag='newtag')
```

## Deleting adtags

```python
publitio_api.delete_adtag(adtag_id)
```

## Creating a watermark

```python
publitio_api.create_watermark(self, file=open('path/to/file', 'rb'), title='whatever')
```

Again, the file needs to be opened for binary reading. This function will not close the file.

## Listing watermarks

```python
publitio_api.list_watermarks()
```

## Showing watermarks

```python
publitio_api.show_watermark(watermark_id)
```

## Updating watermarks

```python
publitio_api.update_watermark(watermark_id, position='left')
```

## Deleting watermarks

```python
publitio_api.delete_watermark(watermark_id)
```
