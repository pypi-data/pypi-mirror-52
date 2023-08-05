(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_extra"] = factory(require("react"));
	else
		root["dazzler_extra"] = factory(root["React"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"extra": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonpdazzler_name_"] = window["webpackJsonpdazzler_name_"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([4,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss":
/*!************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss ***!
  \************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./src/extra/js/components/Drawer.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Drawer.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Drawer; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var Caret = function Caret(_ref) {
  var side = _ref.side,
      opened = _ref.opened;

  switch (side) {
    case 'top':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B2") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25BC");

    case 'right':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B8") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25C2");

    case 'left':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25C2") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B8");

    case 'bottom':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25BC") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B2");
  }
};
/**
 * Draw content from the sides of the screen.
 */


var Drawer =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Drawer, _React$Component);

  function Drawer() {
    _classCallCheck(this, Drawer);

    return _possibleConstructorReturn(this, _getPrototypeOf(Drawer).apply(this, arguments));
  }

  _createClass(Drawer, [{
    key: "render",
    value: function render() {
      var _this = this;

      var _this$props = this.props,
          class_name = _this$props.class_name,
          identity = _this$props.identity,
          style = _this$props.style,
          children = _this$props.children,
          opened = _this$props.opened,
          side = _this$props.side;
      var css = [side];

      if (side === 'top' || side === 'bottom') {
        css.push('horizontal');
      } else {
        css.push('vertical');
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, [class_name])),
        id: identity,
        style: style
      }, opened && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, ['drawer-content']))
      }, children), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, ['drawer-control'])),
        onClick: function onClick() {
          return _this.props.updateAspects({
            opened: !opened
          });
        }
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Caret, {
        opened: opened,
        side: side
      })));
    }
  }]);

  return Drawer;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Drawer.defaultProps = {
  side: 'top'
};
Drawer.propTypes = {
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  opened: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Side which open.
   */
  side: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['top', 'left', 'right', 'bottom']),

  /**
   *  Unique id for this component
   */
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Update aspects on the backend.
   */
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Notice.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Notice.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Notice; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Browser notifications with permissions handling.
 */

var Notice =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Notice, _React$Component);

  function Notice(props) {
    var _this;

    _classCallCheck(this, Notice);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Notice).call(this, props));
    _this.state = {
      lastMessage: props.body,
      notification: null
    };
    _this.onPermission = _this.onPermission.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Notice, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      var updateAspects = this.props.updateAspects;

      if (!('Notification' in window) && updateAspects) {
        updateAspects({
          permission: 'unsupported'
        });
      } else if (Notification.permission === 'default') {
        Notification.requestPermission().then(this.onPermission);
      } else {
        this.onPermission(window.Notification.permission);
      }
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      if (!prevProps.displayed && this.props.displayed) {
        this.sendNotification(this.props.permission);
      }
    }
  }, {
    key: "sendNotification",
    value: function sendNotification(permission) {
      var _this2 = this;

      var _this$props = this.props,
          updateAspects = _this$props.updateAspects,
          body = _this$props.body,
          title = _this$props.title,
          icon = _this$props.icon,
          require_interaction = _this$props.require_interaction,
          lang = _this$props.lang,
          badge = _this$props.badge,
          tag = _this$props.tag,
          image = _this$props.image,
          vibrate = _this$props.vibrate;

      if (permission === 'granted') {
        var options = {
          requireInteraction: require_interaction,
          body: body,
          icon: icon,
          lang: lang,
          badge: badge,
          tag: tag,
          image: image,
          vibrate: vibrate
        };
        var notification = new Notification(title, options);

        notification.onclick = function () {
          if (updateAspects) {
            updateAspects(Object(ramda__WEBPACK_IMPORTED_MODULE_3__["merge"])({
              displayed: false
            }, Object(_commons_js__WEBPACK_IMPORTED_MODULE_2__["timestampProp"])('clicks', _this2.props.clicks + 1)));
          }
        };

        notification.onclose = function () {
          if (updateAspects) {
            updateAspects(Object(ramda__WEBPACK_IMPORTED_MODULE_3__["merge"])({
              displayed: false
            }, Object(_commons_js__WEBPACK_IMPORTED_MODULE_2__["timestampProp"])('closes', _this2.props.closes + 1)));
          }
        };
      }
    }
  }, {
    key: "onPermission",
    value: function onPermission(permission) {
      var _this$props2 = this.props,
          displayed = _this$props2.displayed,
          updateAspects = _this$props2.updateAspects;

      if (updateAspects) {
        updateAspects({
          permission: permission
        });
      }

      if (displayed) {
        this.sendNotification(permission);
      }
    }
  }, {
    key: "render",
    value: function render() {
      return null;
    }
  }]);

  return Notice;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Notice.defaultProps = {
  require_interaction: false,
  clicks: 0,
  clicks_timestamp: -1,
  closes: 0,
  closes_timestamp: -1
}; // Props docs from https://developer.mozilla.org/en-US/docs/Web/API/Notification/Notification

Notice.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Permission granted by the user (READONLY)
   */
  permission: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['denied', 'granted', 'default', 'unsupported']),
  title: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,

  /**
   * The notification's language, as specified using a DOMString representing a BCP 47 language tag.
   */
  lang: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A DOMString representing the body text of the notification, which will be displayed below the title.
   */
  body: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A USVString containing the URL of the image used to represent the notification when there is not enough space to display the notification itself.
   */
  badge: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A DOMString representing an identifying tag for the notification.
   */
  tag: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A USVString containing the URL of an icon to be displayed in the notification.
   */
  icon: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   *  a USVString containing the URL of an image to be displayed in the notification.
   */
  image: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A vibration pattern for the device's vibration hardware to emit when the notification fires.
   */
  vibrate: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOfType([prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number, prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number)]),

  /**
   * Indicates that a notification should remain active until the user clicks or dismisses it, rather than closing automatically. The default value is false.
   */
  require_interaction: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Set to true to display the notification.
   */
  displayed: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  clicks: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  clicks_timestamp: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Number of times the notification was closed.
   */
  closes: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  closes_timestamp: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  updateAspect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Pager.jsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/Pager.jsx ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Pager; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var startOffset = function startOffset(page, itemPerPage) {
  return (page - 1) * (page > 1 ? itemPerPage : 0);
};

var endOffset = function endOffset(start, itemPerPage, page, total, leftOver) {
  return page !== total ? start + itemPerPage : leftOver !== 0 ? start + leftOver : start + itemPerPage;
};

var showList = function showList(page, total, n) {
  if (total > n) {
    var middle = n / 2;
    var first = page >= total - middle ? total - n + 1 : page > middle ? page - middle : 1;
    var last = page < total - middle ? first + n : total + 1;
    return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["range"])(first, last);
  }

  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["range"])(1, total + 1);
};

var Page = function Page(_ref) {
  var style = _ref.style,
      class_name = _ref.class_name,
      on_change = _ref.on_change,
      text = _ref.text,
      page = _ref.page;
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", {
    style: style,
    className: class_name,
    onClick: function onClick() {
      return on_change(page);
    }
  }, text || page);
};
/**
 * Paging for dazzler apps.
 */


var Pager =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Pager, _React$Component);

  function Pager(props) {
    var _this;

    _classCallCheck(this, Pager);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Pager).call(this, props));
    _this.state = {
      current_page: null,
      start_offset: null,
      end_offset: null,
      pages: [],
      total_pages: Math.ceil(props.total_items / props.items_per_page)
    };
    _this.onChangePage = _this.onChangePage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Pager, [{
    key: "componentWillMount",
    value: function componentWillMount() {
      this.onChangePage(this.props.current_page);
    }
  }, {
    key: "onChangePage",
    value: function onChangePage(page) {
      var _this$props = this.props,
          items_per_page = _this$props.items_per_page,
          total_items = _this$props.total_items,
          updateAspects = _this$props.updateAspects,
          pages_displayed = _this$props.pages_displayed;
      var total_pages = this.state.total_pages;
      var start_offset = startOffset(page, items_per_page);
      var leftOver = total_items % items_per_page;
      var end_offset = endOffset(start_offset, items_per_page, page, total_pages, leftOver);
      var payload = {
        current_page: page,
        start_offset: start_offset,
        end_offset: end_offset,
        pages: showList(page, total_pages, pages_displayed)
      };
      this.setState(payload);

      if (updateAspects) {
        if (this.state.total_pages !== this.props.total_pages) {
          payload.total_pages = this.state.total_pages;
        }

        updateAspects(payload);
      }
    }
  }, {
    key: "componentWillReceiveProps",
    value: function componentWillReceiveProps(props) {
      if (props.current_page !== this.state.current_page) {
        this.onChangePage(props.current_page);
      }
    }
  }, {
    key: "render",
    value: function render() {
      var _this2 = this;

      var _this$state = this.state,
          current_page = _this$state.current_page,
          pages = _this$state.pages,
          total_pages = _this$state.total_pages;
      var _this$props2 = this.props,
          class_name = _this$props2.class_name,
          identity = _this$props2.identity,
          page_style = _this$props2.page_style,
          page_class_name = _this$props2.page_class_name;
      var pageCss = ['page'];

      if (page_class_name) {
        pageCss.push(page_class_name);
      }

      pageCss = Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', pageCss);
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: class_name,
        id: identity
      }, current_page > 1 && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: 1,
        text: 'first',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), current_page > 1 && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: current_page - 1,
        text: 'previous',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), pages.map(function (e) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
          page: e,
          key: "page-".concat(e),
          style: page_style,
          class_name: pageCss,
          on_change: _this2.onChangePage
        });
      }), current_page < total_pages && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: current_page + 1,
        text: 'next',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), current_page < total_pages && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: total_pages,
        text: 'last',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }));
    }
  }]);

  return Pager;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Pager.defaultProps = {
  current_page: 1,
  items_per_page: 10,
  pages_displayed: 10
};
Pager.propTypes = {
  /**
   * The total items in the set.
   */
  total_items: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number.isRequired,

  /**
   * The number of items a page contains.
   */
  items_per_page: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Style for the page numbers.
   */
  page_style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   * CSS class for the page numbers.
   */
  page_class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * The number of pages displayed by the pager.
   */
  pages_displayed: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Read only, the currently displayed pages numbers.
   */
  pages: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,

  /**
   * The current selected page.
   */
  current_page: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Set by total_items / items_per_page
   */
  total_pages: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * The starting index of the current page
   * Can be used to slice data eg: data[start_offset: end_offset]
   */
  start_offset: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * The end index of the current page.
   */
  end_offset: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Spinner.jsx":
/*!*********************************************!*\
  !*** ./src/extra/js/components/Spinner.jsx ***!
  \*********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Spinner; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }



/**
 * Simple html/css spinner.
 */

var Spinner =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Spinner, _React$Component);

  function Spinner() {
    _classCallCheck(this, Spinner);

    return _possibleConstructorReturn(this, _getPrototypeOf(Spinner).apply(this, arguments));
  }

  _createClass(Spinner, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          class_name = _this$props.class_name,
          style = _this$props.style,
          identity = _this$props.identity;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: identity,
        className: class_name,
        style: style
      });
    }
  }]);

  return Spinner;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Spinner.defaultProps = {};
Spinner.propTypes = {
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   *  Unique id for this component
   */
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Update aspects on the backend.
   */
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Sticky.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Sticky.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Sticky; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




/**
 * A shorthand component for a sticky div.
 */

var Sticky =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Sticky, _React$Component);

  function Sticky() {
    _classCallCheck(this, Sticky);

    return _possibleConstructorReturn(this, _getPrototypeOf(Sticky).apply(this, arguments));
  }

  _createClass(Sticky, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          class_name = _this$props.class_name,
          identity = _this$props.identity,
          style = _this$props.style,
          children = _this$props.children,
          top = _this$props.top,
          left = _this$props.left,
          right = _this$props.right,
          bottom = _this$props.bottom;
      var styles = Object(ramda__WEBPACK_IMPORTED_MODULE_2__["mergeAll"])([style, {
        top: top,
        left: left,
        right: right,
        bottom: bottom
      }]);
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: class_name,
        id: identity,
        style: styles
      }, children);
    }
  }]);

  return Sticky;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Sticky.defaultProps = {}; // TODO Add Sticky props descriptions

Sticky.propTypes = {
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  top: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  left: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  right: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  bottom: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string
};

/***/ }),

/***/ "./src/extra/js/index.js":
/*!*******************************!*\
  !*** ./src/extra/js/index.js ***!
  \*******************************/
/*! exports provided: Notice, Pager, Spinner, Sticky, Drawer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../scss/index.scss */ "./src/extra/scss/index.scss");
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_scss_index_scss__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_Notice__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/Notice */ "./src/extra/js/components/Notice.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Notice", function() { return _components_Notice__WEBPACK_IMPORTED_MODULE_1__["default"]; });

/* harmony import */ var _components_Pager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Pager */ "./src/extra/js/components/Pager.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Pager", function() { return _components_Pager__WEBPACK_IMPORTED_MODULE_2__["default"]; });

/* harmony import */ var _components_Spinner__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/Spinner */ "./src/extra/js/components/Spinner.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Spinner", function() { return _components_Spinner__WEBPACK_IMPORTED_MODULE_3__["default"]; });

/* harmony import */ var _components_Sticky__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/Sticky */ "./src/extra/js/components/Sticky.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Sticky", function() { return _components_Sticky__WEBPACK_IMPORTED_MODULE_4__["default"]; });

/* harmony import */ var _components_Drawer__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/Drawer */ "./src/extra/js/components/Drawer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Drawer", function() { return _components_Drawer__WEBPACK_IMPORTED_MODULE_5__["default"]; });









/***/ }),

/***/ "./src/extra/scss/index.scss":
/*!***********************************!*\
  !*** ./src/extra/scss/index.scss ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../../node_modules/mini-css-extract-plugin/dist/loader.js!../../../node_modules/css-loader/dist/cjs.js!../../../node_modules/sass-loader/lib/loader.js!./index.scss */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ 4:
/*!*************************************!*\
  !*** multi ./src/extra/js/index.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/extra/js/index.js */"./src/extra/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvZXh0cmEvc2Nzcy9pbmRleC5zY3NzPzNmMzUiLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvZXh0cmEvanMvY29tcG9uZW50cy9EcmF3ZXIuanN4Iiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvTm90aWNlLmpzeCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL1BhZ2VyLmpzeCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL1NwaW5uZXIuanN4Iiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvU3RpY2t5LmpzeCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9leHRyYS9qcy9pbmRleC5qcyIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9leHRyYS9zY3NzL2luZGV4LnNjc3M/NGY5MCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9Il0sIm5hbWVzIjpbIkNhcmV0Iiwic2lkZSIsIm9wZW5lZCIsIkRyYXdlciIsInByb3BzIiwiY2xhc3NfbmFtZSIsImlkZW50aXR5Iiwic3R5bGUiLCJjaGlsZHJlbiIsImNzcyIsInB1c2giLCJqb2luIiwiY29uY2F0IiwidXBkYXRlQXNwZWN0cyIsIlJlYWN0IiwiQ29tcG9uZW50IiwiZGVmYXVsdFByb3BzIiwicHJvcFR5cGVzIiwiUHJvcFR5cGVzIiwibm9kZSIsImJvb2wiLCJvYmplY3QiLCJzdHJpbmciLCJvbmVPZiIsImZ1bmMiLCJOb3RpY2UiLCJzdGF0ZSIsImxhc3RNZXNzYWdlIiwiYm9keSIsIm5vdGlmaWNhdGlvbiIsIm9uUGVybWlzc2lvbiIsImJpbmQiLCJ3aW5kb3ciLCJwZXJtaXNzaW9uIiwiTm90aWZpY2F0aW9uIiwicmVxdWVzdFBlcm1pc3Npb24iLCJ0aGVuIiwicHJldlByb3BzIiwiZGlzcGxheWVkIiwic2VuZE5vdGlmaWNhdGlvbiIsInRpdGxlIiwiaWNvbiIsInJlcXVpcmVfaW50ZXJhY3Rpb24iLCJsYW5nIiwiYmFkZ2UiLCJ0YWciLCJpbWFnZSIsInZpYnJhdGUiLCJvcHRpb25zIiwicmVxdWlyZUludGVyYWN0aW9uIiwib25jbGljayIsIm1lcmdlIiwidGltZXN0YW1wUHJvcCIsImNsaWNrcyIsIm9uY2xvc2UiLCJjbG9zZXMiLCJjbGlja3NfdGltZXN0YW1wIiwiY2xvc2VzX3RpbWVzdGFtcCIsImlzUmVxdWlyZWQiLCJvbmVPZlR5cGUiLCJudW1iZXIiLCJhcnJheU9mIiwidXBkYXRlQXNwZWN0Iiwic3RhcnRPZmZzZXQiLCJwYWdlIiwiaXRlbVBlclBhZ2UiLCJlbmRPZmZzZXQiLCJzdGFydCIsInRvdGFsIiwibGVmdE92ZXIiLCJzaG93TGlzdCIsIm4iLCJtaWRkbGUiLCJmaXJzdCIsImxhc3QiLCJyYW5nZSIsIlBhZ2UiLCJvbl9jaGFuZ2UiLCJ0ZXh0IiwiUGFnZXIiLCJjdXJyZW50X3BhZ2UiLCJzdGFydF9vZmZzZXQiLCJlbmRfb2Zmc2V0IiwicGFnZXMiLCJ0b3RhbF9wYWdlcyIsIk1hdGgiLCJjZWlsIiwidG90YWxfaXRlbXMiLCJpdGVtc19wZXJfcGFnZSIsIm9uQ2hhbmdlUGFnZSIsInBhZ2VzX2Rpc3BsYXllZCIsInBheWxvYWQiLCJzZXRTdGF0ZSIsInBhZ2Vfc3R5bGUiLCJwYWdlX2NsYXNzX25hbWUiLCJwYWdlQ3NzIiwibWFwIiwiZSIsImFycmF5IiwiU3Bpbm5lciIsIlN0aWNreSIsInRvcCIsImxlZnQiLCJyaWdodCIsImJvdHRvbSIsInN0eWxlcyIsIm1lcmdlQWxsIl0sIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTztBQ1ZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0JBQVEsb0JBQW9CO0FBQzVCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EseUJBQWlCLDRCQUE0QjtBQUM3QztBQUNBO0FBQ0EsMEJBQWtCLDJCQUEyQjtBQUM3QztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOzs7QUFHQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0Esa0RBQTBDLGdDQUFnQztBQUMxRTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdFQUF3RCxrQkFBa0I7QUFDMUU7QUFDQSx5REFBaUQsY0FBYztBQUMvRDs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaURBQXlDLGlDQUFpQztBQUMxRSx3SEFBZ0gsbUJBQW1CLEVBQUU7QUFDckk7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxtQ0FBMkIsMEJBQTBCLEVBQUU7QUFDdkQseUNBQWlDLGVBQWU7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YSxtQkFBTyxDQUFDLHlHQUFzRDs7QUFFM0U7O0FBRUEsR0FBRyxLQUFVLEVBQUUsRTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNuQmYsbUQiLCJmaWxlIjoiZGF6emxlcl9leHRyYV8wNWI0NTllMDBmODc3Nzg4MTNjMS5qcyIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfZXh0cmFcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9leHRyYVwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHdpbmRvdywgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fKSB7XG5yZXR1cm4gIiwiIFx0Ly8gaW5zdGFsbCBhIEpTT05QIGNhbGxiYWNrIGZvciBjaHVuayBsb2FkaW5nXG4gXHRmdW5jdGlvbiB3ZWJwYWNrSnNvbnBDYWxsYmFjayhkYXRhKSB7XG4gXHRcdHZhciBjaHVua0lkcyA9IGRhdGFbMF07XG4gXHRcdHZhciBtb3JlTW9kdWxlcyA9IGRhdGFbMV07XG4gXHRcdHZhciBleGVjdXRlTW9kdWxlcyA9IGRhdGFbMl07XG5cbiBcdFx0Ly8gYWRkIFwibW9yZU1vZHVsZXNcIiB0byB0aGUgbW9kdWxlcyBvYmplY3QsXG4gXHRcdC8vIHRoZW4gZmxhZyBhbGwgXCJjaHVua0lkc1wiIGFzIGxvYWRlZCBhbmQgZmlyZSBjYWxsYmFja1xuIFx0XHR2YXIgbW9kdWxlSWQsIGNodW5rSWQsIGkgPSAwLCByZXNvbHZlcyA9IFtdO1xuIFx0XHRmb3IoO2kgPCBjaHVua0lkcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdGNodW5rSWQgPSBjaHVua0lkc1tpXTtcbiBcdFx0XHRpZihpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0pIHtcbiBcdFx0XHRcdHJlc29sdmVzLnB1c2goaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdWzBdKTtcbiBcdFx0XHR9XG4gXHRcdFx0aW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdID0gMDtcbiBcdFx0fVxuIFx0XHRmb3IobW9kdWxlSWQgaW4gbW9yZU1vZHVsZXMpIHtcbiBcdFx0XHRpZihPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwobW9yZU1vZHVsZXMsIG1vZHVsZUlkKSkge1xuIFx0XHRcdFx0bW9kdWxlc1ttb2R1bGVJZF0gPSBtb3JlTW9kdWxlc1ttb2R1bGVJZF07XG4gXHRcdFx0fVxuIFx0XHR9XG4gXHRcdGlmKHBhcmVudEpzb25wRnVuY3Rpb24pIHBhcmVudEpzb25wRnVuY3Rpb24oZGF0YSk7XG5cbiBcdFx0d2hpbGUocmVzb2x2ZXMubGVuZ3RoKSB7XG4gXHRcdFx0cmVzb2x2ZXMuc2hpZnQoKSgpO1xuIFx0XHR9XG5cbiBcdFx0Ly8gYWRkIGVudHJ5IG1vZHVsZXMgZnJvbSBsb2FkZWQgY2h1bmsgdG8gZGVmZXJyZWQgbGlzdFxuIFx0XHRkZWZlcnJlZE1vZHVsZXMucHVzaC5hcHBseShkZWZlcnJlZE1vZHVsZXMsIGV4ZWN1dGVNb2R1bGVzIHx8IFtdKTtcblxuIFx0XHQvLyBydW4gZGVmZXJyZWQgbW9kdWxlcyB3aGVuIGFsbCBjaHVua3MgcmVhZHlcbiBcdFx0cmV0dXJuIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCk7XG4gXHR9O1xuIFx0ZnVuY3Rpb24gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKSB7XG4gXHRcdHZhciByZXN1bHQ7XG4gXHRcdGZvcih2YXIgaSA9IDA7IGkgPCBkZWZlcnJlZE1vZHVsZXMubGVuZ3RoOyBpKyspIHtcbiBcdFx0XHR2YXIgZGVmZXJyZWRNb2R1bGUgPSBkZWZlcnJlZE1vZHVsZXNbaV07XG4gXHRcdFx0dmFyIGZ1bGZpbGxlZCA9IHRydWU7XG4gXHRcdFx0Zm9yKHZhciBqID0gMTsgaiA8IGRlZmVycmVkTW9kdWxlLmxlbmd0aDsgaisrKSB7XG4gXHRcdFx0XHR2YXIgZGVwSWQgPSBkZWZlcnJlZE1vZHVsZVtqXTtcbiBcdFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tkZXBJZF0gIT09IDApIGZ1bGZpbGxlZCA9IGZhbHNlO1xuIFx0XHRcdH1cbiBcdFx0XHRpZihmdWxmaWxsZWQpIHtcbiBcdFx0XHRcdGRlZmVycmVkTW9kdWxlcy5zcGxpY2UoaS0tLCAxKTtcbiBcdFx0XHRcdHJlc3VsdCA9IF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gZGVmZXJyZWRNb2R1bGVbMF0pO1xuIFx0XHRcdH1cbiBcdFx0fVxuXG4gXHRcdHJldHVybiByZXN1bHQ7XG4gXHR9XG5cbiBcdC8vIFRoZSBtb2R1bGUgY2FjaGVcbiBcdHZhciBpbnN0YWxsZWRNb2R1bGVzID0ge307XG5cbiBcdC8vIG9iamVjdCB0byBzdG9yZSBsb2FkZWQgYW5kIGxvYWRpbmcgY2h1bmtzXG4gXHQvLyB1bmRlZmluZWQgPSBjaHVuayBub3QgbG9hZGVkLCBudWxsID0gY2h1bmsgcHJlbG9hZGVkL3ByZWZldGNoZWRcbiBcdC8vIFByb21pc2UgPSBjaHVuayBsb2FkaW5nLCAwID0gY2h1bmsgbG9hZGVkXG4gXHR2YXIgaW5zdGFsbGVkQ2h1bmtzID0ge1xuIFx0XHRcImV4dHJhXCI6IDBcbiBcdH07XG5cbiBcdHZhciBkZWZlcnJlZE1vZHVsZXMgPSBbXTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuIFx0dmFyIGpzb25wQXJyYXkgPSB3aW5kb3dbXCJ3ZWJwYWNrSnNvbnBkYXp6bGVyX25hbWVfXCJdID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSB8fCBbXTtcbiBcdHZhciBvbGRKc29ucEZ1bmN0aW9uID0ganNvbnBBcnJheS5wdXNoLmJpbmQoanNvbnBBcnJheSk7XG4gXHRqc29ucEFycmF5LnB1c2ggPSB3ZWJwYWNrSnNvbnBDYWxsYmFjaztcbiBcdGpzb25wQXJyYXkgPSBqc29ucEFycmF5LnNsaWNlKCk7XG4gXHRmb3IodmFyIGkgPSAwOyBpIDwganNvbnBBcnJheS5sZW5ndGg7IGkrKykgd2VicGFja0pzb25wQ2FsbGJhY2soanNvbnBBcnJheVtpXSk7XG4gXHR2YXIgcGFyZW50SnNvbnBGdW5jdGlvbiA9IG9sZEpzb25wRnVuY3Rpb247XG5cblxuIFx0Ly8gYWRkIGVudHJ5IG1vZHVsZSB0byBkZWZlcnJlZCBsaXN0XG4gXHRkZWZlcnJlZE1vZHVsZXMucHVzaChbNCxcImNvbW1vbnNcIl0pO1xuIFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiByZWFkeVxuIFx0cmV0dXJuIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCk7XG4iLCIvLyBleHRyYWN0ZWQgYnkgbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7am9pbiwgY29uY2F0fSBmcm9tICdyYW1kYSc7XG5cbmNvbnN0IENhcmV0ID0gKHtzaWRlLCBvcGVuZWR9KSA9PiB7XG4gICAgc3dpdGNoIChzaWRlKSB7XG4gICAgICAgIGNhc2UgJ3RvcCc6XG4gICAgICAgICAgICByZXR1cm4gb3BlbmVkID8gPHNwYW4+JiM5NjUwOzwvc3Bhbj4gOiA8c3Bhbj4mIzk2NjA7PC9zcGFuPjtcbiAgICAgICAgY2FzZSAncmlnaHQnOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY1Njs8L3NwYW4+IDogPHNwYW4+JiM5NjY2Ozwvc3Bhbj47XG4gICAgICAgIGNhc2UgJ2xlZnQnOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY2Njs8L3NwYW4+IDogPHNwYW4+JiM5NjU2Ozwvc3Bhbj47XG4gICAgICAgIGNhc2UgJ2JvdHRvbSc6XG4gICAgICAgICAgICByZXR1cm4gb3BlbmVkID8gPHNwYW4+JiM5NjYwOzwvc3Bhbj4gOiA8c3Bhbj4mIzk2NTA7PC9zcGFuPjtcbiAgICB9XG59O1xuXG4vKipcbiAqIERyYXcgY29udGVudCBmcm9tIHRoZSBzaWRlcyBvZiB0aGUgc2NyZWVuLlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBEcmF3ZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge1xuICAgICAgICAgICAgY2xhc3NfbmFtZSxcbiAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgc3R5bGUsXG4gICAgICAgICAgICBjaGlsZHJlbixcbiAgICAgICAgICAgIG9wZW5lZCxcbiAgICAgICAgICAgIHNpZGUsXG4gICAgICAgIH0gPSB0aGlzLnByb3BzO1xuXG4gICAgICAgIGNvbnN0IGNzcyA9IFtzaWRlXTtcblxuICAgICAgICBpZiAoc2lkZSA9PT0gJ3RvcCcgfHwgc2lkZSA9PT0gJ2JvdHRvbScpIHtcbiAgICAgICAgICAgIGNzcy5wdXNoKCdob3Jpem9udGFsJyk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBjc3MucHVzaCgndmVydGljYWwnKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXtqb2luKCcgJywgY29uY2F0KGNzcywgW2NsYXNzX25hbWVdKSl9XG4gICAgICAgICAgICAgICAgaWQ9e2lkZW50aXR5fVxuICAgICAgICAgICAgICAgIHN0eWxlPXtzdHlsZX1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICB7b3BlbmVkICYmIChcbiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2pvaW4oJyAnLCBjb25jYXQoY3NzLCBbJ2RyYXdlci1jb250ZW50J10pKX0+XG4gICAgICAgICAgICAgICAgICAgICAgICB7Y2hpbGRyZW59XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2pvaW4oJyAnLCBjb25jYXQoY3NzLCBbJ2RyYXdlci1jb250cm9sJ10pKX1cbiAgICAgICAgICAgICAgICAgICAgb25DbGljaz17KCkgPT4gdGhpcy5wcm9wcy51cGRhdGVBc3BlY3RzKHtvcGVuZWQ6ICFvcGVuZWR9KX1cbiAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgIDxDYXJldCBvcGVuZWQ9e29wZW5lZH0gc2lkZT17c2lkZX0gLz5cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuRHJhd2VyLmRlZmF1bHRQcm9wcyA9IHtcbiAgICBzaWRlOiAndG9wJyxcbn07XG5cbkRyYXdlci5wcm9wVHlwZXMgPSB7XG4gICAgY2hpbGRyZW46IFByb3BUeXBlcy5ub2RlLFxuICAgIG9wZW5lZDogUHJvcFR5cGVzLmJvb2wsXG4gICAgc3R5bGU6IFByb3BUeXBlcy5vYmplY3QsXG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBTaWRlIHdoaWNoIG9wZW4uXG4gICAgICovXG4gICAgc2lkZTogUHJvcFR5cGVzLm9uZU9mKFsndG9wJywgJ2xlZnQnLCAncmlnaHQnLCAnYm90dG9tJ10pLFxuXG4gICAgLyoqXG4gICAgICogIFVuaXF1ZSBpZCBmb3IgdGhpcyBjb21wb25lbnRcbiAgICAgKi9cbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIFVwZGF0ZSBhc3BlY3RzIG9uIHRoZSBiYWNrZW5kLlxuICAgICAqL1xuICAgIHVwZGF0ZUFzcGVjdHM6IFByb3BUeXBlcy5mdW5jLFxufTtcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUHJvcFR5cGVzIGZyb20gJ3Byb3AtdHlwZXMnO1xuaW1wb3J0IHt0aW1lc3RhbXBQcm9wfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzJztcbmltcG9ydCB7bWVyZ2V9IGZyb20gJ3JhbWRhJztcblxuLyoqXG4gKiBCcm93c2VyIG5vdGlmaWNhdGlvbnMgd2l0aCBwZXJtaXNzaW9ucyBoYW5kbGluZy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgTm90aWNlIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgICAgICBzdXBlcihwcm9wcyk7XG4gICAgICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAgICAgICBsYXN0TWVzc2FnZTogcHJvcHMuYm9keSxcbiAgICAgICAgICAgIG5vdGlmaWNhdGlvbjogbnVsbCxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5vblBlcm1pc3Npb24gPSB0aGlzLm9uUGVybWlzc2lvbi5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgICAgICBjb25zdCB7dXBkYXRlQXNwZWN0c30gPSB0aGlzLnByb3BzO1xuICAgICAgICBpZiAoISgnTm90aWZpY2F0aW9uJyBpbiB3aW5kb3cpICYmIHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoe3Blcm1pc3Npb246ICd1bnN1cHBvcnRlZCd9KTtcbiAgICAgICAgfSBlbHNlIGlmIChOb3RpZmljYXRpb24ucGVybWlzc2lvbiA9PT0gJ2RlZmF1bHQnKSB7XG4gICAgICAgICAgICBOb3RpZmljYXRpb24ucmVxdWVzdFBlcm1pc3Npb24oKS50aGVuKHRoaXMub25QZXJtaXNzaW9uKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHRoaXMub25QZXJtaXNzaW9uKHdpbmRvdy5Ob3RpZmljYXRpb24ucGVybWlzc2lvbik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRVcGRhdGUocHJldlByb3BzKSB7XG4gICAgICAgIGlmICghcHJldlByb3BzLmRpc3BsYXllZCAmJiB0aGlzLnByb3BzLmRpc3BsYXllZCkge1xuICAgICAgICAgICAgdGhpcy5zZW5kTm90aWZpY2F0aW9uKHRoaXMucHJvcHMucGVybWlzc2lvbik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBzZW5kTm90aWZpY2F0aW9uKHBlcm1pc3Npb24pIHtcbiAgICAgICAgY29uc3Qge1xuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGJvZHksXG4gICAgICAgICAgICB0aXRsZSxcbiAgICAgICAgICAgIGljb24sXG4gICAgICAgICAgICByZXF1aXJlX2ludGVyYWN0aW9uLFxuICAgICAgICAgICAgbGFuZyxcbiAgICAgICAgICAgIGJhZGdlLFxuICAgICAgICAgICAgdGFnLFxuICAgICAgICAgICAgaW1hZ2UsXG4gICAgICAgICAgICB2aWJyYXRlLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgaWYgKHBlcm1pc3Npb24gPT09ICdncmFudGVkJykge1xuICAgICAgICAgICAgY29uc3Qgb3B0aW9ucyA9IHtcbiAgICAgICAgICAgICAgICByZXF1aXJlSW50ZXJhY3Rpb246IHJlcXVpcmVfaW50ZXJhY3Rpb24sXG4gICAgICAgICAgICAgICAgYm9keSxcbiAgICAgICAgICAgICAgICBpY29uLFxuICAgICAgICAgICAgICAgIGxhbmcsXG4gICAgICAgICAgICAgICAgYmFkZ2UsXG4gICAgICAgICAgICAgICAgdGFnLFxuICAgICAgICAgICAgICAgIGltYWdlLFxuICAgICAgICAgICAgICAgIHZpYnJhdGUsXG4gICAgICAgICAgICB9O1xuICAgICAgICAgICAgY29uc3Qgbm90aWZpY2F0aW9uID0gbmV3IE5vdGlmaWNhdGlvbih0aXRsZSwgb3B0aW9ucyk7XG4gICAgICAgICAgICBub3RpZmljYXRpb24ub25jbGljayA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICBpZiAodXBkYXRlQXNwZWN0cykge1xuICAgICAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzKFxuICAgICAgICAgICAgICAgICAgICAgICAgbWVyZ2UoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAge2Rpc3BsYXllZDogZmFsc2V9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRpbWVzdGFtcFByb3AoJ2NsaWNrcycsIHRoaXMucHJvcHMuY2xpY2tzICsgMSlcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9O1xuICAgICAgICAgICAgbm90aWZpY2F0aW9uLm9uY2xvc2UgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIG1lcmdlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtkaXNwbGF5ZWQ6IGZhbHNlfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aW1lc3RhbXBQcm9wKCdjbG9zZXMnLCB0aGlzLnByb3BzLmNsb3NlcyArIDEpXG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIG9uUGVybWlzc2lvbihwZXJtaXNzaW9uKSB7XG4gICAgICAgIGNvbnN0IHtkaXNwbGF5ZWQsIHVwZGF0ZUFzcGVjdHN9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgaWYgKHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoe3Blcm1pc3Npb259KTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZGlzcGxheWVkKSB7XG4gICAgICAgICAgICB0aGlzLnNlbmROb3RpZmljYXRpb24ocGVybWlzc2lvbik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbn1cblxuTm90aWNlLmRlZmF1bHRQcm9wcyA9IHtcbiAgICByZXF1aXJlX2ludGVyYWN0aW9uOiBmYWxzZSxcbiAgICBjbGlja3M6IDAsXG4gICAgY2xpY2tzX3RpbWVzdGFtcDogLTEsXG4gICAgY2xvc2VzOiAwLFxuICAgIGNsb3Nlc190aW1lc3RhbXA6IC0xLFxufTtcblxuLy8gUHJvcHMgZG9jcyBmcm9tIGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0FQSS9Ob3RpZmljYXRpb24vTm90aWZpY2F0aW9uXG5Ob3RpY2UucHJvcFR5cGVzID0ge1xuICAgIGlkZW50aXR5OiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgLyoqXG4gICAgICogUGVybWlzc2lvbiBncmFudGVkIGJ5IHRoZSB1c2VyIChSRUFET05MWSlcbiAgICAgKi9cbiAgICBwZXJtaXNzaW9uOiBQcm9wVHlwZXMub25lT2YoW1xuICAgICAgICAnZGVuaWVkJyxcbiAgICAgICAgJ2dyYW50ZWQnLFxuICAgICAgICAnZGVmYXVsdCcsXG4gICAgICAgICd1bnN1cHBvcnRlZCcsXG4gICAgXSksXG5cbiAgICB0aXRsZTogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuXG4gICAgLyoqXG4gICAgICogVGhlIG5vdGlmaWNhdGlvbidzIGxhbmd1YWdlLCBhcyBzcGVjaWZpZWQgdXNpbmcgYSBET01TdHJpbmcgcmVwcmVzZW50aW5nIGEgQkNQIDQ3IGxhbmd1YWdlIHRhZy5cbiAgICAgKi9cbiAgICBsYW5nOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIEEgRE9NU3RyaW5nIHJlcHJlc2VudGluZyB0aGUgYm9keSB0ZXh0IG9mIHRoZSBub3RpZmljYXRpb24sIHdoaWNoIHdpbGwgYmUgZGlzcGxheWVkIGJlbG93IHRoZSB0aXRsZS5cbiAgICAgKi9cbiAgICBib2R5OiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIEEgVVNWU3RyaW5nIGNvbnRhaW5pbmcgdGhlIFVSTCBvZiB0aGUgaW1hZ2UgdXNlZCB0byByZXByZXNlbnQgdGhlIG5vdGlmaWNhdGlvbiB3aGVuIHRoZXJlIGlzIG5vdCBlbm91Z2ggc3BhY2UgdG8gZGlzcGxheSB0aGUgbm90aWZpY2F0aW9uIGl0c2VsZi5cbiAgICAgKi9cbiAgICBiYWRnZTogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIEEgRE9NU3RyaW5nIHJlcHJlc2VudGluZyBhbiBpZGVudGlmeWluZyB0YWcgZm9yIHRoZSBub3RpZmljYXRpb24uXG4gICAgICovXG4gICAgdGFnOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIEEgVVNWU3RyaW5nIGNvbnRhaW5pbmcgdGhlIFVSTCBvZiBhbiBpY29uIHRvIGJlIGRpc3BsYXllZCBpbiB0aGUgbm90aWZpY2F0aW9uLlxuICAgICAqL1xuICAgIGljb246IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogIGEgVVNWU3RyaW5nIGNvbnRhaW5pbmcgdGhlIFVSTCBvZiBhbiBpbWFnZSB0byBiZSBkaXNwbGF5ZWQgaW4gdGhlIG5vdGlmaWNhdGlvbi5cbiAgICAgKi9cbiAgICBpbWFnZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBBIHZpYnJhdGlvbiBwYXR0ZXJuIGZvciB0aGUgZGV2aWNlJ3MgdmlicmF0aW9uIGhhcmR3YXJlIHRvIGVtaXQgd2hlbiB0aGUgbm90aWZpY2F0aW9uIGZpcmVzLlxuICAgICAqL1xuICAgIHZpYnJhdGU6IFByb3BUeXBlcy5vbmVPZlR5cGUoW1xuICAgICAgICBQcm9wVHlwZXMubnVtYmVyLFxuICAgICAgICBQcm9wVHlwZXMuYXJyYXlPZihQcm9wVHlwZXMubnVtYmVyKSxcbiAgICBdKSxcbiAgICAvKipcbiAgICAgKiBJbmRpY2F0ZXMgdGhhdCBhIG5vdGlmaWNhdGlvbiBzaG91bGQgcmVtYWluIGFjdGl2ZSB1bnRpbCB0aGUgdXNlciBjbGlja3Mgb3IgZGlzbWlzc2VzIGl0LCByYXRoZXIgdGhhbiBjbG9zaW5nIGF1dG9tYXRpY2FsbHkuIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGZhbHNlLlxuICAgICAqL1xuICAgIHJlcXVpcmVfaW50ZXJhY3Rpb246IFByb3BUeXBlcy5ib29sLFxuXG4gICAgLyoqXG4gICAgICogU2V0IHRvIHRydWUgdG8gZGlzcGxheSB0aGUgbm90aWZpY2F0aW9uLlxuICAgICAqL1xuICAgIGRpc3BsYXllZDogUHJvcFR5cGVzLmJvb2wsXG5cbiAgICBjbGlja3M6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgY2xpY2tzX3RpbWVzdGFtcDogUHJvcFR5cGVzLm51bWJlcixcbiAgICAvKipcbiAgICAgKiBOdW1iZXIgb2YgdGltZXMgdGhlIG5vdGlmaWNhdGlvbiB3YXMgY2xvc2VkLlxuICAgICAqL1xuICAgIGNsb3NlczogUHJvcFR5cGVzLm51bWJlcixcbiAgICBjbG9zZXNfdGltZXN0YW1wOiBQcm9wVHlwZXMubnVtYmVyLFxuXG4gICAgdXBkYXRlQXNwZWN0OiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7cmFuZ2UsIGpvaW59IGZyb20gJ3JhbWRhJztcblxuY29uc3Qgc3RhcnRPZmZzZXQgPSAocGFnZSwgaXRlbVBlclBhZ2UpID0+XG4gICAgKHBhZ2UgLSAxKSAqIChwYWdlID4gMSA/IGl0ZW1QZXJQYWdlIDogMCk7XG5cbmNvbnN0IGVuZE9mZnNldCA9IChzdGFydCwgaXRlbVBlclBhZ2UsIHBhZ2UsIHRvdGFsLCBsZWZ0T3ZlcikgPT5cbiAgICBwYWdlICE9PSB0b3RhbFxuICAgICAgICA/IHN0YXJ0ICsgaXRlbVBlclBhZ2VcbiAgICAgICAgOiBsZWZ0T3ZlciAhPT0gMFxuICAgICAgICA/IHN0YXJ0ICsgbGVmdE92ZXJcbiAgICAgICAgOiBzdGFydCArIGl0ZW1QZXJQYWdlO1xuXG5jb25zdCBzaG93TGlzdCA9IChwYWdlLCB0b3RhbCwgbikgPT4ge1xuICAgIGlmICh0b3RhbCA+IG4pIHtcbiAgICAgICAgY29uc3QgbWlkZGxlID0gbiAvIDI7XG4gICAgICAgIGNvbnN0IGZpcnN0ID1cbiAgICAgICAgICAgIHBhZ2UgPj0gdG90YWwgLSBtaWRkbGVcbiAgICAgICAgICAgICAgICA/IHRvdGFsIC0gbiArIDFcbiAgICAgICAgICAgICAgICA6IHBhZ2UgPiBtaWRkbGVcbiAgICAgICAgICAgICAgICA/IHBhZ2UgLSBtaWRkbGVcbiAgICAgICAgICAgICAgICA6IDE7XG4gICAgICAgIGNvbnN0IGxhc3QgPSBwYWdlIDwgdG90YWwgLSBtaWRkbGUgPyBmaXJzdCArIG4gOiB0b3RhbCArIDE7XG4gICAgICAgIHJldHVybiByYW5nZShmaXJzdCwgbGFzdCk7XG4gICAgfVxuICAgIHJldHVybiByYW5nZSgxLCB0b3RhbCArIDEpO1xufTtcblxuY29uc3QgUGFnZSA9ICh7c3R5bGUsIGNsYXNzX25hbWUsIG9uX2NoYW5nZSwgdGV4dCwgcGFnZX0pID0+IChcbiAgICA8c3BhbiBzdHlsZT17c3R5bGV9IGNsYXNzTmFtZT17Y2xhc3NfbmFtZX0gb25DbGljaz17KCkgPT4gb25fY2hhbmdlKHBhZ2UpfT5cbiAgICAgICAge3RleHQgfHwgcGFnZX1cbiAgICA8L3NwYW4+XG4pO1xuXG4vKipcbiAqIFBhZ2luZyBmb3IgZGF6emxlciBhcHBzLlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBQYWdlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgY3VycmVudF9wYWdlOiBudWxsLFxuICAgICAgICAgICAgc3RhcnRfb2Zmc2V0OiBudWxsLFxuICAgICAgICAgICAgZW5kX29mZnNldDogbnVsbCxcbiAgICAgICAgICAgIHBhZ2VzOiBbXSxcbiAgICAgICAgICAgIHRvdGFsX3BhZ2VzOiBNYXRoLmNlaWwocHJvcHMudG90YWxfaXRlbXMgLyBwcm9wcy5pdGVtc19wZXJfcGFnZSksXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMub25DaGFuZ2VQYWdlID0gdGhpcy5vbkNoYW5nZVBhZ2UuYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnRXaWxsTW91bnQoKSB7XG4gICAgICAgIHRoaXMub25DaGFuZ2VQYWdlKHRoaXMucHJvcHMuY3VycmVudF9wYWdlKTtcbiAgICB9XG5cbiAgICBvbkNoYW5nZVBhZ2UocGFnZSkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBpdGVtc19wZXJfcGFnZSxcbiAgICAgICAgICAgIHRvdGFsX2l0ZW1zLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIHBhZ2VzX2Rpc3BsYXllZCxcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGNvbnN0IHt0b3RhbF9wYWdlc30gPSB0aGlzLnN0YXRlO1xuXG4gICAgICAgIGNvbnN0IHN0YXJ0X29mZnNldCA9IHN0YXJ0T2Zmc2V0KHBhZ2UsIGl0ZW1zX3Blcl9wYWdlKTtcbiAgICAgICAgY29uc3QgbGVmdE92ZXIgPSB0b3RhbF9pdGVtcyAlIGl0ZW1zX3Blcl9wYWdlO1xuXG4gICAgICAgIGNvbnN0IGVuZF9vZmZzZXQgPSBlbmRPZmZzZXQoXG4gICAgICAgICAgICBzdGFydF9vZmZzZXQsXG4gICAgICAgICAgICBpdGVtc19wZXJfcGFnZSxcbiAgICAgICAgICAgIHBhZ2UsXG4gICAgICAgICAgICB0b3RhbF9wYWdlcyxcbiAgICAgICAgICAgIGxlZnRPdmVyXG4gICAgICAgICk7XG5cbiAgICAgICAgY29uc3QgcGF5bG9hZCA9IHtcbiAgICAgICAgICAgIGN1cnJlbnRfcGFnZTogcGFnZSxcbiAgICAgICAgICAgIHN0YXJ0X29mZnNldDogc3RhcnRfb2Zmc2V0LFxuICAgICAgICAgICAgZW5kX29mZnNldDogZW5kX29mZnNldCxcbiAgICAgICAgICAgIHBhZ2VzOiBzaG93TGlzdChwYWdlLCB0b3RhbF9wYWdlcywgcGFnZXNfZGlzcGxheWVkKSxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZShwYXlsb2FkKTtcblxuICAgICAgICBpZiAodXBkYXRlQXNwZWN0cykge1xuICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUudG90YWxfcGFnZXMgIT09IHRoaXMucHJvcHMudG90YWxfcGFnZXMpIHtcbiAgICAgICAgICAgICAgICBwYXlsb2FkLnRvdGFsX3BhZ2VzID0gdGhpcy5zdGF0ZS50b3RhbF9wYWdlcztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMocGF5bG9hZCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjb21wb25lbnRXaWxsUmVjZWl2ZVByb3BzKHByb3BzKSB7XG4gICAgICAgIGlmIChwcm9wcy5jdXJyZW50X3BhZ2UgIT09IHRoaXMuc3RhdGUuY3VycmVudF9wYWdlKSB7XG4gICAgICAgICAgICB0aGlzLm9uQ2hhbmdlUGFnZShwcm9wcy5jdXJyZW50X3BhZ2UpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7Y3VycmVudF9wYWdlLCBwYWdlcywgdG90YWxfcGFnZXN9ID0gdGhpcy5zdGF0ZTtcbiAgICAgICAgY29uc3Qge2NsYXNzX25hbWUsIGlkZW50aXR5LCBwYWdlX3N0eWxlLCBwYWdlX2NsYXNzX25hbWV9ID0gdGhpcy5wcm9wcztcblxuICAgICAgICBsZXQgcGFnZUNzcyA9IFsncGFnZSddO1xuICAgICAgICBpZiAocGFnZV9jbGFzc19uYW1lKSB7XG4gICAgICAgICAgICBwYWdlQ3NzLnB1c2gocGFnZV9jbGFzc19uYW1lKTtcbiAgICAgICAgfVxuICAgICAgICBwYWdlQ3NzID0gam9pbignICcsIHBhZ2VDc3MpO1xuXG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT17Y2xhc3NfbmFtZX0gaWQ9e2lkZW50aXR5fT5cbiAgICAgICAgICAgICAgICB7Y3VycmVudF9wYWdlID4gMSAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXsxfVxuICAgICAgICAgICAgICAgICAgICAgICAgdGV4dD17J2ZpcnN0J31cbiAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPXtwYWdlX3N0eWxlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NfbmFtZT17cGFnZUNzc31cbiAgICAgICAgICAgICAgICAgICAgICAgIG9uX2NoYW5nZT17dGhpcy5vbkNoYW5nZVBhZ2V9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICB7Y3VycmVudF9wYWdlID4gMSAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXtjdXJyZW50X3BhZ2UgLSAxfVxuICAgICAgICAgICAgICAgICAgICAgICAgdGV4dD17J3ByZXZpb3VzJ31cbiAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPXtwYWdlX3N0eWxlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NfbmFtZT17cGFnZUNzc31cbiAgICAgICAgICAgICAgICAgICAgICAgIG9uX2NoYW5nZT17dGhpcy5vbkNoYW5nZVBhZ2V9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICB7cGFnZXMubWFwKGUgPT4gKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17ZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGtleT17YHBhZ2UtJHtlfWB9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICkpfVxuICAgICAgICAgICAgICAgIHtjdXJyZW50X3BhZ2UgPCB0b3RhbF9wYWdlcyAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXtjdXJyZW50X3BhZ2UgKyAxfVxuICAgICAgICAgICAgICAgICAgICAgICAgdGV4dD17J25leHQnfVxuICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGU9e3BhZ2Vfc3R5bGV9XG4gICAgICAgICAgICAgICAgICAgICAgICBjbGFzc19uYW1lPXtwYWdlQ3NzfVxuICAgICAgICAgICAgICAgICAgICAgICAgb25fY2hhbmdlPXt0aGlzLm9uQ2hhbmdlUGFnZX1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgIHtjdXJyZW50X3BhZ2UgPCB0b3RhbF9wYWdlcyAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXt0b3RhbF9wYWdlc31cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydsYXN0J31cbiAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPXtwYWdlX3N0eWxlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NfbmFtZT17cGFnZUNzc31cbiAgICAgICAgICAgICAgICAgICAgICAgIG9uX2NoYW5nZT17dGhpcy5vbkNoYW5nZVBhZ2V9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuUGFnZXIuZGVmYXVsdFByb3BzID0ge1xuICAgIGN1cnJlbnRfcGFnZTogMSxcbiAgICBpdGVtc19wZXJfcGFnZTogMTAsXG4gICAgcGFnZXNfZGlzcGxheWVkOiAxMCxcbn07XG5cblBhZ2VyLnByb3BUeXBlcyA9IHtcbiAgICAvKipcbiAgICAgKiBUaGUgdG90YWwgaXRlbXMgaW4gdGhlIHNldC5cbiAgICAgKi9cbiAgICB0b3RhbF9pdGVtczogUHJvcFR5cGVzLm51bWJlci5pc1JlcXVpcmVkLFxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2YgaXRlbXMgYSBwYWdlIGNvbnRhaW5zLlxuICAgICAqL1xuICAgIGl0ZW1zX3Blcl9wYWdlOiBQcm9wVHlwZXMubnVtYmVyLFxuXG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgc3R5bGU6IFByb3BUeXBlcy5vYmplY3QsXG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBTdHlsZSBmb3IgdGhlIHBhZ2UgbnVtYmVycy5cbiAgICAgKi9cbiAgICBwYWdlX3N0eWxlOiBQcm9wVHlwZXMub2JqZWN0LFxuICAgIC8qKlxuICAgICAqIENTUyBjbGFzcyBmb3IgdGhlIHBhZ2UgbnVtYmVycy5cbiAgICAgKi9cbiAgICBwYWdlX2NsYXNzX25hbWU6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogVGhlIG51bWJlciBvZiBwYWdlcyBkaXNwbGF5ZWQgYnkgdGhlIHBhZ2VyLlxuICAgICAqL1xuICAgIHBhZ2VzX2Rpc3BsYXllZDogUHJvcFR5cGVzLm51bWJlcixcbiAgICAvKipcbiAgICAgKiBSZWFkIG9ubHksIHRoZSBjdXJyZW50bHkgZGlzcGxheWVkIHBhZ2VzIG51bWJlcnMuXG4gICAgICovXG4gICAgcGFnZXM6IFByb3BUeXBlcy5hcnJheSxcbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBzZWxlY3RlZCBwYWdlLlxuICAgICAqL1xuICAgIGN1cnJlbnRfcGFnZTogUHJvcFR5cGVzLm51bWJlcixcbiAgICAvKipcbiAgICAgKiBTZXQgYnkgdG90YWxfaXRlbXMgLyBpdGVtc19wZXJfcGFnZVxuICAgICAqL1xuICAgIHRvdGFsX3BhZ2VzOiBQcm9wVHlwZXMubnVtYmVyLFxuXG4gICAgLyoqXG4gICAgICogVGhlIHN0YXJ0aW5nIGluZGV4IG9mIHRoZSBjdXJyZW50IHBhZ2VcbiAgICAgKiBDYW4gYmUgdXNlZCB0byBzbGljZSBkYXRhIGVnOiBkYXRhW3N0YXJ0X29mZnNldDogZW5kX29mZnNldF1cbiAgICAgKi9cbiAgICBzdGFydF9vZmZzZXQ6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgLyoqXG4gICAgICogVGhlIGVuZCBpbmRleCBvZiB0aGUgY3VycmVudCBwYWdlLlxuICAgICAqL1xuICAgIGVuZF9vZmZzZXQ6IFByb3BUeXBlcy5udW1iZXIsXG5cbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuLyoqXG4gKiBTaW1wbGUgaHRtbC9jc3Mgc3Bpbm5lci5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgU3Bpbm5lciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7Y2xhc3NfbmFtZSwgc3R5bGUsIGlkZW50aXR5fSA9IHRoaXMucHJvcHM7XG4gICAgICAgIHJldHVybiA8ZGl2IGlkPXtpZGVudGl0eX0gY2xhc3NOYW1lPXtjbGFzc19uYW1lfSBzdHlsZT17c3R5bGV9IC8+O1xuICAgIH1cbn1cblxuU3Bpbm5lci5kZWZhdWx0UHJvcHMgPSB7fTtcblxuU3Bpbm5lci5wcm9wVHlwZXMgPSB7XG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICAvKipcbiAgICAgKiAgVW5pcXVlIGlkIGZvciB0aGlzIGNvbXBvbmVudFxuICAgICAqL1xuICAgIGlkZW50aXR5OiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgLyoqXG4gICAgICogVXBkYXRlIGFzcGVjdHMgb24gdGhlIGJhY2tlbmQuXG4gICAgICovXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge21lcmdlQWxsfSBmcm9tICdyYW1kYSc7XG5cbi8qKlxuICogQSBzaG9ydGhhbmQgY29tcG9uZW50IGZvciBhIHN0aWNreSBkaXYuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFN0aWNreSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICBzdHlsZSxcbiAgICAgICAgICAgIGNoaWxkcmVuLFxuICAgICAgICAgICAgdG9wLFxuICAgICAgICAgICAgbGVmdCxcbiAgICAgICAgICAgIHJpZ2h0LFxuICAgICAgICAgICAgYm90dG9tLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgY29uc3Qgc3R5bGVzID0gbWVyZ2VBbGwoW3N0eWxlLCB7dG9wLCBsZWZ0LCByaWdodCwgYm90dG9tfV0pO1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0gc3R5bGU9e3N0eWxlc30+XG4gICAgICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5TdGlja3kuZGVmYXVsdFByb3BzID0ge307XG5cbi8vIFRPRE8gQWRkIFN0aWNreSBwcm9wcyBkZXNjcmlwdGlvbnNcblxuU3RpY2t5LnByb3BUeXBlcyA9IHtcbiAgICBjaGlsZHJlbjogUHJvcFR5cGVzLm5vZGUsXG4gICAgdG9wOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIGxlZnQ6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgcmlnaHQ6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgYm90dG9tOiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcbn07XG4iLCJpbXBvcnQgJy4uL3Njc3MvaW5kZXguc2Nzcyc7XG5cbmltcG9ydCBOb3RpY2UgZnJvbSAnLi9jb21wb25lbnRzL05vdGljZSc7XG5pbXBvcnQgUGFnZXIgZnJvbSAnLi9jb21wb25lbnRzL1BhZ2VyJztcbmltcG9ydCBTcGlubmVyIGZyb20gJy4vY29tcG9uZW50cy9TcGlubmVyJztcbmltcG9ydCBTdGlja3kgZnJvbSAnLi9jb21wb25lbnRzL1N0aWNreSc7XG5pbXBvcnQgRHJhd2VyIGZyb20gJy4vY29tcG9uZW50cy9EcmF3ZXInO1xuXG5leHBvcnQge05vdGljZSwgUGFnZXIsIFNwaW5uZXIsIFN0aWNreSwgRHJhd2VyfTtcbiIsIlxudmFyIGNvbnRlbnQgPSByZXF1aXJlKFwiISEuLi8uLi8uLi9ub2RlX21vZHVsZXMvbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4vZGlzdC9sb2FkZXIuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL2Nzcy1sb2FkZXIvZGlzdC9janMuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL3Nhc3MtbG9hZGVyL2xpYi9sb2FkZXIuanMhLi9pbmRleC5zY3NzXCIpO1xuXG5pZih0eXBlb2YgY29udGVudCA9PT0gJ3N0cmluZycpIGNvbnRlbnQgPSBbW21vZHVsZS5pZCwgY29udGVudCwgJyddXTtcblxudmFyIHRyYW5zZm9ybTtcbnZhciBpbnNlcnRJbnRvO1xuXG5cblxudmFyIG9wdGlvbnMgPSB7XCJobXJcIjp0cnVlfVxuXG5vcHRpb25zLnRyYW5zZm9ybSA9IHRyYW5zZm9ybVxub3B0aW9ucy5pbnNlcnRJbnRvID0gdW5kZWZpbmVkO1xuXG52YXIgdXBkYXRlID0gcmVxdWlyZShcIiEuLi8uLi8uLi9ub2RlX21vZHVsZXMvc3R5bGUtbG9hZGVyL2xpYi9hZGRTdHlsZXMuanNcIikoY29udGVudCwgb3B0aW9ucyk7XG5cbmlmKGNvbnRlbnQubG9jYWxzKSBtb2R1bGUuZXhwb3J0cyA9IGNvbnRlbnQubG9jYWxzO1xuXG5pZihtb2R1bGUuaG90KSB7XG5cdG1vZHVsZS5ob3QuYWNjZXB0KFwiISEuLi8uLi8uLi9ub2RlX21vZHVsZXMvbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4vZGlzdC9sb2FkZXIuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL2Nzcy1sb2FkZXIvZGlzdC9janMuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL3Nhc3MtbG9hZGVyL2xpYi9sb2FkZXIuanMhLi9pbmRleC5zY3NzXCIsIGZ1bmN0aW9uKCkge1xuXHRcdHZhciBuZXdDb250ZW50ID0gcmVxdWlyZShcIiEhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL21pbmktY3NzLWV4dHJhY3QtcGx1Z2luL2Rpc3QvbG9hZGVyLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9jc3MtbG9hZGVyL2Rpc3QvY2pzLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9zYXNzLWxvYWRlci9saWIvbG9hZGVyLmpzIS4vaW5kZXguc2Nzc1wiKTtcblxuXHRcdGlmKHR5cGVvZiBuZXdDb250ZW50ID09PSAnc3RyaW5nJykgbmV3Q29udGVudCA9IFtbbW9kdWxlLmlkLCBuZXdDb250ZW50LCAnJ11dO1xuXG5cdFx0dmFyIGxvY2FscyA9IChmdW5jdGlvbihhLCBiKSB7XG5cdFx0XHR2YXIga2V5LCBpZHggPSAwO1xuXG5cdFx0XHRmb3Ioa2V5IGluIGEpIHtcblx0XHRcdFx0aWYoIWIgfHwgYVtrZXldICE9PSBiW2tleV0pIHJldHVybiBmYWxzZTtcblx0XHRcdFx0aWR4Kys7XG5cdFx0XHR9XG5cblx0XHRcdGZvcihrZXkgaW4gYikgaWR4LS07XG5cblx0XHRcdHJldHVybiBpZHggPT09IDA7XG5cdFx0fShjb250ZW50LmxvY2FscywgbmV3Q29udGVudC5sb2NhbHMpKTtcblxuXHRcdGlmKCFsb2NhbHMpIHRocm93IG5ldyBFcnJvcignQWJvcnRpbmcgQ1NTIEhNUiBkdWUgdG8gY2hhbmdlZCBjc3MtbW9kdWxlcyBsb2NhbHMuJyk7XG5cblx0XHR1cGRhdGUobmV3Q29udGVudCk7XG5cdH0pO1xuXG5cdG1vZHVsZS5ob3QuZGlzcG9zZShmdW5jdGlvbigpIHsgdXBkYXRlKCk7IH0pO1xufSIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyJdLCJzb3VyY2VSb290IjoiIn0=