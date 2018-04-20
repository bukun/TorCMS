
说明
============

Install
------------

::

    gem install compass
    gem install bootstrap-sass

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