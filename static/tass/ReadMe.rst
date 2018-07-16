
说明
============

Install
------------

::

    gem install compass
    gem install bootstrap-sass

Ubunt 17.04:

::

    sudo apt install ruby-compass compass-bootstrap-sass-plugin

Note, there must be something wrong under Ubuntu 17.04. The following command should run first.

::

    sudo ln -s /usr/share/rubygems-integration/all/gems/bootstrap-sass-3.3.5.1/assets/stylesheets /usr/share/rubygems-integration/all/gems/bootstrap-sass-3.3.5.1/stylesheets



使用的时候，在 ``config.rb`` 中，写入：

::

    require "bootstrap-sass"

在样式文件中，

::

    //@import "bootstrap-sass"
    @import "bootstrap-compass"
    @import "bootstrap-variables"
    @import "bootstrap"

其中， ``bootstrap-variables`` ，没有，在 bootstrap-sass 项目中找。