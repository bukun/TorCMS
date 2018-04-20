jQuery.extend(jQuery.validator.messages, {
required: "<span class='red'>必选字段</span>",
remote: "<span class='red'>请修正该字段</span>",
email: "<span class='red'>请输入正确格式的电子邮件</span>",
url: "<span class='red'>请输入合法的网址</span>",
date: "<span class='red'>请输入合法的日期</span>",
dateISO: "<span class='red'>请输入合法的日期 (ISO).</span>",
number: "<span class='red'>请输入合法的数字</span>",
digits: "<span class='red'>只能输入整数</span>",
creditcard: "<span class='red'>请输入合法的信用卡号</span>",
equalTo: "<span class='red'>请再次输入相同的值</span>",
accept: "<span class='red'>请输入拥有合法后缀名的字符串</span>",
maxlength: jQuery.validator.format("<span class='red'>请输入一个 长度最多是 {0} 的字符串</span>"),
minlength: jQuery.validator.format("<span class='red'>请输入一个 长度最少是 {0} 的字符串</span>"),
rangelength: jQuery.validator.format("<span class='red'>请输入 一个长度介于 {0} 和 {1} 之间的字符串</span>"),
range: jQuery.validator.format("<span class='red'>请输入一个介于 {0} 和 {1} 之间的值</span>"),
max: jQuery.validator.format("<span class='red'>请输入一个最大为{0} 的值</span>"),
min: jQuery.validator.format("<span class='red'>请输入一个最小为{0} 的值</span>")
});