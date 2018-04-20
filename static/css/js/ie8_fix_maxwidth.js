/**
 * IE8 max-width bug: a generic fix for images
 * ===========================================
 * 
 * When the size of a replaced element is controlled by CSS rules for width and
 * max-width, the browser has to rescale the element. Ie, it has to adjust both
 * width and height according to the intrinsic aspect ratio of the element.
 * 
 * IE8 does not rescale replaced elements correctly when a max-width limit is
 * binding.
 * 
 * This script uses jQuery to fix the problem for the most affected element
 * type, images. It corrects the height of the affected images by setting an
 * appropriate max-height.
 * 
 * ## Usage:
 * 
 * Usage is simple. Put a conditional comment targeting IE8 in your page source.
 * Within it, load a copy of the jQuery library if it isn't available already,
 * then load this script. That's all there is to it.
 * 

 *
 * ## Dependencies:
 *
 * jQuery 1.6.1 or newer. Will also work with older versions - ymmv.
 *
 * (The test suite requires jQuery >= 1.6.1, so the script is not unit tested
 * with older versions.)
 * 
 * ## Limitations:
 *
 * None, AFAICT, with regard to IE8. Note that the script will cause distortions
 * in IE6, 7 and 9 if it is not enclosed in a conditional comment targeting IE8.
 * (These distortions could be avoided, but at a computational cost. Use the
 * comment.)
 *
 * See the test suite for currently supported scenarios:
 * http://www.zeilenwechsel.de/it/code/get/ie8-max-width-fix/tests/ie8_fix_maxwidth.html
 *
 * ## Other:
 * 
 * Tested with jQuery 1.6.1, 1.6.2
 *
 * @author  Michael Heim, http://www.zeilenwechsel.de/
 * @license MIT, http://www.opensource.org/licenses/mit-license.php
 * @version 0.3.0, 13 July 2011
 */

$( function() {
    
    // Make sure the browser features we access are indeed there. This will
    // exclude non-IE browsers if the script is run outside of conditional
    // comments.
    if ( ! (
            document.documentElement
         && document.documentElement.currentStyle
         && document.documentElement.runtimeStyle
    ) ) {
        return;
    }
    
    /**
     * Callback function setting max-height for an image tag. It is calculated
     * from max-width and the intrinsic aspect ratio of the image.
     * 
     * @param   {element} imgElement  the image DOM node
     * @returns {void}
     */
    var fixImage = function ( imgElement ) {
        
        // Working out the aspect ratio.
        
        // First, we get the height as rendered by IE8: scaled in proportion
        // to 'width', while ignoring 'max-width'.
        var image = $( imgElement ),
            height = image.height(),
        
        // Next, we need the corresponding value for width: using 'width',
        // ignoring 'max-width'. But image.width() returns the result as
        // rendered, ie respecting the max-width directive.
        //
        // Instead we use a hack from a previous version of jQuery (lifted
        // from curCSS in jQuery 1.3.2), which was in turn inspired by
        // http://erik.eae.net/archives/2007/07/27/18.54.15/#comment-102291.
        // 
        // There, the hack was used for getting a computed style in IE. Here
        // it will return the pixel equivalent of the width rule, regardless
        // of the real width of the image (which may be constrained by
        // max-width).
        
            width = imgElement.currentStyle.width;
        if ( /^[\d.]+(px)?$/i.test( width ) ) {
            
            // We already have a pixel value for width: a number without a
            // unit, or a px string. Just remove the 'px' suffix.
            width = parseInt( width, 10 );
            
        } else if ( /^\d/.test( width ) ) {
            
            // We have a number with a different unit. Convert it to a
            // value in pixels.
            
            // Remember the original values for the styles we have to
            // manipulate
            var left   = imgElement.style.left;
            var rsLeft = imgElement.runtimeStyle.left;
            
            // Put in the right values to get a computed value out
            imgElement.runtimeStyle.left = imgElement.currentStyle.left;
            imgElement.style.left = width || 0;
            width = imgElement.style.pixelLeft;
            
            // Revert the changed values
            imgElement.style.left = left;
            imgElement.runtimeStyle.left = rsLeft;
            
        }
        
        if ( width && height ) {
            
            // Calculate and apply max-height, using the aspect ratio.
            var ratio = height / width,
                maxwidth = image.css( 'max-width' ),
                           // will return px in current jQuery versions
                maxheight = Math.round( parseFloat( maxwidth ) * ratio )
                          + maxwidth.match( /[\d.]+([^\d.]*)$/ )[1];
                            // ... the regex returns the unit. (Could be
                            // simplified, but this is more likely to work in
                            // older jQuery versions.)
            
            image.css( 'max-height', maxheight );
            
            // max-width in percent:
            // max-height is fixed in px. The value must be readjusted every
            // time the actual image width changes.
            if ( /[\d.]+%/.test( imgElement.currentStyle.maxWidth ) ) {
                
                image.resize( function () {
                    
                    maxwidth = image.css( 'max-width' );
                    maxheight = Math.round( parseFloat( maxwidth ) * ratio )
                              + maxwidth.match( /[\d.]+([^\d.]*)$/ )[1];
                    image.css( 'max-height', maxheight );
                    
                } );
                
            }
        }
        
    };
    
    $( 'img' )
    .filter( function () {
        
        // Reduce the set to affected images only. These have width and
        // max-width specified in a CSS rule, but max-height is not set.
        
        var isAffected = (                          
            this.currentStyle.width     !== 'auto'     // 'auto' works without fix
         && this.currentStyle.width     !== 'inherit'  // 'inherit' works without fix
         && this.currentStyle.height    === 'auto'     // explicit height doesn't need fix
         && this.currentStyle.maxWidth  !== 'none'     // max-width must be defined
         && this.currentStyle.maxHeight === 'none'     // explicit max-height doesn't need fix
        );
        
        return ( isAffected );
        
    } )
    .each( function () {
        
        // In order to determine the intrinsic aspect ratio, we need to look at
        // the actual image. In other words, it needs to be fully loaded. So
        // let's wait.
        
        $( this ).load( function () {
            
            fixImage( this );
            
        } );
        
        // If the image is already in the cache, the onload event will have
        // fired long before the event handler was set up. We need to call the
        // handler manually.
        if ( this.complete ) fixImage( this );
        
    } );
    
} ); 

