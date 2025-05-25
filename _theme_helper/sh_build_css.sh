#
# ./node_modules/.bin/sass  style.scss:../static/css/osgeo.css

sudo apt install -y nodejs npm
npm install bootstrap sass

# 生成压缩的生产环境样式：
# ./node_modules/.bin/sass --style compressed style.scss:../static/css/torcms.css

# 修改过程动态
./node_modules/.bin/sass --watch style.scss:../static/css/torcms.css


