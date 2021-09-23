#!/usr/bin/env python

"""
Uncompressed javascript. Just for better code reading and understanding.

function getElement(locator) {
    return window.document.evaluate(locator,
        window.document.documentElement, null,
        XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotItem(0);
}

---- Simulate 'onmouseover' and 'onclick' events. ----
function eventFire(el, event_type){
    if (el.fireEvent) {
        el.fireEvent('on' + event_type);
    } else {
        var eventObj = document.createEvent('Events');
        eventObj.initEvent(event_type, true, false);
        el.dispatchEvent(eventObj);
    }
}

// Example
var el = getElement("some_locator");
eventFire(el,'mouseover');
el.click();

---- Simulate 'selected' and 'onclick' events. ----
function selectItemIndexByValue(el, expr) {
    var regexp = new RegExp("^"+expr+"*", "i");
    for(var i=0; i<el.options.length; i++) {
        if (el.options[i].text.match(regexp)) {
            el.selectedIndex = i;
            break;
        }
    }
}

// Example
var el = getElement("//*[@id='size_condition']");
selectItemIndexByValue(el, 'less');
el.click();
"""

# minified js
eventFireCompressed = """function eventFire(el,event_type){if(el.fireEvent){el.fireEvent('on'+event_type)}else{var eventObj=document.createEvent('Events');eventObj.initEvent(event_type,true,false);el.dispatchEvent(eventObj)}}"""
getElementCompressed = """function getElement(locator){return window.document.evaluate(locator,window.document.documentElement,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null).snapshotItem(0)}"""
selectItemIndexByValueCompressed = """function selectItemIndexByValue(el, expr){var regexp=new RegExp("^"+expr+"*","i");for(var i=0;i<el.options.length;i++){if(el.options[i].text.match(regexp)){el.selectedIndex=i;break}}}"""

def SimulateEventAndClickOnElement(locator, event):
    el = """var el = getElement("%s");""" % locator
    event = "eventFire(el,'%s');" % event
    el_click = "el.click()"
    return "%s %s %s %s %s" % (eventFireCompressed, getElementCompressed, el, event, el_click)

def SimulateSelectEventAndClickOnElement(locator, item):
    el = """var el = getElement("%s");""" % locator
    event1 = "eventFire(el,'click');"
    event2 = "selectItemIndexByValue(el, '%s');" % item
    el_click = "(el.onclick || el.click || function() {})();"
    return "%s %s %s %s %s %s %s" % (eventFireCompressed, selectItemIndexByValueCompressed, getElementCompressed, el, event1, event2, el_click)
