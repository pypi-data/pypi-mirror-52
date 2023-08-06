#coding: utf8
from __future__ import absolute_import
import re
import difflib
from .md_block import  get_md_blocks_info, get_wrap_html_for_section, wrap_normal_block_html_with_context
from .auto_fix import fix_content_before_compile
from ..compile_md import compile_markdown, TOC_MARKER, get_markdown_toc_html_content, replace_toc_marker


def get_wrapped_block_html(dom_id, block_text, blocks_info=None, path='/', root=None, for_local=False):
    block_text = block_text.strip('\n')
    block_html = compile_markdown(
        block_text,
        wrap_md_blocks = False,
        compute_md_blocks = False,
        compile_metadata = False,
        remove_h1 = False,
        do_after_job = False,
        path = path,
        root = root,
        for_local = for_local,
    )

    if blocks_info: # 构建上下文关系的 html
        block_html = wrap_normal_block_html_with_context(dom_id, block_html, blocks_info)

    wrapped_block_html = get_wrap_html_for_section(dom_id, block_html)
    return wrapped_block_html



def get_block_delta_list(new_block_ids, old_block_ids, new_block_ids_map=None, old_block_ids_map=None):
    # 要判断进一步获得其对应的 pre  next block_id 的逻辑
    new_block_ids_map = new_block_ids_map or {}
    old_block_ids_map = old_block_ids_map or {}
    diff = difflib.ndiff(old_block_ids, new_block_ids)
    pre_block_id = None
    index = 0
    block_delta_list = [] # delta data
    for diff_block_id in diff:
        block_id = re.sub(r'[\+\-\? ^]', '', diff_block_id).strip()
        if diff_block_id.startswith('-'):
            is_deleted = True # 意味着这条内容, 不是当前 list 中的
        else:
            is_deleted = False
        if diff_block_id.startswith('+'):
            is_added = True # 新增（或者是修改的）
        else:
            is_added = False
        # 要获得 block_id, 以及对应的 index ..

        #if diff_block_id.startswith('?'):
        #    pass # ignore
        #elif diff_block_id.startswith(' '): # 没有变化
        #    pass # ignore

        # 一般当前行的变化, 是 减去一个 old, 再 新增一个 new 的叠加逻辑

        if is_deleted:
            block_data = dict(
                action = 'delete',
                block_id = block_id,
                pre_block_id = pre_block_id,
                block = old_block_ids_map.get(block_id)
            )
            block_delta_list.append(block_data)
        elif is_added:
            block_data = dict(
                action = 'add',
                block_id = block_id,
                pre_block_id = pre_block_id,
                index = index,
                block = new_block_ids_map.get(block_id)
            )
            block_delta_list.append(block_data)

        if not is_deleted and block_id:
            # 意味着当前的 block_id, 实际上是当前 new_block_ids 中的
            # 获得对应的 pre_block_id & index
            index += 1
            pre_block_id = block_id

    return block_delta_list




def get_delta_md_blocks_info(new_content, old_content, pre_auto_fix=True):
    # content 要进行额外的 auto fix
    if pre_auto_fix:
        new_content = fix_content_before_compile(new_content)
        old_content = fix_content_before_compile(old_content)
    #with open('/Users/hepochen/Dev/QuanDuan/MacMarkEditor/tmp2.txt', 'wb')  as f:
        #f.write(old_content.encode('utf8'))
    new_blocks_info = get_md_blocks_info(new_content)
    old_blocks_info = get_md_blocks_info(old_content)
    new_block_ids_map = new_blocks_info['block_ids_map']
    new_block_ids = new_blocks_info['block_ids']
    old_block_ids_map = old_blocks_info['block_ids_map']
    old_block_ids = old_blocks_info['block_ids']

    block_delta_list = get_block_delta_list(new_block_ids, old_block_ids,
                                            new_block_ids_map = new_block_ids_map,
                                            old_block_ids_map = old_block_ids_map,

                                            )

    info = dict(
        new_blocks_info = new_blocks_info,
        old_blocks_info = old_blocks_info,
        new_block_ids = new_block_ids,
        old_block_ids = old_block_ids,
        block_delta_list = block_delta_list,
    )

    return info



def get_previewer_blocks_delta(new_content, old_content, path='/', root=None, for_local=False):
    # 为 previewer 提供一个 delta 的逻辑, 获得 doms_to_add & dom_ids_to_delete
    doms_to_add = []
    dom_ids_to_delete = []
    info = get_delta_md_blocks_info(new_content, old_content)
    new_blocks_info = info['new_blocks_info']
    block_delta_list = info['block_delta_list']
    toc_content = None
    for block_delta_data in block_delta_list:
        block = block_delta_data.get('block')
        block_id = block_delta_data.get('block_id')
        if not block or not block_id:
            continue
        pre_block_id = block_delta_data.get('pre_block_id', None)
        action = block_delta_data.get('action')
        if action == 'add':
            rng, block_type, block_text, _block_id = block
            if block_type in ['yaml_header', 'simple_header']:
                continue
                
            block_html = get_wrapped_block_html(block_id, block_text, new_blocks_info, path=path, root=root, for_local=for_local)

            # TOC 逻辑的更新
            if TOC_MARKER in block_html:
                if toc_content is None:
                    new_content_for_toc = fix_content_before_compile(new_content)
                    toc_content = get_markdown_toc_html_content(new_content_for_toc, old_markdown=False)
                block_html = replace_toc_marker(block_html, toc_content)

            doms_to_add.append([block_id, pre_block_id, block_html])
        elif action == 'delete':
            dom_ids_to_delete.append(block_id)
    info['doms_to_add'] = doms_to_add
    info['dom_ids_to_delete'] = dom_ids_to_delete
    return info

