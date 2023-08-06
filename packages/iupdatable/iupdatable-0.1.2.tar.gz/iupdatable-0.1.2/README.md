IUpdatable
=======================

封装常用函数


Installation
-----

```bash
pip install iupdatable
```

```bash
pip install --upgrade iupdatable
```

函数
-----

### File
- read： 读取文件
- write： 写入文件
- append：追加写入文件
- append_new_line：新建一行，然后追加写入文件
- read_lines： 按行一次性读取文件
- write_lines：按行一次性写入文件
- write_csv：写入CSV文件
- read_csv：读取CSV文件
- exist_within_extensions: 检查一个文件是否存在（在指定的几种格式中）
- get_file_path_within_extensions: 获取一个文件的路径（在指定的几种格式中）

### Base64
- encode：base64编码
- decode：base64解码
- encode_multilines：base64多行解码
- decode_multilines：base64多行解码

License
-------
MIT