xgettext --language=Python --from-code=utf-8 --keyword=_:1,2 -d pycate  ../../templates/*/*.html ../../templates/*/*/*.html

cp pycate_zh.po old_zh.po
cp pycate_zh.po bak_zh.po

cp pycate_en.po old_en.po
cp pycate_en.po bak_en.po

msgmerge  old_zh.po pycate.po  > pycate_zh.po
msgmerge  old_en.po pycate.po  > pycate_en.po

rm -f old_en.po old_zh.po

# msgfmt pycate_en.po -o ../../locale/en_US/LC_MESSAGES/pycate.mo
# msgfmt pycate_en.po -o ../../locale/zh_CN/LC_MESSAGES/pycate.mo

msgfmt pycate_zh.po -o ../../locale/en_US/LC_MESSAGES/pycate.mo
msgfmt pycate_zh.po -o ../../locale/zh_CN/LC_MESSAGES/pycate.mo

