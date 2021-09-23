# robot import
#from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
import re
import time

from robot.utils import timestr_to_secs

# selenium import
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from SeleniumLibrary.locators import ElementFinder
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from SeleniumLibrary import SeleniumLibrary, __version__

from common.gui.wait import Wait
try:
    from exceptions import AttributeError
except ImportError:
    pass

# sarf import
from common.logging import Logger
from common.gui.guiexceptions import GuiLoginFailureError, InvalidUrlPathError
from common.ngui.exceptions import DataNotFoundError
from common.util.misc import Misc


js_wait_for_angular = """
    var waiting = true;
    var callback = function () {waiting = false;}
    var el = document.querySelector(arguments[0]);
    if (!el) {
      throw new Error('Unable to find root selector using "' +
                      arguments[0] +
                      '". Please refer to the AngularJS library documentation' +
                      ' for more information on how to resolve this error.')
    }
    if (window.angular && !(window.angular.version &&
          window.angular.version.major > 1)) {
      /* ng1 */
      angular.element(el).injector().get('$browser').
          notifyWhenNoOutstandingRequests(callback);
    } else if (window.getAngularTestability) {
      return !window.getAngularTestability(el).isStable(callback);
    } else if (window.getAllAngularTestabilities) {
      throw new Error('AngularJSLibrary does not currently handle ' +
          'window.getAllAngularTestabilities. It does work on sites supporting ' +
          'window.getAngularTestability. If you require this functionality, please ' +
          'the library authors or reach out to the Robot Framework Users Group.');
    } else if (!window.angular) {
      throw new Error('window.angular is undefined.  This could be either ' +
          'because this is a non-angular page or because your test involves ' +
          'client-side navigation. Currently the AngularJS Library is not ' +
          'designed to wait in such situations. Instead you should explicitly ' +
          'call the "Wait For Angular" keyword.');
    } else if (window.angular.version >= 2) {
      throw new Error('You appear to be using angular, but window.' +
          'getAngularTestability was never set.  This may be due to bad ' +
          'obfuscation.');
    } else {
      throw new Error('Cannot get testability API for unknown angular ' +
          'version "' + window.angular.version + '"');
    }
    return waiting;
"""

#
# js_get_pending_http_requests="""
# var el = document.querySelector('[ng-app]');
# var $injector = angular.element(el).injector();
# var $http = $injector.get('$http');
# return $http.pendingRequests;
# """

js_repeater_min = """
var rootSelector=null;function byRepeaterInner(b){var a="by."+(b?"exactR":"r")+"epeater";return function(c){return{getElements:function(d){return findAllRepeaterRows(c,b,d)},row:function(d){return{getElements:function(e){return findRepeaterRows(c,b,d,e)},column:function(e){return{getElements:function(f){return findRepeaterElement(c,b,d,e,f,rootSelector)}}}}},column:function(d){return{getElements:function(e){return findRepeaterColumn(c,b,d,e,rootSelector)},row:function(e){return{getElements:function(f){return findRepeaterElement(c,b,e,d,f,rootSelector)}}}}}}}}repeater=byRepeaterInner(false);exactRepeater=byRepeaterInner(true);function repeaterMatch(a,b,c){if(c){return a.split(" track by ")[0].split(" as ")[0].split("|")[0].split("=")[0].trim()==b}else{return a.indexOf(b)!=-1}}function findRepeaterRows(k,e,g,l){l=l||document;var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]];var o=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){o.push(n[c])}}}var f=[];for(var a=0;a<d.length;++a){var h=d[a]+"repeat-start";var n=l.querySelectorAll("["+h+"]");h=h.replace(arguments[0]);for(var c=0;c<n.length;++c){if(repeaterMatch(n[c].getAttribute(h),k,e)){var b=n[c];var m=[];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,k)){if(b.nodeType==1){m.push(b)}b=b.nextSibling}f.push(m)}}}var m=o[g]||[],j=f[g]||[];return[].concat(m,j)}function findAllRepeaterRows(g,e,h){h=h||document;var k=[];var d=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var a=0;a<d.length;++a){var f=d[a]+"repeat";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){k.push(j[c])}}}for(var a=0;a<d.length;++a){var f=d[a]+"repeat-start";var j=h.querySelectorAll("["+f+"]");f=f.replace(arguments[0]);for(var c=0;c<j.length;++c){if(repeaterMatch(j[c].getAttribute(f),g,e)){var b=j[c];while(b.nodeType!=8||!repeaterMatch(b.nodeValue,g)){if(b.nodeType==1){k.push(b)}b=b.nextSibling}}}}return k}function findRepeaterElement(a,b,g,r,q,w){var c=[];var t=document.querySelector(w||"body");q=q||document;var l=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var n=0;n<x.length;++n){var s=x[n]+"repeat";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){l.push(o[v])}}}var m=[];for(var n=0;n<x.length;++n){var s=x[n]+"repeat-start";var o=q.querySelectorAll("["+s+"]");s=s.replace(arguments[0]);for(var v=0;v<o.length;++v){if(repeaterMatch(o[v].getAttribute(s),a,b)){var y=o[v];var f=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){f.push(y)}y=y.nextSibling}m.push(f)}}}var f=l[g];var z=m[g];var A=[];if(f){if(f.className.indexOf("ng-binding")!=-1){A.push(f)}var k=f.getElementsByClassName("ng-binding");for(var v=0;v<k.length;++v){A.push(k[v])}}if(z){for(var v=0;v<z.length;++v){var e=z[v];if(e.className.indexOf("ng-binding")!=-1){A.push(e)}var k=e.getElementsByClassName("ng-binding");for(var u=0;u<k.length;++u){A.push(k[u])}}}for(var v=0;v<A.length;++v){var h=angular.element(A[v]).data("$binding");if(h){var d=h.exp||h[0].exp||h;if(d.indexOf(r)!=-1){c.push(A[v])}}}return c}function findRepeaterColumn(a,b,q,o,w){var c=[];var s=document.querySelector(w||"body");o=o||document;var h=[];var x=["ng-","ng_","data-ng-","x-ng-",arguments[1]];for(var m=0;m<x.length;++m){var r=x[m]+"repeat";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){h.push(n[v])}}}var l=[];for(var m=0;m<x.length;++m){var r=x[m]+"repeat-start";var n=o.querySelectorAll("["+r+"]");r=r.replace(arguments[0]);for(var v=0;v<n.length;++v){if(repeaterMatch(n[v].getAttribute(r),a,b)){var y=n[v];var e=[];while(y.nodeType!=8||(y.nodeValue&&!repeaterMatch(y.nodeValue,a))){if(y.nodeType==1){e.push(y)}y=y.nextSibling}l.push(e)}}}var z=[];for(var v=0;v<h.length;++v){if(h[v].className.indexOf("ng-binding")!=-1){z.push(h[v])}var g=h[v].getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}for(var v=0;v<l.length;++v){for(var u=0;u<l[v].length;++u){var y=l[v][u];if(y.className.indexOf("ng-binding")!=-1){z.push(y)}var g=y.getElementsByClassName("ng-binding");for(var t=0;t<g.length;++t){z.push(g[t])}}}for(var u=0;u<z.length;++u){var f=angular.element(z[u]).data("$binding");if(f){var d=f.exp||f[0].exp||f;if(d.indexOf(q)!=-1){c.push(z[u])}}}return c};"""

arg0 = "/\\/g,\"\""
arg1 = "ng\\:"


def stripcurly(binding):
    """ Starting with AngularJS 1.3 the interpolation brackets are not allowed
    in the binding description string. As such the AngularJSLibrary strips them
    out before calling the _find_by_binding method.

    See http://www.protractortest.org/#/api?view=ProtractorBy.prototype.binding
    """
    if binding.startswith('{{'):
        binding = binding[2:]

    if binding.endswith('}}'):
        binding = binding[:-2]

    return binding


def is_boolean(item):
    return isinstance(item, bool)


def get_driver_obj(lib):
    try:
        driver_obj = lib._current_browser()
    except AttributeError:
        driver_obj = lib.driver

    return driver_obj


#
# class ngElementFinder(ElementFinder):
#     def __init__(self, root_selector, ignore_implicit_angular_wait=False, _s2l=SeleniumLibrary()):
#         super(ngElementFinder, self).__init__()
#         self.root_selector = root_selector
#         self.ignore_implicit_angular_wait = ignore_implicit_angular_wait

# def find(self, locator, tag=None, first_only=True, required=True,
#          parent=None):
#     timeout = self._s2l.get_selenium_timeout()
#     timeout = timestr_to_secs(timeout)
#
#     if not self.ignore_implicit_angular_wait:
#         try:
#             WebDriverWait(self._sldriver, timeout, 0.2)\
#                 .until_not(lambda x: self._sldriver.execute_script(js_wait_for_angular, self.root_selector))
#         except TimeoutException:
#             pass
#     elements = ElementFinder.find(self, locator, tag, first_only, required, parent)
#     print ("Elements in find", elements)
#     return elements
#
# def _find_by_default(self, criteria, tag, constraints, parent):
#     if criteria.startswith('{{'):
#         criteria = stripcurly(criteria)
#         return self._find_by_binding(criteria, tag, constraints, parent)
#     else:
#         return ElementFinder._find_by_default(self, criteria, tag, constraints, parent)
#
# def _find_by_binding(self, criteria, tag, constraints, parent):
#
#     matched =  self._sldriver.execute_script("""
#         var binding = '%s';
#         var bindings = document.getElementsByClassName('ng-binding');
#         var matches = [];
#         for (var i = 0; i < bindings.length; ++i) {
#             var dataBinding = angular.element(bindings[i]).data('$binding');
#             if(dataBinding) {
#                 var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
#                 if (bindingName.indexOf(binding) != -1) {
#                     matches.push(bindings[i]);
#                 }
#             }
#         }
#         return matches;""")
#     print ("Matched 0", matched)
#
#     return self._sldriver.execute_script("""
#         var binding = '%s';
#         var bindings = document.getElementsByClassName('ng-binding');
#         var matches = [];
#         for (var i = 0; i < bindings.length; ++i) {
#             var dataBinding = angular.element(bindings[i]).data('$binding');
#             if(dataBinding) {
#                 var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
#                 if (bindingName.indexOf(binding) != -1) {
#                     matches.push(bindings[i]);
#                 }
#             }
#         }
#         return matches;
#     """ % criteria)

# @property
# def _s2l(self):
#     return self
#
# @property
# def _sldriver(self):
#     return self._s2l.driver

class NGGuiCommon():
    """Common GUI actions.
    """
    #  class level dictionary gives to possibility to have single instance of SeleniumLibrary per dut
    __shared_state = {}

    def __init__(self, dut=None, dut_version=None, dut_browser='firefox', timeout=60, alias=''):

        self.dut = dut
        self.dut_version = dut_version
        if alias:
            session_name = "%s-%s-%s" % (self.dut, dut_browser, alias)
        else:
            session_name = "%s-%s" % (self.dut, dut_browser)
        if not NGGuiCommon.__shared_state.has_key(session_name):
            # Need to handle run_on_failure action
            self._seleniumlib = AngularJSLibrary(dut=dut, dut_version=dut_version, dut_browser=dut_browser, \
                                                 implicit_angular_wait=timeout, run_on_failure='Handle GUI Failure', \
                                                 alias=session_name)
            NGGuiCommon.__shared_state[session_name] = {'seleniumlib': self._seleniumlib, 'browser': dut_browser}
        else:
            self._seleniumlib = NGGuiCommon.__shared_state[session_name]['seleniumlib']

    # RF Hybrid API for Test Libraries , return all keywords from SeleniumLibrary + its own ones
    def get_keyword_names(self):
        exclude_list = ['ROBOT_LIBRARY_SCOPE', 'ROBOT_LIBRARY_VERSION', 'ROBOT_LIBRARY_LISTENER', 'log', 'dut',
                        'dut_version', 'run_keyword',
                        'dut_browser', 'trackOutstandingTimeouts', 'root_selector', 'attributes', \
                        'ignore_implicit_angular_wait', 'speed', 'keywords', 'attributes', 'screenshot_root_directory',
                        'driver', 'implicit_wait', 'implicit_angular_wait', 'session_name', 'timeout', \
                        'run_on_failure_keyword', 'Get WebElement', 'Get WebElements', 'ctx', 'drivers',
                        'element_finder']

        self.common_keywords = [keyword for keyword in dir(self._seleniumlib) if keyword[0] != '_' and \
                                keyword not in exclude_list]
        return self.common_keywords

    # redirects request for unknown attribures to the SeleniumLibrary
    def __getattr__(self, name):
        if name == '_seleniumlib':
            raise RuntimeError('SeleniumLibrary has not been initialized')
        return getattr(self._seleniumlib, name)


class AngularJSLibrary(SeleniumLibrary, ElementFinder, Logger):

    def __init__(self, dut=None, dut_version=None, dut_browser=None, run_on_failure='Handle GUI Failure', root_selector=None, \
                 implicit_angular_wait=30.0, ignore_implicit_angular_wait=False, alias=''):
        super(AngularJSLibrary, self).__init__(timeout=30.0, run_on_failure=run_on_failure)
        ElementFinder.__init__(self, self._s2l)
        self.dut = dut
        self.dut_version = dut_version
        self.dut_browser = dut_browser
        self.ignore_implicit_angular_wait = ignore_implicit_angular_wait
        self.implicit_angular_wait = implicit_angular_wait

        if not root_selector:
            self.root_selector = '[ng-app]'
        else:
            self.root_selector = root_selector
        if alias:
            self.session_name = "%s-%s-%s" % (self.dut, dut_browser, alias)
        else:
            self.session_name = "%s-%s" % (self.dut, dut_browser)
        print "self.session_name ", dut, dut_version, self.dut_browser, self.session_name

        # Override default locators to include binding {{ }}
        # self._s2l._element_finder = ngElementFinder(self.root_selector, ignore_implicit_angular_wait, self)
        # Add Angular specific locator strategies
        self._s2l.add_location_strategy('ng-binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('binding', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('ng-bind', self._find_by_binding, persist=True)
        self._s2l.add_location_strategy('ng-click', self._find_by_click, persist=True)
        self._s2l.add_location_strategy('click', self._find_by_click, persist=True)
        self._s2l.add_location_strategy('ng-model', self._find_by_model, persist=True)
        self._s2l.add_location_strategy('model', self._find_by_model, persist=True)
        self._s2l.add_location_strategy('ng-repeater', self._find_by_ng_repeater, persist=True)
        self._s2l.add_location_strategy('ng-repeat', self._find_by_ng_repeater, persist=True)
        self._s2l.add_location_strategy('repeater', self._find_by_ng_repeater, persist=True)
        self.trackOutstandingTimeouts = True

    def click_with_action_chain(self, locator):
        self._info("Clicking '%s' using an action chain." % locator)
        action = ActionChains(self._sldriver)
        action.move_to_element(self.find_element(locator))
        action.click()
        action.perform()

    def right_click_on_element(self, locator):
        self._info("Right Clicking '%s' using an action chain." % locator)
        action = ActionChains(self._sldriver)
        action.move_to_element(self.find_element(locator))
        action.context_click()
        action.perform()

    ## Angular JS keywords
    # Wait For Angular

    def change_root_selector(self, selector):
        self.root_selector = selector

    def wait_for_angular(self, timeout=None, error=None):
        """
        An explicit wait allowing Angular queue to empty.

        With the implicit wait functionality it is expected that most of the
        situations where waiting is needed will be handled "automatically" by
        the "hidden" implicit wait. Thus it is expected that this keyword will
        be rarely used.
        """
        # Determine timeout and error

        timeout = timeout or self._s2l.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)
        error = error or ('Timed out waiting for AngularJSLibrary to synchronize with ' +
                          'the page after specified timeout.')

        try:
            WebDriverWait(self._sldriver, timeout, 0.5) \
                .until_not(lambda x: self._sldriver.execute_script(js_wait_for_angular, self.root_selector))
        except TimeoutException:
            pass
            # if self.trackOutstandingTimeouts:
            #    timeouts = self._exec_js('return window.NG_PENDING_TIMEOUTS')
            #    logger.debug(timeouts)
            # pendingHttps = self._exec_js(js_get_pending_http_requests)
            # logger.debug(pendingHttps)
            # raise TimeoutException(error)

    def set_ignore_implicit_angular_wait(self, ignore):
        """
        Turns off the implicit wait by setting ``ignore`` to ${True}. The
        implicit wait can be re-enabled by setting ``ignore`` to ${False}.
        Note the value for ``ignore`` must be a Python boolean, meaning
        either ${True} or ${False} or equivalent, for this
        keyword.

        This is helpful when navigating between a Angular site and a
        non-angular website within the same script.
        """
        if not is_boolean(ignore):
            raise TypeError("Ignore must be boolean, got %s."
                            % type_name(ignore))
        self.ignore_implicit_angular_wait = ignore

    # Locators

    def _find_by_binding(self, browser, criteria, tag=None, constrains={}):
        matches = self._sldriver.execute_script("""
            var binding = '%s';
            var bindings = document.getElementsByClassName('ng-binding');
            var matches = [];
            for (var i = 0; i < bindings.length; ++i) {
                var dataBinding = angular.element(bindings[i]).data('$binding');
                console.log('dataBinding'+dataBinding)
                if(dataBinding) {
                    var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
                    if (bindingName.indexOf(binding) != -1) {
                        matches.push(bindings[i]);
                    }
                }
            }
            return matches;""" % criteria)
        #print ("Matches 0", matches)

        return self._sldriver.execute_script("""
            var binding = '%s';
            var bindings = document.getElementsByClassName('ng-binding');
            var matches = [];
            for (var i = 0; i < bindings.length; ++i) {
                var dataBinding = angular.element(bindings[i]).data('$binding');
                if(dataBinding) {
                    var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
                    if (bindingName.indexOf(binding) != -1) {
                        matches.push(bindings[i]);
                    }
                }
            }
            return matches;
        """ % criteria)

    def _find_by_model(self, parent, criteria, tag, constraints):
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-']  # , 'ng\\:']
        for prefix in prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            elements = self._sldriver.execute_script("""return document.querySelectorAll('%s');""" % selector);
            if len(elements):
                print  ("_find_by_model:  elements, tag, constraints", elements, tag, constraints)
                #modelrec = ElementFinder(self._s2l)._filter_elements(elements, tag, constraints)
                return ElementFinder(self._s2l)._filter_elements(elements, tag, constraints)
        raise ValueError("_find_by_model: Element locator '" + criteria + "' did not match any elements.")

    # Helper Methods
    def _exec_js(self, code):
        return self._sldriver.execute_script(code)

    def _parse_ng_repeat_locator(self, criteria):
        def _startswith(str, sep):
            parts = str.lower().partition(sep)
            if parts[1] == sep and parts[0] == '':
                return parts[2]
            else:
                return None

        def _parse_arrayRE(str):
            import re
            match = re.search(r"(?<=^\[).+([0-9]*).+(?=\]$)", str)
            if match:
                return match.group()
            else:
                return None

        def _parse_array(str):
            if str[0] == '[' and str[-1] == ']':
                return int(str[1:-1])
            else:
                return None

        rrc = criteria.rsplit('@')
        extractElem = {'repeater': None, 'row_index': None, 'col_binding': None}
        if len(rrc) == 1:
            # is only repeater
            extractElem['repeater'] = rrc[0]
            return extractElem
        else:
            # for index in reversed(rrc):
            while 1 < len(rrc):
                index = rrc.pop()
                row = _startswith(index, 'row')
                column = _startswith(index, 'column')
                if row:
                    array = _parse_array(row)
                    rlocator = _startswith(row, '=')
                    if array is not None:
                        extractElem['row_index'] = array
                    elif rlocator:
                        # row should be an list index and not binding locator
                        raise ValueError("AngularJS ng-repeat locator with row as binding is not supported")
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                elif column:
                    array = _parse_array(column)
                    clocator = _startswith(column, '=')
                    if array is not None:
                        # col should be an binding locator and not list index
                        raise ValueError("AngularJS ng-repeat locator with column as index is not supported")
                    elif clocator:
                        extractElem['col_binding'] = clocator
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                else:
                    # stray @ not releated to row/column seperator
                    rrc[-1] = rrc[-1] + '@' + index
        extractElem['repeater'] = rrc[0]
        return extractElem

    def _reconstruct_js_locator(self, loc_dict):
        js_locator = "(\"%s\")" % loc_dict['repeater']
        if loc_dict['row_index']:
            js_locator = js_locator + ".row(%s)" % loc_dict['row_index']
        if loc_dict['col_binding']:
            js_locator = js_locator + ".column(\"%s\")" % loc_dict['col_binding']
        return js_locator

    def find(self, locator, tag=None, first_only=True, required=True,
             parent=None):
        timeout = self._s2l.get_selenium_timeout()
        timeout = timestr_to_secs(timeout)

        if not self.ignore_implicit_angular_wait:
            try:
                WebDriverWait(self._sldriver, timeout, 0.2) \
                    .until_not(lambda x: self._sldriver.execute_script(js_wait_for_angular, self.root_selector))
            except TimeoutException:
                pass
        elements = ElementFinder.find(self, locator, tag, first_only, required, parent)
        return elements

    def _find_by_default(self, criteria, tag, constraints, parent):
        if criteria.startswith('{{'):
            criteria = stripcurly(criteria)
            return self._find_by_binding(criteria, tag, constraints, parent)
        else:
            return ElementFinder._find_by_default(self, criteria, tag, constraints, parent)

    @property
    def _s2l(self):
        return self

    @property
    def _sldriver(self):
        return self._s2l.driver

    ## custom keywords for angular js library

    def handle_gui_failure(self):
        """
        A list of actions to be taken when failure in any GUI library occurs.
        """
        # turn off run_on_failure decorator to avoid recursion calls when
        # exception is raised inside this method
        self._debug('came in handle gui failure...')
        on_failure_keyword = self._get_run_on_failure_name()
        self._set_run_on_failure('Capture Screenshot')
        test_id_var = '${TEST_ID}-'
        try:
            test_id = BuiltIn().replace_variables(test_id_var)
        except:
            test_id = ''

        # try to put window on foreground before making screen shot
        try:
            self._window_focus()
            # wait until window become in focus
            time.sleep(3)
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            pass

        try:
            self.capture_screenshot(test_id + 'screenshot' + '-' + time.strftime('%b%d-%H%M%S', time.gmtime()) + '.png')
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            self._info("Could not capture screenshot of the page")

        try:
            self.capture_source(test_id + 'source' + '-' + test_time + '.html')
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            self._info("Could not log HTML source of the page")

        # turn on run_on_failure decorator
        self._set_run_on_failure(on_failure_keyword)

    def _is_element_present(self, locator):
        try:
            self.element_should_be_visible(locator)
            return True
        except Exception:
            return False

    def _is_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False

    def _is_checked(self, locator):
        try:
            return self.find_element(locator).is_selected()
        except Exception:
            return False

    def _wait_until_element_is_present(self, locator, timeout=5, interval=1):
        """
        Wait until the specified element is present or timeout is expired
        """
        start_time = time.time()
        while ( (time.time() - start_time) <= timeout):
            if self._is_element_present(locator):
                 return True
            time.sleep(interval)
        return False

    def _find_by_click(self, parent, criteria, tag, constraints):
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-']  # , 'ng\\:']
        for prefix in prefixes:
            selector = '[%sclick=\\"%s\\"]' % (prefix, criteria)
            elements = self._sldriver.execute_script("""return document.querySelectorAll("%s");""" % selector);
            if len(elements):
                self._debug("Found:%s"%elements)
                return ElementFinder(self._s2l)._filter_elements(elements, tag, constraints)
        raise ValueError("Element locator '" + criteria + "' did not match any elements.")

    def select_ng_model_dropdown(self, criteria, name, tag=None, constraints={}):
        elements = self._find_by_model(self._sldriver, criteria, tag, constraints)
        for eachElement in elements:
            if eachElement.get_attribute("placeholder") == name:
                print ("Matched ", eachElement.get_attribute("placeholder"))

    def _find_by_ng_repeater(self, parent, criteria, tag, constraints):
        repeater_row_col = self._parse_ng_repeat_locator(criteria)
        js_repeater_str = self._reconstruct_js_locator(repeater_row_col)
        elements = self._sldriver.execute_script(
            js_repeater_min +
            """var ng_repeat = new byRepeaterInner(true);""" +
            """return ng_repeat%s.getElements();""" % (js_repeater_str),
            arg0, arg1
        );
        if len(elements):
            return ElementFinder(self._s2l)._filter_elements(elements, tag, constraints)
        else:
            raise ValueError("Element locator '" + criteria + "' did not match any elements.")

    def select_custom_dropdown(self, locator, choice, regexp=False):
        self.find(locator, first_only=True).click()
        tag_choices = ['a', 'div', 'div/div/span/span']
        self.set_selenium_speed('0s')
        choice_matched = 0
        for eachtag in tag_choices:
            dropdown_option_links = self.find(locator + '//%s'%eachtag, first_only=False)
            for eachelement in dropdown_option_links:
                if eachelement.text:
                    self._debug("Searching: %s:%s:%s" % (locator + '//%s' % eachtag, eachelement.text.strip(), choice))
                    if regexp:
                        if re.search(choice, eachelement.text.strip()):
                            self._info("select_custom_dropdown: Selecting by Regexp:%s" % eachelement.text.strip())
                            eachelement.click()
                            self.wait_for_angular()
                            choice_matched = 1
                            self.set_selenium_speed('0.5s')
                            return
                    if str(eachelement.text.strip()) == str(choice):
                        self._info("select_custom_dropdown: Selecting by choice:%s" % eachelement.text.strip())
                        eachelement.click()
                        self.wait_for_angular()
                        self.set_selenium_speed('0.5s')
                        choice_matched = 1
                        return
        if not choice_matched:
            raise ValueError("Element locator %s : %s did not match any elements" %(locator, choice))

    def select_ngsma_search_result_checkbox(self, locator):
        self.select_custom_checkbox(locator, tag='ngsma-search-result-checkbox')

    def select_custom_checkbox(self, locator, tag='ngsma-custom-checkbox'):
        self.find(locator, first_only=True, tag=tag).click()

    def select_ngsma_checkbox(self, locator):
        self.select_custom_checkbox(locator, tag='ngsma-checkbox')

    def custom_checkbox_should_be_selected(self, locator):
        if self.find(locator + '//input', first_only=True).is_selected():
            return True
        else:
            return False

    def select_ng_repeat_checkbox(self, locator):
        self.find(locator, first_only=True).click()

    def select_ng_repeat_checkbox_be_selected(self, locator):
        if self.find(locator, first_only=True).is_selected():
            return True
        else:
            return False

    def ng_button_is_visible(self, locator):
        elements = self._find_by_click(self._sldriver, locator, None, {})
        for each_element in elements:
            if each_element.is_displayed():
                return True
            else:
                return False

    def click_ng_button(self, criteria, value=None, tag=None, constraints={}):
        elements = self._find_by_click(self._sldriver, criteria, tag, constraints)
        for click_element in elements:
            self._debug("Current Text:%s|:Input Text:%s" % (click_element.text, value))
            if value in click_element.text:
                click_element.click()
                return
        self.wait_for_angular()
        raise ValueError("Element locator '" + criteria + "' did not match any elements.")

    def select_date_on_calendar_widget(self, locator, date, tag='td'):
        self.click_element(locator)
        date_swap = date.split('/')
        date_swap[0], date_swap[1] = date_swap[1], str(int(date_swap[0])-1)
        md_date = '-'.join([str(int(x)) for x in date_swap[::-1]])
        found_elements = self.find("//%s[contains(@id,'month-%s')]"% (tag,md_date), tag=tag, first_only=False)
        for eachelement in found_elements:
            if int(eachelement.text) ==  int(date.split('/')[1]):
                self._debug("Found:date on calendar widget:%s" % eachelement)
                self._debug("Matched::%s"% (eachelement.text))
                eachelement.click()
                return
        self.wait_for_angular()
        raise ValueError("Element locator on calendar widget" + locator + "' did not match any elements.")


    ###end custom keywords

    ###  user keywords
    def _check_login_successful(self, locator):
        ERROR_MSG_LOCATOR = 'css:.ping-error-msg'
        ERROR_NOTIFICATION = "//*[@class='notification__content ng-binding']"
	if self._is_element_present(ERROR_NOTIFICATION) and "/ng-login" in self.get_location():
	    error_msg = self.get_text(ERROR_NOTIFICATION)
	    if error_msg:
		raise GuiLoginFailureError('ERROR: Login Into dut Failed:%s' % error_msg)

	if self._is_element_present(locator) and "/ng-login" in self.get_location():
            raise GuiLoginFailureError('ERROR: Login Into dut Failed:%s' % self.get_text(ERROR_MSG_LOCATOR))
	
    def _get_dut_default_url(self, protocol):
        return '%s://%s:%s/ng-login' % (protocol, self.dut, self._get_default_dut_port(protocol))

    def _get_default_dut_port(self, protocol='https'):
        DEFAULT_PORTS = {'WSA': {'http': 8080, 'https': 8443}, 'ESA': {'http': 80, 'https': 443}}
        if self.dut_version.startswith('coeus'):
            return DEFAULT_PORTS['WSA'][protocol]
        else:
            return DEFAULT_PORTS['ESA'][protocol]

    def launch_dut_browser(self, dut_url=None, dut_browser=None, protocol='https', delay=0.5):
        disable_insecure_cert = ['chrome','opera']
        allowed_attempts = 3
        desired_capabilities = {}
        dut_browser = dut_browser or self.dut_browser
        if not dut_url:
            dut_url = self._get_dut_default_url(protocol)
        self._debug("launch_dut_browser :::%s %s %s" % (dut_url, dut_browser, self.session_name))
        if dut_browser in disable_insecure_cert:
            desired_capabilities = {"acceptInsecureCerts": True, 'acceptSslCerts':True}
        for open_browser_attempt in range(allowed_attempts):
            try:
                self.open_browser(dut_url, browser=self.dut_browser, alias=self.session_name, desired_capabilities=desired_capabilities)
            except Exception as e:
                if open_browser_attempt < allowed_attempts - 1:
                    self._warn("Got exception from open_browser: %s. Will attempt open_browser again" % str(e))
                else:
                    self._warn("Got exception from open_browser: %s.Too many failed attempt for open_browser" % str(e))
                    raise
                try:
                    self.close_browser()
                except Exception as e:
                    self._warn("Got exception from driver: %s during close_browser" % str(e))
            else:
                break
        self.set_selenium_speed(delay)
        self.maximize_browser_window()

    def _check_logout_successful(self):
        ERROR_MSG_LOCATOR = "//span[contains(.,'Logout Successful.')]"
        if self.get_text(ERROR_MSG_LOCATOR) != 'Logout Successful.' and "/ng-login" not in self.get_location():
            raise GuiLoginFailureError('ERROR: Logout of dut Failed:%s' % self.get_text(ERROR_MSG_LOCATOR))

    def login_into_dut(self, username=None, password=None):
        logged_in = False
        count = 0
        username_xpath = 'id:username'
        password_xpath = 'id:password'
        login_button = "//*[@type='submit' and text()='Log in']"
        if not username:
            username = 'admin'
        if not password:
            password = Misc(None, None).get_admin_password(self.dut)

        while (not logged_in and count <=2):
            try:
                self.input_text(username_xpath, username)
                self.input_password(password_xpath, password)
                self.click_button(login_button)
                self.wait_for_angular(timeout=30)
                self._check_login_successful(login_button)
                self._info("Login Successful Username:%s Password:%s" % (username, password))
                logged_in = True
            except Exception:
                pass
            count +=1
        if not logged_in:
            self._info("Failed to Login Username:%s Password:%s" % (username, password))
            self._check_login_successful(login_button)

    def logout_of_dut(self):
        logout_menu_xpath = "//div[@class='menu-header__item dropdown']"
        logout_icon_xpath = "//div[@class='menu-header__item dropdown']/ul/li/a"
        self.click_with_action_chain(logout_menu_xpath)
        self.click_element(logout_icon_xpath)
        self.wait_for_angular()
        self._check_logout_successful()

    def get_current_user(self):
        current_user = "//*[@id='userLabel']"
        return self.get_text(current_user)

    def login_into_casebook(self, server, clientid, clientsecret):
        self.click_element('//*[@id="ats-casebook-button"]')
        self.wait_for_angular()
        if 'Login to use Casebook/Pivot Menu' in self.get_text(
                '//md-dialog[@class="ngsma-ctr-authentication _md md-transition-in"]/md-toolbar/div'):
            print "case menus opened"
            # click on cancel
            cancel_button = "//md-dialog[@class='ngsma-ctr-authentication _md md-transition-in']/form/md-dialog-actions/button[1]/span"
            self.click_element(cancel_button)
            self.wait_for_angular()
        else:
            pass

    def _visit_to(self, pagepath, urlpath, wait=True):
        self.set_selenium_speed('0s')
        self.click_element(pagepath)
        if wait:
            self.wait_for_angular()
        if urlpath not in self.get_location():
            raise InvalidUrlPathError

    def select_ng_dropdown(self, locator,  choice):
        found_dropdown = self.find(locator, first_only=True)
        found_dropdown.click()
        dropdown_option_links = self.find(locator , first_only=False)
        for eachelement in dropdown_option_links:
            if eachelement.text:
                if str(eachelement.text.strip()) == str(choice):
                    self._info("select_custom_dropdown: Selecting by choice:%s" % eachelement.text.strip())
                    eachelement.click()
                    self.wait_for_angular()
                    return

    def check_for_backend_error(self):
        """This keyword will check for any backend errors after some action on ngui"""
        backend_error = "//*[@translation-key='common.errors.backend_error_smth_went_wrong']"
        return self._is_visible(backend_error)

    def get_grid_canvas_details(self, canvas, headers, counter=False, flag=False):
        """
        To get the canvas details of labels values etc /labels , percent, value
        :param canvas: Canvas Xpath
        :param headers: header names
        :return: dict of canvas details with label as key
        """
        details = {}
        if self._is_visible(canvas):

            if flag:
                ele_count= range(1, self.get_element_count(canvas))
            else:
                ele_count= range(1, self.get_element_count(canvas) +1)
            for eachcanvas in ele_count:
                marked_label_list = self.get_text('%s[%s]' % (canvas, eachcanvas)).strip().split('\n')
                if len(headers) == 2:
                    details[marked_label_list[0]] = marked_label_list[1]
                if len(headers) == 3:
                    if counter:
			            details[marked_label_list[0]] ={headers[0]:marked_label_list[0],
                                                    headers[1]:marked_label_list[1].split(' ')[0],
                                                    headers[2]:marked_label_list[1].split(' ')[1]}
                    else:
			            details[marked_label_list[0]] ={headers[0]:marked_label_list[0],
                                                    headers[1]:marked_label_list[1],
                                                    headers[2]:marked_label_list[2]}
            return details
        else:
            raise DataNotFoundError('Grid Canvas is not found..')

    def switch_dusk_theme(self):
        """
        To enable the dusk theme on ngui
        :return: None
        """
        logout_menu_xpath = "//div[@class='menu-header__item dropdown']"
        dusk_theme = "//*[@ng-click='$ctrl.toggleDarkTheme()']"
        self.click_with_action_chain(logout_menu_xpath)
        self.click_element(dusk_theme)
