from application import APP_URLS
from torcms.handlers.post_handler import PostHandler

def test_a():
    for item in APP_URLS:
        if '.PostHandler' in str(item[1]):
            print(item[0], str(item[1]) , item[2])
        elif '.MapPostHandler' in str(item[1]):
            print(item[0], str(item[1]), item[2])
        assert len(item) == 3
        assert item[0] != ''
def test_post_url():
    for item in APP_URLS:
        if item[0].startswith('/post/(.*)'):
            assert item[1] == PostHandler
            assert '.PostHandler' in str(item[1])
            assert item[2].get('kind') == '1'
def test_info_url():
    for item in APP_URLS:
        if item[0].startswith('/info/(.*)'):
            # assert item[1] == PostHandler
            assert '.PostHandler' in str(item[1])
            assert item[2].get('kind') == '3'
            assert item[2].get('filter_view') == True

