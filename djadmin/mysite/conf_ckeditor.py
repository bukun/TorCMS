CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'PIL'
# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono-lisa',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_Full': [
#             [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ],
#             [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],
#
#             [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ],
#             [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ],
#             '/',
#             [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ],
#             [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv', '-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
#             [ 'Link','Unlink','Anchor' ],
#             [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ],
#             '/',
#             [ 'Styles','Format','Font','FontSize' ] ,
#             [ 'TextColor','BGColor' ] ,
#             [ 'Maximize', 'ShowBlocks','-','About' ] ,
#             ['CodeSnippet'],  #代码段按钮
#
#         ],
#         'toolbar': 'Full',
#         'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),   #代码段插件
#     }
# }

CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '300px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            [
                'Source',
                '-',
                'Save',
                'NewPage',
                'DocProps',
                'Preview',
                'Print',
                '-',
                'Templates',
            ],
            # 格式、字体、大小
            ['Format', 'Font', 'FontSize'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 列表
            [
                'Image',
                'Table',
                'NumberedList',
                'BulletedList',
                'HorizontalRule',
                'Smiley',
                'SpecialChar',
                'PageBreak',
                'Iframe',
            ],
            [
                'Form',
                'Checkbox',
                'Radio',
                'TextField',
                'Textarea',
                'Select',
                'Button',
                'ImageButton',
                'HiddenField',
            ],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            # 链接
            ['Link', 'Unlink', 'Anchor'],
            # 预览、表情
            ['Preview', 'Smiley'],
            # 居左，居中，居右
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 最大化
            ['Maximize'],
            # ['CodeSnippet', 'Markdown'],  # 这个markdown插件默认没有，得额外下载。
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(
            ['codesnippet', 'image2', 'filebrowser', 'widget', 'lineutils']
        ),  # 'markdown'
    },
    # 评论
    'comment': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '140px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet']),
    },
}
