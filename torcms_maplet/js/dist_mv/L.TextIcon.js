var testDiv = document.createElement('div')
testDiv.style.position = 'absolute'
testDiv.style.visibility = 'hidden'
testDiv.setAttribute('id', 'testDiv')
document.body.appendChild(testDiv)

L.TextIcon = L.DivIcon.extend({
  defaultIcon: 'text',
  options: {
    marker: 'text',
    color: '#000',
    size: 16,
    icon: null,
    borderRadius: null,
    text: null,
    textMaxSize: 20,
    active: false,
    // boxShadow: true,
    borderWidth: 2,
    padding: 3
  },
  initialize: function (options) {
    // L.setOptions(this, options);

    options = L.extend({}, this.options, options);

    var text = options.text || options.name || "New layer",
      icon = options.icon || "",
      size = options.size,
      color = options.color, width, height, background, lineHeight, marginLeft, marginTop,
      borderRadius, boxShadow;

    switch (options.marker) {
      case "text":
        icon = "";
        break;
      case "icon":
        text = "";
        break;
      case "mix":
        icon = options.icon || this.defaultIcon;
        break;
    }

    if (text == "" && icon == "") {
      icon = 'star';
    }

    if (text) {
      text = this.truncateChars(text, options.textMaxSize);
      width = this.getWidth(text, size);
      height = lineHeight = size;
      marginTop = -height / 2 + 6;
      background = '';
      boxShadow = '';
      //style.push('text-shadow: 1px 1px 1px #333;');
      if (icon) {
        width = size + this.getWidth(options.text || options.name, size);
        marginLeft = -size / 2 + 6;
        icon = '<i class="text-and-icon icon iconfont icon-' + options.icon + '"></i>'
      } else {
        marginLeft = -width / 2 + 6;
      }
    } else {
      var i = parseInt(size * 1.5);
      i = i % 2 == 0 ? i : i + 1;

      borderRadius = size;
      lineHeight = width = height = i;
      background = color;
      color = this.contrastColor(color);
      icon = '<i class="icon iconfont icon-' + icon + '"></i>';
      marginTop = marginLeft = -(width / 2 - 6);
      boxShadow = '1px 1px 1px #666666';
    }

    var css = {
      'width': width + 'px',
      'height': height + 'px',
      'color': color,
      'font-size': size + 'px',
      'line-height': lineHeight + 'px',
      'margin-left': marginLeft + 'px',
      'margin-top': marginTop + 'px',
      'background-color': background,
      'border-radius': borderRadius + 'px',
      'box-shadow': boxShadow,
      'text-shadow': text ? '1px 1px 1px {color}'.replace(
        '{color}', this.contrastColor(color)
      ) : ""
    };

    if (options.active == true) {
      var offset = options.borderWidth * 2 + options.padding * 2;
      L.extend(css, {
        'width': width += offset,
        'height': height += offset,
        'margin-left': marginLeft -= offset / 2,
        'margin-top': marginTop -= offset / 2,
        'padding': options.padding + 'px',
        'border': options.borderWidth + 'px dashed ' + color,
        'border-radius': height
        // 'box-shadow': '1px 1px 1px #666666'
      });
    }

    var div = document.createElement('div')
    div.innerHTML = icon + text
    for (var key in css){
      console.log(key, css[key])
      div.style.setProperty(key, css[key])
    }

    options.html = div.outerHTML;
    options.className = 'leaflet-text-icon';
    options.popupAnchor = [0, -size / 2];

    L.DivIcon.prototype.initialize.call(this, options);
  },
  onAdd: function (map) {
    L.DivIcon.prototype.onAdd.call(this, map);
  },
  contrastColor: function (color) {
    var r = parseInt(color.slice(1, 3), 16),
      g = parseInt(color.slice(3, 5), 16),
      b = parseInt(color.slice(5, 7), 16);

    if (r + g + b > 475 || r + g > 400 || r + b > 400 || g + b > 450) {
      return '#000000'
    } else {
      return '#ffffff'
    }
  },
  truncateChars: function (string, maxLength) {
    if (this.getLength(string) > maxLength) {
      var i = 0, len = string.length, getLength = 0, result = "";
      for (; i < len; i++) {
        if (maxLength <= 0) {
          break
        }
        var charCode = string.charCodeAt(i);
        result += string[i];
        if (charCode >= 0 && charCode <= 128) {
          maxLength -= 0.5
        } else {
          maxLength -= 1
        }
      }
      return result + '...'
    } else {
      return string.toString()
    }
  },
  getLength: function (string) {
    var i = 0, len = string.length, getLength = 0;
    for (; i < len; i++) {
      var charCode = string.charCodeAt(i);
      if (charCode >= 0 && charCode <= 128) {
        getLength += 0.5
      } else {
        getLength++
      }
    }
    return getLength;
  },
  getWidth: function (string, size) {
    var div = document.getElementById('testDiv')
    div.style.fontSize = size + 'px'
    div.innerHTML = string
    return div.offsetWidth
  }
})
;

L.textIcon = function (options) {
  return new L.TextIcon(options);
};
