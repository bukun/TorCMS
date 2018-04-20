var ad_divs = $obj('ad_none').getElementsByTagName('div');
var ad_obj = null;

for (var i = 0; i < ad_divs.length; i++) {
    if (ad_divs[i].id.substr(0, 3) == 'ad_' && (ad_obj = $obj(ad_divs[i].id.substr(0, ad_divs[i].id.length - 5))) && ad_divs[i].innerHTML) {
        ad_obj.innerHTML = ad_divs[i].innerHTML;
        ad_obj.className = ad_divs[i].className;
    }
}


