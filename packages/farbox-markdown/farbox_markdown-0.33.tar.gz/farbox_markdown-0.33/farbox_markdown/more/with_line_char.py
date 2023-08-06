#coding: utf8
from __future__ import absolute_import
import re
from ..compile_md import rreplace, smart_unicode, extract_metadata

line_char = u'\uffff'

def add_line_char_for_markdown_content(raw_content):
    raw_content = smart_unicode(raw_content)
    body, metadata = extract_metadata(raw_content)
    lines = raw_content.split('\n')
    new_lines = []
    line_numbers = [] # 添加了空字符的 行list

    length_used = 0
    metadata_length = len(raw_content.rstrip()) - len(body)
    for line_number, line in enumerate(lines):
        # 实质性的空行, 是不处理的; 而实质性的空行必须要处理, 以保证整体的连续性
        length_used += len(line)+1
        mark_line = True
        line_strip = line.strip()
        if length_used <= metadata_length:
            mark_line = False
        elif not line_strip:
            mark_line = False
        elif '```' in line:
            mark_line = False
        elif line_strip == '$$': # 数学公式的块状
            mark_line = False
        elif line_strip.startswith('<!--/'): # div-block
            mark_line = False
        elif line.startswith('// ') or line.startswith('/// '): # 注释
            mark_line = False
        elif re.match('\[[^\[\]]+?\]:', line):
            mark_line = False
        elif not line.strip(' -'):
            mark_line = False
        elif line.startswith('>') and not line[1:].strip(): # 引用, 空行
            mark_line = False
        elif line_strip.startswith('|') and line_strip.endswith('|') and line_strip.count('|') >= 3:
            # markdown 通用表格
            mark_line = False
            if re.sub(r'[|\-:]', '', line_strip).strip():
                line = rreplace(line, '|', '%s|'%line_char)
                line_numbers.append(line_number)
        elif re.match('(:?-{2,}:? +\| *)+:?-{2,}:?\s*$', line_strip):
            # markdown 通用表格2
            mark_line = False
        elif re.match(r'\[[^\[\]]+\]:', line_strip):
            # [xxx]: xxx 这种link的形式, 最终并不会形成真实的内容
            mark_line = False
        elif re.match(r'</?[a-z][a-z0-9]+[^<>]*?>(.*?</[a-z][a-z0-9]+>)?$', line_strip, flags=re.I): # 整行属于 html 片段
            mark_line = False
        else:
            line_lower = line.lower()
            if line_lower in ['[page]']:
                mark_line = False
        if mark_line:
            line += line_char
            line_numbers.append(line_number)
        new_lines.append(line)

    new_raw_content = '\n'.join(new_lines)
    return new_raw_content, line_numbers
