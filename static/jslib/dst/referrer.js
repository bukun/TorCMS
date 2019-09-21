var args = {
    mySite: "http://127.0.0.1:8888/"  //修改为需要统计网址
};


//媒体
var media = "";
//媒体细分
var mediaSubdivide = "";
//终端,根据用户使用设备判断
var terminal = "";
//数据来源
var dataSource = document.referrer;

var userChannel = {
    //媒体
    Media: function (channelInfo) {
        channelInfo = channelInfo.toLowerCase();
        if (channelInfo.indexOf(args.mySite) >= 0) {
            //媒体  无法判断（如直接搜索）
            media = "站内跳转";  //媒体
            mediaSubdivide = "";       //媒体细分

            if (channelInfo.indexOf("zhihu") >= 0) {
                media = "知乎";
                mediaSubdivide = "";
            }
        } else if (channelInfo.indexOf("baidu.com") != -1) {
            media = "百度";                       //媒体
            if (channelInfo.indexOf('utm_medium=cpc') != -1) {
                mediaSubdivide = "sem";         //媒体细分
            } else if (channelInfo.indexOf('utm_medium=cpc') == -1) {
                mediaSubdivide = "seo";         //媒体细分
            } else {
                mediaSubdivide = "其它";      //媒体细分
            }
        } else if (channelInfo.indexOf('haosou.com') != -1 || channelInfo.indexOf('so.com') != -1) {
            media = "好搜";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf('sogou.com') != -1) {
            media = "搜狗";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf('sm.cn') != -1) {
            media = "神马";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf('bing.com') != -1) {
            media = "必应";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf('google.com') != -1) {
            media = "google";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf('douban.com') != -1) {
            media = "豆瓣";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        } else if (channelInfo.indexOf("zhihu.com") != -1) {
            media = "知乎";
            mediaSubdivide = "无法判断";
        }
        else if (channelInfo.indexOf("toutiao") != -1) {
            media = "今日头条";
            mediaSubdivide = "无法判断";
        }
        else {
            media = "来源不明";                       //媒体
            mediaSubdivide = "无法判断";        //媒体细分
        }

        var mediaInfo = new Array(media, mediaSubdivide);
        return mediaInfo;
    },
    //终端
    Terminal: function () {
        if ((navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i))) {
            terminal = "移动端";
            return terminal;
        } else {
            terminal = "PC端";
            return terminal;
        }
    }

};


var judgeMedia = userChannel.Media(dataSource);
var judgeTerminal = userChannel.Terminal();
var judgeip = returnCitySN["cip"];
var judgecity = returnCitySN["cname"];

// FormData 对象
var formData = new FormData();
formData.append("media", judgeMedia);    // 可以增加表单数据
formData.append("terminal", judgeTerminal);
formData.append("userip", judgeip);
formData.append("usercity", judgecity);

$.ajax({
    url: "/referrer/_add",
    type: "post",
    cache: false,
    data: formData,
    processData: false,
    contentType: false
});

