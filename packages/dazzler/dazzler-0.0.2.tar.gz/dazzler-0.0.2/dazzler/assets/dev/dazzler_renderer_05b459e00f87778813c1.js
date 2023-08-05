(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
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
/******/ 		"renderer": 0
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
/******/ 	deferredModules.push([1,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/renderer/js/components/Renderer.jsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.jsx ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Renderer; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _Updater__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.jsx");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var Renderer =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Renderer, _React$Component);

  function Renderer() {
    _classCallCheck(this, Renderer);

    return _possibleConstructorReturn(this, _getPrototypeOf(Renderer).apply(this, arguments));
  }

  _createClass(Renderer, [{
    key: "componentWillMount",
    value: function componentWillMount() {
      window.dazzler_base_url = this.props.baseUrl;
    }
  }, {
    key: "render",
    value: function render() {
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-renderer"
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Updater__WEBPACK_IMPORTED_MODULE_1__["default"], this.props));
    }
  }]);

  return Renderer;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Renderer.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number
};

/***/ }),

/***/ "./src/renderer/js/components/Updater.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Updater; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var _Wrapper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Wrapper */ "./src/renderer/js/components/Wrapper.jsx");
/* harmony import */ var _requests__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.js");
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }








function isComponent(c) {
  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(c) === 'Object' && c.hasOwnProperty('package') && c.hasOwnProperty('aspects') && c.hasOwnProperty('name') && c.hasOwnProperty('identity');
}

function hydrateProps(props, updateAspects, connect, disconnect) {
  var replace = {};
  Object.entries(props).forEach(function (_ref) {
    var _ref2 = _slicedToArray(_ref, 2),
        k = _ref2[0],
        v = _ref2[1];

    if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(v) === 'Array') {
      replace[k] = v.map(function (c) {
        if (!isComponent(c)) {
          // Mixing components and primitives
          return c;
        }

        var newProps = hydrateProps(c.aspects, updateAspects, connect, disconnect);

        if (!newProps.key) {
          newProps.key = c.identity;
        }

        return hydrateComponent(c.name, c["package"], c.identity, newProps, updateAspects, connect, disconnect);
      });
    } else if (isComponent(v)) {
      var newProps = hydrateProps(v.aspects, updateAspects, connect, disconnect);
      replace[k] = hydrateComponent(v.name, v["package"], v.identity, newProps, updateAspects, connect, disconnect);
    } else if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(v) === 'Object') {
      replace[k] = hydrateProps(v, updateAspects, connect, disconnect);
    }
  });
  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["merge"])(props, replace);
}

function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect) {
  var pack = window[package_name];
  var element = react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(pack[name], props);
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Wrapper__WEBPACK_IMPORTED_MODULE_3__["default"], {
    identity: identity,
    updateAspects: updateAspects,
    component: element,
    connect: connect,
    package_name: package_name,
    component_name: name,
    aspects: props,
    disconnect: disconnect,
    key: "wrapper-".concat(identity)
  });
}

function prepareProp(prop) {
  if (react__WEBPACK_IMPORTED_MODULE_0___default.a.isValidElement(prop)) {
    return {
      identity: prop.props.identity,
      aspects: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["map"])(prepareProp, Object(ramda__WEBPACK_IMPORTED_MODULE_2__["omit"])(['identity', 'updateAspects', '_name', '_package', 'aspects', 'key'], prop.props.aspects // You actually in the wrapper here.
      )),
      name: prop.props.component_name,
      "package": prop.props.package_name
    };
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(prop) === 'Array') {
    return prop.map(prepareProp);
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_2__["type"])(prop) === 'Object') {
    return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["map"])(prepareProp, prop);
  }

  return prop;
}

var Updater =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Updater, _React$Component);

  function Updater(props) {
    var _this;

    _classCallCheck(this, Updater);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Updater).call(this, props));
    _this.state = {
      layout: false,
      ready: false,
      page: null,
      bindings: {},
      packages: [],
      requirements: []
    }; // The api url for the page is the same but a post.
    // Fetch bindings, packages & requirements

    _this.pageApi = Object(_requests__WEBPACK_IMPORTED_MODULE_4__["apiRequest"])(_this.getHeaders.bind(_assertThisInitialized(_this)), _this.refresh.bind(_assertThisInitialized(_this)), window.location.href); // All components get connected.

    _this.boundComponents = {};
    _this.ws = null;
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    _this.connect = _this.connect.bind(_assertThisInitialized(_this));
    _this.disconnect = _this.disconnect.bind(_assertThisInitialized(_this));
    _this.onMessage = _this.onMessage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Updater, [{
    key: "updateAspects",
    value: function updateAspects(identity, aspects) {
      var _this2 = this;

      return new Promise(function (resolve) {
        var bindings = Object.keys(aspects).map(function (key) {
          return _this2.state.bindings["".concat(identity, ".").concat(key)];
        }).filter(function (e) {
          return e;
        });

        if (!bindings) {
          return resolve(0);
        }

        bindings.forEach(function (binding) {
          return _this2.sendBinding(binding, aspects[binding.trigger.aspect]);
        });
        resolve();
      });
    }
  }, {
    key: "connect",
    value: function connect(identity, setAspects, getAspect) {
      this.boundComponents[identity] = {
        setAspects: setAspects,
        getAspect: getAspect
      };
    }
  }, {
    key: "disconnect",
    value: function disconnect(identity) {
      delete this.boundComponents[identity];
    }
  }, {
    key: "onMessage",
    value: function onMessage(response) {
      var _this3 = this;

      var data = JSON.parse(response.data);
      var identity = data.identity,
          kind = data.kind,
          payload = data.payload,
          storage = data.storage,
          request_id = data.request_id;
      var store;

      if (storage === 'session') {
        store = window.sessionStorage;
      } else {
        store = window.localStorage;
      }

      switch (kind) {
        case 'set-aspect':
          var component = this.boundComponents[identity];

          if (!component) {
            var error = "Component not found: ".concat(identity);
            this.ws.send(JSON.stringify({
              error: error,
              kind: 'error'
            }));
            console.error(error);
            return;
          }

          component.setAspects(hydrateProps(payload, this.updateAspects, this.connect, this.disconnect)).then(function () {
            Object.keys(payload).forEach(function (k) {
              var key = "".concat(identity, ".").concat(k);
              var binding = _this3.state.bindings[key];

              if (binding) {
                _this3.sendBinding(binding, component.getAspect(k));
              } // What about returned components ?
              // They get their Wrapper.

            });
          });
          break;

        case 'get-aspect':
          var aspect = data.aspect;
          var wanted = this.boundComponents[identity];

          if (!wanted) {
            this.ws.send(JSON.stringify({
              kind: kind,
              identity: identity,
              aspect: aspect,
              request_id: request_id,
              error: "Aspect not found ".concat(identity, ".").concat(aspect)
            }));
            return;
          }

          var value = wanted.getAspect(aspect);
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            aspect: aspect,
            value: prepareProp(value),
            request_id: request_id
          }));
          break;

        case 'set-storage':
          store.setItem(identity, JSON.stringify(payload));
          break;

        case 'get-storage':
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            request_id: request_id,
            value: JSON.parse(store.getItem(identity))
          }));
          break;

        case 'ping':
          // Just do nothing.
          break;
      }
    }
  }, {
    key: "sendBinding",
    value: function sendBinding(binding, value) {
      var _this4 = this;

      // Collect all values and send a binding payload
      var trigger = _objectSpread({}, binding.trigger, {
        value: prepareProp(value)
      });

      var states = binding.states.map(function (state) {
        return _objectSpread({}, state, {
          value: _this4.boundComponents[state.identity] && prepareProp(_this4.boundComponents[state.identity].getAspect(state.aspect))
        });
      });
      var payload = {
        trigger: trigger,
        states: states,
        kind: 'binding',
        page: this.state.page,
        key: binding.key
      };
      this.ws.send(JSON.stringify(payload));
    }
  }, {
    key: "loadRequirements",
    value: function loadRequirements(requirements, packages) {
      var _this5 = this;

      return new Promise(function (resolve, reject) {
        var loadings = []; // Load packages first.

        Object.keys(packages).forEach(function (pack_name) {
          var pack = packages[pack_name];
          loadings = loadings.concat(pack.requirements.map(_this5.loadRequirement));
        }); // Then load requirements so they can use packages
        // and override css.

        Promise.all(loadings).then(function () {
          var i = 0; // Load in order.

          var handler = function handler() {
            if (i < requirements.length) {
              _this5.loadRequirement(requirements[i]).then(function () {
                i++;
                handler();
              });
            } else {
              resolve();
            }
          };

          handler();
        })["catch"](reject);
      });
    }
  }, {
    key: "loadRequirement",
    value: function loadRequirement(requirement) {
      return new Promise(function (resolve, reject) {
        var url = requirement.url,
            kind = requirement.kind,
            meta = requirement.meta;
        var method;

        if (kind === 'js') {
          method = _commons_js__WEBPACK_IMPORTED_MODULE_5__["loadScript"];
        } else if (kind === 'css') {
          method = _commons_js__WEBPACK_IMPORTED_MODULE_5__["loadCss"];
        } else if (kind === 'map') {
          return resolve();
        } else {
          return reject({
            error: "Invalid requirement kind: ".concat(kind)
          });
        }

        method(url, meta).then(resolve)["catch"](reject);
      });
    }
  }, {
    key: "_connectWS",
    value: function _connectWS() {
      var _this6 = this;

      // Setup websocket for updates
      var tries = 0;

      var connexion = function connexion() {
        _this6.ws = new WebSocket("ws".concat(window.location.href.startsWith('https') ? 's' : '', "://").concat(_this6.props.baseUrl || window.location.host, "/dazzler/update"));

        _this6.ws.addEventListener('message', _this6.onMessage);

        _this6.ws.onopen = function () {
          _this6.setState({
            ready: true
          });

          tries = 0;
        };

        _this6.ws.onclose = function () {
          var reconnect = function reconnect() {
            try {
              tries++;
              connexion();
            } catch (e) {
              if (tries < _this6.props.retries) {
                setTimeout(reconnect, 1000);
              }
            }
          };

          setTimeout(reconnect, 1000);
        };
      };

      connexion();
    } // TODO implement or remove dependence on these functions.

  }, {
    key: "getHeaders",
    value: function getHeaders() {
      return {};
    }
  }, {
    key: "refresh",
    value: function refresh() {}
  }, {
    key: "componentWillMount",
    value: function componentWillMount() {
      var _this7 = this;

      this.pageApi('', {
        method: 'POST'
      }).then(function (response) {
        _this7.setState({
          page: response.page,
          layout: response.layout,
          bindings: response.bindings,
          packages: response.packages,
          requirements: response.requirements
        });

        _this7.loadRequirements(response.requirements, response.packages).then(function () {
          return _this7._connectWS();
        });
      });
    }
  }, {
    key: "render",
    value: function render() {
      var _this$state = this.state,
          layout = _this$state.layout,
          ready = _this$state.ready;
      if (!ready) return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", null, "Loading...");

      if (!isComponent(layout)) {
        throw new Error("Layout is not a component: ".concat(layout));
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-rendered"
      }, hydrateComponent(layout.name, layout["package"], layout.identity, hydrateProps(layout.aspects, this.updateAspects, this.connect, this.disconnect), this.updateAspects, this.connect, this.disconnect));
    }
  }]);

  return Updater;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Updater.defaultProps = {};
Updater.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number
};

/***/ }),

/***/ "./src/renderer/js/components/Wrapper.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Wrapper; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Wraps components for aspects updating.
 */

var Wrapper =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Wrapper, _React$Component);

  function Wrapper(props) {
    var _this;

    _classCallCheck(this, Wrapper);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Wrapper).call(this, props));
    _this.state = {
      aspects: props.aspects || {},
      ready: false,
      initial: false
    };
    _this.setAspects = _this.setAspects.bind(_assertThisInitialized(_this));
    _this.getAspect = _this.getAspect.bind(_assertThisInitialized(_this));
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Wrapper, [{
    key: "updateAspects",
    value: function updateAspects(aspects) {
      var _this2 = this;

      return this.setAspects(aspects).then(function () {
        return _this2.props.updateAspects(_this2.props.identity, aspects);
      });
    }
  }, {
    key: "setAspects",
    value: function setAspects(aspects) {
      var _this3 = this;

      return new Promise(function (resolve) {
        _this3.setState({
          aspects: _objectSpread({}, _this3.state.aspects, aspects)
        }, resolve);
      });
    }
  }, {
    key: "getAspect",
    value: function getAspect(aspect) {
      return this.state.aspects[aspect];
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this4 = this;

      // Only update the component when mounted.
      // Otherwise gets a race condition with willUnmount
      this.props.connect(this.props.identity, this.setAspects, this.getAspect);

      if (!this.state.initial) {
        this.updateAspects(this.state.aspects).then(function () {
          return _this4.setState({
            ready: true,
            initial: true
          });
        });
      }
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.disconnect(this.props.identity);
    }
  }, {
    key: "render",
    value: function render() {
      var _this$props = this.props,
          component = _this$props.component,
          component_name = _this$props.component_name,
          package_name = _this$props.package_name;
      var _this$state = this.state,
          aspects = _this$state.aspects,
          ready = _this$state.ready;
      if (!ready) return null;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.cloneElement(component, _objectSpread({}, aspects, {
        updateAspects: this.updateAspects,
        identity: this.props.identity,
        class_name: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(["".concat(package_name.replace('_', '-').toLowerCase(), "-").concat(Object(_commons_js__WEBPACK_IMPORTED_MODULE_3__["camelToSpinal"])(component_name))], aspects.class_name ? aspects.class_name.split(' ') : []))
      }));
    }
  }]);

  return Wrapper;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Wrapper.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node.isRequired,
  connect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  package_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  disconnect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired
};

/***/ }),

/***/ "./src/renderer/js/index.js":
/*!**********************************!*\
  !*** ./src/renderer/js/index.js ***!
  \**********************************/
/*! exports provided: Renderer, render */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Renderer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Renderer", function() { return _components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"]; });





function render(_ref, element) {
  var baseUrl = _ref.baseUrl,
      ping = _ref.ping,
      ping_interval = _ref.ping_interval,
      retries = _ref.retries;
  react_dom__WEBPACK_IMPORTED_MODULE_1___default.a.render(react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"], {
    baseUrl: baseUrl,
    ping: ping,
    ping_interval: ping_interval,
    retries: retries
  }), element);
}



/***/ }),

/***/ "./src/renderer/js/requests.js":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.js ***!
  \*************************************/
/*! exports provided: JSONHEADERS, xhrRequest, apiRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JSONHEADERS", function() { return JSONHEADERS; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "xhrRequest", function() { return xhrRequest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "apiRequest", function() { return apiRequest; });
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* eslint-disable no-magic-numbers */
var jsonPattern = /json/i;
/**
 * @typedef {Object} XhrOptions
 * @property {string} [method='GET']
 * @property {Object} [headers={}]
 * @property {string|Blob|ArrayBuffer|object|Array} [payload='']
 */

/**
 * @type {XhrOptions}
 */

var defaultXhrOptions = {
  method: 'GET',
  headers: {},
  payload: '',
  json: true
};
var JSONHEADERS = {
  'Content-Type': 'application/json'
};
/**
 * Xhr promise wrap.
 *
 * Fetch can't do put request, so xhr still useful.
 *
 * Auto parse json responses.
 * Cancellation: xhr.abort
 * @param {string} url
 * @param {XhrOptions} [options]
 * @return {Promise}
 */

function xhrRequest(url) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : defaultXhrOptions;
  return new Promise(function (resolve, reject) {
    var _defaultXhrOptions$op = _objectSpread({}, defaultXhrOptions, options),
        method = _defaultXhrOptions$op.method,
        headers = _defaultXhrOptions$op.headers,
        payload = _defaultXhrOptions$op.payload,
        json = _defaultXhrOptions$op.json;

    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    var head = json ? _objectSpread({}, JSONHEADERS, headers) : headers;
    Object.keys(head).forEach(function (k) {
      return xhr.setRequestHeader(k, head[k]);
    });

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status < 400) {
          var responseValue = xhr.response;

          if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
            responseValue = JSON.parse(xhr.responseText);
          }

          resolve(responseValue);
        } else {
          reject({
            error: 'RequestError',
            message: "XHR ".concat(url, " FAILED - STATUS: ").concat(xhr.status, " MESSAGE: ").concat(xhr.statusText),
            status: xhr.status,
            xhr: xhr
          });
        }
      }
    };

    xhr.onerror = function (err) {
      return reject(err);
    };

    xhr.send(json ? JSON.stringify(payload) : payload);
  });
}
/**
 * Auto get headers and refresh/retry.
 *
 * @param {function} getHeaders
 * @param {function} refresh
 * @param {string} baseUrl
 */

function apiRequest(getHeaders, refresh) {
  var baseUrl = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '';
  return function () {
    var retried = false;
    var url = baseUrl + arguments[0];
    var options = arguments[1] || {};
    options.headers = _objectSpread({}, getHeaders(), options.headers);
    return new Promise(function (resolve, reject) {
      xhrRequest(url, options).then(resolve)["catch"](function (err) {
        if (err.status === 401 && !retried) {
          retried = true;
          refresh().then(function () {
            return xhrRequest(url, _objectSpread({}, options, {
              headers: _objectSpread({}, options.headers, getHeaders())
            })).then(resolve);
          })["catch"](reject);
        } else {
          reject(err);
        }
      });
    });
  };
}

/***/ }),

/***/ 1:
/*!****************************************!*\
  !*** multi ./src/renderer/js/index.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/renderer/js/index.js */"./src/renderer/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9SZW5kZXJlci5qc3giLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9VcGRhdGVyLmpzeCIsIndlYnBhY2s6Ly9kYXp6bGVyX1tuYW1lXS8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1dyYXBwZXIuanN4Iiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL3JlbmRlcmVyL2pzL2luZGV4LmpzIiwid2VicGFjazovL2RhenpsZXJfW25hbWVdLy4vc3JjL3JlbmRlcmVyL2pzL3JlcXVlc3RzLmpzIiwid2VicGFjazovL2RhenpsZXJfW25hbWVdL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0iLCJ3ZWJwYWNrOi8vZGF6emxlcl9bbmFtZV0vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0LWRvbVwiLFwiY29tbW9uanMyXCI6XCJyZWFjdC1kb21cIixcImFtZFwiOlwicmVhY3QtZG9tXCIsXCJ1bWRcIjpcInJlYWN0LWRvbVwiLFwicm9vdFwiOlwiUmVhY3RET01cIn0iXSwibmFtZXMiOlsiUmVuZGVyZXIiLCJ3aW5kb3ciLCJkYXp6bGVyX2Jhc2VfdXJsIiwicHJvcHMiLCJiYXNlVXJsIiwiUmVhY3QiLCJDb21wb25lbnQiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJzdHJpbmciLCJpc1JlcXVpcmVkIiwicGluZyIsImJvb2wiLCJwaW5nX2ludGVydmFsIiwibnVtYmVyIiwicmV0cmllcyIsImlzQ29tcG9uZW50IiwiYyIsInR5cGUiLCJoYXNPd25Qcm9wZXJ0eSIsImh5ZHJhdGVQcm9wcyIsInVwZGF0ZUFzcGVjdHMiLCJjb25uZWN0IiwiZGlzY29ubmVjdCIsInJlcGxhY2UiLCJPYmplY3QiLCJlbnRyaWVzIiwiZm9yRWFjaCIsImsiLCJ2IiwibWFwIiwibmV3UHJvcHMiLCJhc3BlY3RzIiwia2V5IiwiaWRlbnRpdHkiLCJoeWRyYXRlQ29tcG9uZW50IiwibmFtZSIsIm1lcmdlIiwicGFja2FnZV9uYW1lIiwicGFjayIsImVsZW1lbnQiLCJjcmVhdGVFbGVtZW50IiwicHJlcGFyZVByb3AiLCJwcm9wIiwiaXNWYWxpZEVsZW1lbnQiLCJvbWl0IiwiY29tcG9uZW50X25hbWUiLCJVcGRhdGVyIiwic3RhdGUiLCJsYXlvdXQiLCJyZWFkeSIsInBhZ2UiLCJiaW5kaW5ncyIsInBhY2thZ2VzIiwicmVxdWlyZW1lbnRzIiwicGFnZUFwaSIsImFwaVJlcXVlc3QiLCJnZXRIZWFkZXJzIiwiYmluZCIsInJlZnJlc2giLCJsb2NhdGlvbiIsImhyZWYiLCJib3VuZENvbXBvbmVudHMiLCJ3cyIsIm9uTWVzc2FnZSIsIlByb21pc2UiLCJyZXNvbHZlIiwia2V5cyIsImZpbHRlciIsImUiLCJiaW5kaW5nIiwic2VuZEJpbmRpbmciLCJ0cmlnZ2VyIiwiYXNwZWN0Iiwic2V0QXNwZWN0cyIsImdldEFzcGVjdCIsInJlc3BvbnNlIiwiZGF0YSIsIkpTT04iLCJwYXJzZSIsImtpbmQiLCJwYXlsb2FkIiwic3RvcmFnZSIsInJlcXVlc3RfaWQiLCJzdG9yZSIsInNlc3Npb25TdG9yYWdlIiwibG9jYWxTdG9yYWdlIiwiY29tcG9uZW50IiwiZXJyb3IiLCJzZW5kIiwic3RyaW5naWZ5IiwiY29uc29sZSIsInRoZW4iLCJ3YW50ZWQiLCJ2YWx1ZSIsInNldEl0ZW0iLCJnZXRJdGVtIiwic3RhdGVzIiwicmVqZWN0IiwibG9hZGluZ3MiLCJwYWNrX25hbWUiLCJjb25jYXQiLCJsb2FkUmVxdWlyZW1lbnQiLCJhbGwiLCJpIiwiaGFuZGxlciIsImxlbmd0aCIsInJlcXVpcmVtZW50IiwidXJsIiwibWV0YSIsIm1ldGhvZCIsImxvYWRTY3JpcHQiLCJsb2FkQ3NzIiwidHJpZXMiLCJjb25uZXhpb24iLCJXZWJTb2NrZXQiLCJzdGFydHNXaXRoIiwiaG9zdCIsImFkZEV2ZW50TGlzdGVuZXIiLCJvbm9wZW4iLCJzZXRTdGF0ZSIsIm9uY2xvc2UiLCJyZWNvbm5lY3QiLCJzZXRUaW1lb3V0IiwibG9hZFJlcXVpcmVtZW50cyIsIl9jb25uZWN0V1MiLCJFcnJvciIsImRlZmF1bHRQcm9wcyIsIldyYXBwZXIiLCJpbml0aWFsIiwiY2xvbmVFbGVtZW50IiwiY2xhc3NfbmFtZSIsImpvaW4iLCJ0b0xvd2VyQ2FzZSIsImNhbWVsVG9TcGluYWwiLCJzcGxpdCIsImZ1bmMiLCJub2RlIiwicmVuZGVyIiwiUmVhY3RET00iLCJqc29uUGF0dGVybiIsImRlZmF1bHRYaHJPcHRpb25zIiwiaGVhZGVycyIsImpzb24iLCJKU09OSEVBREVSUyIsInhoclJlcXVlc3QiLCJvcHRpb25zIiwieGhyIiwiWE1MSHR0cFJlcXVlc3QiLCJvcGVuIiwiaGVhZCIsInNldFJlcXVlc3RIZWFkZXIiLCJvbnJlYWR5c3RhdGVjaGFuZ2UiLCJyZWFkeVN0YXRlIiwiRE9ORSIsInN0YXR1cyIsInJlc3BvbnNlVmFsdWUiLCJ0ZXN0IiwiZ2V0UmVzcG9uc2VIZWFkZXIiLCJyZXNwb25zZVRleHQiLCJtZXNzYWdlIiwic3RhdHVzVGV4dCIsIm9uZXJyb3IiLCJlcnIiLCJyZXRyaWVkIiwiYXJndW1lbnRzIl0sIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTztBQ1ZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0JBQVEsb0JBQW9CO0FBQzVCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtB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UyxDQUFDLENBQUQsQ0FBL0I7QUFDQSxRQUFNbkIsT0FBTyxHQUFHbUIsU0FBUyxDQUFDLENBQUQsQ0FBVCxJQUFnQixFQUFoQztBQUNBbkIsV0FBTyxDQUFDSixPQUFSLHFCQUFzQnJGLFVBQVUsRUFBaEMsRUFBdUN5RixPQUFPLENBQUNKLE9BQS9DO0FBQ0EsV0FBTyxJQUFJN0UsT0FBSixDQUFZLFVBQUNDLE9BQUQsRUFBVWdDLE1BQVYsRUFBcUI7QUFDcEMrQyxnQkFBVSxDQUFDckMsR0FBRCxFQUFNc0MsT0FBTixDQUFWLENBQ0t0RCxJQURMLENBQ1UxQixPQURWLFdBRVcsVUFBQWlHLEdBQUcsRUFBSTtBQUNWLFlBQUlBLEdBQUcsQ0FBQ1IsTUFBSixLQUFlLEdBQWYsSUFBc0IsQ0FBQ1MsT0FBM0IsRUFBb0M7QUFDaENBLGlCQUFPLEdBQUcsSUFBVjtBQUNBekcsaUJBQU8sR0FDRmlDLElBREwsQ0FDVTtBQUFBLG1CQUNGcUQsVUFBVSxDQUFDckMsR0FBRCxvQkFDSHNDLE9BREc7QUFFTkoscUJBQU8sb0JBQ0FJLE9BQU8sQ0FBQ0osT0FEUixFQUVBckYsVUFBVSxFQUZWO0FBRkQsZUFBVixDQU1HbUMsSUFOSCxDQU1RMUIsT0FOUixDQURFO0FBQUEsV0FEVixXQVVXZ0MsTUFWWDtBQVdILFNBYkQsTUFhTztBQUNIQSxnQkFBTSxDQUFDaUUsR0FBRCxDQUFOO0FBQ0g7QUFDSixPQW5CTDtBQW9CSCxLQXJCTSxDQUFQO0FBc0JILEdBM0JEO0FBNEJILEM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDN0dELG1EOzs7Ozs7Ozs7OztBQ0FBLHVEIiwiZmlsZSI6ImRhenpsZXJfcmVuZGVyZXJfMDViNDU5ZTAwZjg3Nzc4ODEzYzEuanMiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSwgcmVxdWlyZShcInJlYWN0LWRvbVwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiLCBcInJlYWN0LWRvbVwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX3JlbmRlcmVyXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIiksIHJlcXVpcmUoXCJyZWFjdC1kb21cIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfcmVuZGVyZXJcIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSwgcm9vdFtcIlJlYWN0RE9NXCJdKTtcbn0pKHdpbmRvdywgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fLCBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X2RvbV9fKSB7XG5yZXR1cm4gIiwiIFx0Ly8gaW5zdGFsbCBhIEpTT05QIGNhbGxiYWNrIGZvciBjaHVuayBsb2FkaW5nXG4gXHRmdW5jdGlvbiB3ZWJwYWNrSnNvbnBDYWxsYmFjayhkYXRhKSB7XG4gXHRcdHZhciBjaHVua0lkcyA9IGRhdGFbMF07XG4gXHRcdHZhciBtb3JlTW9kdWxlcyA9IGRhdGFbMV07XG4gXHRcdHZhciBleGVjdXRlTW9kdWxlcyA9IGRhdGFbMl07XG5cbiBcdFx0Ly8gYWRkIFwibW9yZU1vZHVsZXNcIiB0byB0aGUgbW9kdWxlcyBvYmplY3QsXG4gXHRcdC8vIHRoZW4gZmxhZyBhbGwgXCJjaHVua0lkc1wiIGFzIGxvYWRlZCBhbmQgZmlyZSBjYWxsYmFja1xuIFx0XHR2YXIgbW9kdWxlSWQsIGNodW5rSWQsIGkgPSAwLCByZXNvbHZlcyA9IFtdO1xuIFx0XHRmb3IoO2kgPCBjaHVua0lkcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdGNodW5rSWQgPSBjaHVua0lkc1tpXTtcbiBcdFx0XHRpZihpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0pIHtcbiBcdFx0XHRcdHJlc29sdmVzLnB1c2goaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdWzBdKTtcbiBcdFx0XHR9XG4gXHRcdFx0aW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdID0gMDtcbiBcdFx0fVxuIFx0XHRmb3IobW9kdWxlSWQgaW4gbW9yZU1vZHVsZXMpIHtcbiBcdFx0XHRpZihPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwobW9yZU1vZHVsZXMsIG1vZHVsZUlkKSkge1xuIFx0XHRcdFx0bW9kdWxlc1ttb2R1bGVJZF0gPSBtb3JlTW9kdWxlc1ttb2R1bGVJZF07XG4gXHRcdFx0fVxuIFx0XHR9XG4gXHRcdGlmKHBhcmVudEpzb25wRnVuY3Rpb24pIHBhcmVudEpzb25wRnVuY3Rpb24oZGF0YSk7XG5cbiBcdFx0d2hpbGUocmVzb2x2ZXMubGVuZ3RoKSB7XG4gXHRcdFx0cmVzb2x2ZXMuc2hpZnQoKSgpO1xuIFx0XHR9XG5cbiBcdFx0Ly8gYWRkIGVudHJ5IG1vZHVsZXMgZnJvbSBsb2FkZWQgY2h1bmsgdG8gZGVmZXJyZWQgbGlzdFxuIFx0XHRkZWZlcnJlZE1vZHVsZXMucHVzaC5hcHBseShkZWZlcnJlZE1vZHVsZXMsIGV4ZWN1dGVNb2R1bGVzIHx8IFtdKTtcblxuIFx0XHQvLyBydW4gZGVmZXJyZWQgbW9kdWxlcyB3aGVuIGFsbCBjaHVua3MgcmVhZHlcbiBcdFx0cmV0dXJuIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCk7XG4gXHR9O1xuIFx0ZnVuY3Rpb24gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKSB7XG4gXHRcdHZhciByZXN1bHQ7XG4gXHRcdGZvcih2YXIgaSA9IDA7IGkgPCBkZWZlcnJlZE1vZHVsZXMubGVuZ3RoOyBpKyspIHtcbiBcdFx0XHR2YXIgZGVmZXJyZWRNb2R1bGUgPSBkZWZlcnJlZE1vZHVsZXNbaV07XG4gXHRcdFx0dmFyIGZ1bGZpbGxlZCA9IHRydWU7XG4gXHRcdFx0Zm9yKHZhciBqID0gMTsgaiA8IGRlZmVycmVkTW9kdWxlLmxlbmd0aDsgaisrKSB7XG4gXHRcdFx0XHR2YXIgZGVwSWQgPSBkZWZlcnJlZE1vZHVsZVtqXTtcbiBcdFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tkZXBJZF0gIT09IDApIGZ1bGZpbGxlZCA9IGZhbHNlO1xuIFx0XHRcdH1cbiBcdFx0XHRpZihmdWxmaWxsZWQpIHtcbiBcdFx0XHRcdGRlZmVycmVkTW9kdWxlcy5zcGxpY2UoaS0tLCAxKTtcbiBcdFx0XHRcdHJlc3VsdCA9IF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gZGVmZXJyZWRNb2R1bGVbMF0pO1xuIFx0XHRcdH1cbiBcdFx0fVxuXG4gXHRcdHJldHVybiByZXN1bHQ7XG4gXHR9XG5cbiBcdC8vIFRoZSBtb2R1bGUgY2FjaGVcbiBcdHZhciBpbnN0YWxsZWRNb2R1bGVzID0ge307XG5cbiBcdC8vIG9iamVjdCB0byBzdG9yZSBsb2FkZWQgYW5kIGxvYWRpbmcgY2h1bmtzXG4gXHQvLyB1bmRlZmluZWQgPSBjaHVuayBub3QgbG9hZGVkLCBudWxsID0gY2h1bmsgcHJlbG9hZGVkL3ByZWZldGNoZWRcbiBcdC8vIFByb21pc2UgPSBjaHVuayBsb2FkaW5nLCAwID0gY2h1bmsgbG9hZGVkXG4gXHR2YXIgaW5zdGFsbGVkQ2h1bmtzID0ge1xuIFx0XHRcInJlbmRlcmVyXCI6IDBcbiBcdH07XG5cbiBcdHZhciBkZWZlcnJlZE1vZHVsZXMgPSBbXTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuIFx0dmFyIGpzb25wQXJyYXkgPSB3aW5kb3dbXCJ3ZWJwYWNrSnNvbnBkYXp6bGVyX25hbWVfXCJdID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSB8fCBbXTtcbiBcdHZhciBvbGRKc29ucEZ1bmN0aW9uID0ganNvbnBBcnJheS5wdXNoLmJpbmQoanNvbnBBcnJheSk7XG4gXHRqc29ucEFycmF5LnB1c2ggPSB3ZWJwYWNrSnNvbnBDYWxsYmFjaztcbiBcdGpzb25wQXJyYXkgPSBqc29ucEFycmF5LnNsaWNlKCk7XG4gXHRmb3IodmFyIGkgPSAwOyBpIDwganNvbnBBcnJheS5sZW5ndGg7IGkrKykgd2VicGFja0pzb25wQ2FsbGJhY2soanNvbnBBcnJheVtpXSk7XG4gXHR2YXIgcGFyZW50SnNvbnBGdW5jdGlvbiA9IG9sZEpzb25wRnVuY3Rpb247XG5cblxuIFx0Ly8gYWRkIGVudHJ5IG1vZHVsZSB0byBkZWZlcnJlZCBsaXN0XG4gXHRkZWZlcnJlZE1vZHVsZXMucHVzaChbMSxcImNvbW1vbnNcIl0pO1xuIFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiByZWFkeVxuIFx0cmV0dXJuIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCk7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFVwZGF0ZXIgZnJvbSAnLi9VcGRhdGVyJztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFJlbmRlcmVyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICBjb21wb25lbnRXaWxsTW91bnQoKSB7XG4gICAgICAgIHdpbmRvdy5kYXp6bGVyX2Jhc2VfdXJsID0gdGhpcy5wcm9wcy5iYXNlVXJsO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1yZW5kZXJlclwiPlxuICAgICAgICAgICAgICAgIDxVcGRhdGVyIHsuLi50aGlzLnByb3BzfSAvPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5SZW5kZXJlci5wcm9wVHlwZXMgPSB7XG4gICAgYmFzZVVybDogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIHBpbmc6IFByb3BUeXBlcy5ib29sLFxuICAgIHBpbmdfaW50ZXJ2YWw6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgcmV0cmllczogUHJvcFR5cGVzLm51bWJlcixcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7YW55LCBtZXJnZSwgdHlwZSwgb21pdCwgbWFwfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQgV3JhcHBlciBmcm9tICcuL1dyYXBwZXInO1xuaW1wb3J0IHthcGlSZXF1ZXN0fSBmcm9tICcuLi9yZXF1ZXN0cyc7XG5pbXBvcnQge2xvYWRDc3MsIGxvYWRTY3JpcHR9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMnO1xuXG5mdW5jdGlvbiBpc0NvbXBvbmVudChjKSB7XG4gICAgcmV0dXJuIChcbiAgICAgICAgdHlwZShjKSA9PT0gJ09iamVjdCcgJiZcbiAgICAgICAgKGMuaGFzT3duUHJvcGVydHkoJ3BhY2thZ2UnKSAmJlxuICAgICAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnYXNwZWN0cycpICYmXG4gICAgICAgICAgICBjLmhhc093blByb3BlcnR5KCduYW1lJykgJiZcbiAgICAgICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ2lkZW50aXR5JykpXG4gICAgKTtcbn1cblxuZnVuY3Rpb24gaHlkcmF0ZVByb3BzKHByb3BzLCB1cGRhdGVBc3BlY3RzLCBjb25uZWN0LCBkaXNjb25uZWN0KSB7XG4gICAgY29uc3QgcmVwbGFjZSA9IHt9O1xuICAgIE9iamVjdC5lbnRyaWVzKHByb3BzKS5mb3JFYWNoKChbaywgdl0pID0+IHtcbiAgICAgICAgaWYgKHR5cGUodikgPT09ICdBcnJheScpIHtcbiAgICAgICAgICAgIHJlcGxhY2Vba10gPSB2Lm1hcChjID0+IHtcbiAgICAgICAgICAgICAgICBpZiAoIWlzQ29tcG9uZW50KGMpKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIE1peGluZyBjb21wb25lbnRzIGFuZCBwcmltaXRpdmVzXG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBjO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCBuZXdQcm9wcyA9IGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgYy5hc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICBkaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICBpZiAoIW5ld1Byb3BzLmtleSkge1xuICAgICAgICAgICAgICAgICAgICBuZXdQcm9wcy5rZXkgPSBjLmlkZW50aXR5O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gaHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICAgICAgYy5uYW1lLFxuICAgICAgICAgICAgICAgICAgICBjLnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgICAgIGMuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgIG5ld1Byb3BzLFxuICAgICAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICBkaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICB9IGVsc2UgaWYgKGlzQ29tcG9uZW50KHYpKSB7XG4gICAgICAgICAgICBjb25zdCBuZXdQcm9wcyA9IGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICB2LmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICByZXBsYWNlW2tdID0gaHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICB2Lm5hbWUsXG4gICAgICAgICAgICAgICAgdi5wYWNrYWdlLFxuICAgICAgICAgICAgICAgIHYuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgbmV3UHJvcHMsXG4gICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0gZWxzZSBpZiAodHlwZSh2KSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgICAgIHJlcGxhY2Vba10gPSBoeWRyYXRlUHJvcHModiwgdXBkYXRlQXNwZWN0cywgY29ubmVjdCwgZGlzY29ubmVjdCk7XG4gICAgICAgIH1cbiAgICB9KTtcbiAgICByZXR1cm4gbWVyZ2UocHJvcHMsIHJlcGxhY2UpO1xufVxuXG5mdW5jdGlvbiBoeWRyYXRlQ29tcG9uZW50KFxuICAgIG5hbWUsXG4gICAgcGFja2FnZV9uYW1lLFxuICAgIGlkZW50aXR5LFxuICAgIHByb3BzLFxuICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgY29ubmVjdCxcbiAgICBkaXNjb25uZWN0XG4pIHtcbiAgICBjb25zdCBwYWNrID0gd2luZG93W3BhY2thZ2VfbmFtZV07XG4gICAgY29uc3QgZWxlbWVudCA9IFJlYWN0LmNyZWF0ZUVsZW1lbnQocGFja1tuYW1lXSwgcHJvcHMpO1xuICAgIHJldHVybiAoXG4gICAgICAgIDxXcmFwcGVyXG4gICAgICAgICAgICBpZGVudGl0eT17aWRlbnRpdHl9XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzPXt1cGRhdGVBc3BlY3RzfVxuICAgICAgICAgICAgY29tcG9uZW50PXtlbGVtZW50fVxuICAgICAgICAgICAgY29ubmVjdD17Y29ubmVjdH1cbiAgICAgICAgICAgIHBhY2thZ2VfbmFtZT17cGFja2FnZV9uYW1lfVxuICAgICAgICAgICAgY29tcG9uZW50X25hbWU9e25hbWV9XG4gICAgICAgICAgICBhc3BlY3RzPXtwcm9wc31cbiAgICAgICAgICAgIGRpc2Nvbm5lY3Q9e2Rpc2Nvbm5lY3R9XG4gICAgICAgICAgICBrZXk9e2B3cmFwcGVyLSR7aWRlbnRpdHl9YH1cbiAgICAgICAgLz5cbiAgICApO1xufVxuXG5mdW5jdGlvbiBwcmVwYXJlUHJvcChwcm9wKSB7XG4gICAgaWYgKFJlYWN0LmlzVmFsaWRFbGVtZW50KHByb3ApKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICBpZGVudGl0eTogcHJvcC5wcm9wcy5pZGVudGl0eSxcbiAgICAgICAgICAgIGFzcGVjdHM6IG1hcChcbiAgICAgICAgICAgICAgICBwcmVwYXJlUHJvcCxcbiAgICAgICAgICAgICAgICBvbWl0KFxuICAgICAgICAgICAgICAgICAgICBbXG4gICAgICAgICAgICAgICAgICAgICAgICAnaWRlbnRpdHknLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ3VwZGF0ZUFzcGVjdHMnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ19uYW1lJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdfcGFja2FnZScsXG4gICAgICAgICAgICAgICAgICAgICAgICAnYXNwZWN0cycsXG4gICAgICAgICAgICAgICAgICAgICAgICAna2V5JyxcbiAgICAgICAgICAgICAgICAgICAgXSxcbiAgICAgICAgICAgICAgICAgICAgcHJvcC5wcm9wcy5hc3BlY3RzIC8vIFlvdSBhY3R1YWxseSBpbiB0aGUgd3JhcHBlciBoZXJlLlxuICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICksXG4gICAgICAgICAgICBuYW1lOiBwcm9wLnByb3BzLmNvbXBvbmVudF9uYW1lLFxuICAgICAgICAgICAgcGFja2FnZTogcHJvcC5wcm9wcy5wYWNrYWdlX25hbWUsXG4gICAgICAgIH07XG4gICAgfVxuICAgIGlmICh0eXBlKHByb3ApID09PSAnQXJyYXknKSB7XG4gICAgICAgIHJldHVybiBwcm9wLm1hcChwcmVwYXJlUHJvcCk7XG4gICAgfVxuICAgIGlmICh0eXBlKHByb3ApID09PSAnT2JqZWN0Jykge1xuICAgICAgICByZXR1cm4gbWFwKHByZXBhcmVQcm9wLCBwcm9wKTtcbiAgICB9XG4gICAgcmV0dXJuIHByb3A7XG59XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFVwZGF0ZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGxheW91dDogZmFsc2UsXG4gICAgICAgICAgICByZWFkeTogZmFsc2UsXG4gICAgICAgICAgICBwYWdlOiBudWxsLFxuICAgICAgICAgICAgYmluZGluZ3M6IHt9LFxuICAgICAgICAgICAgcGFja2FnZXM6IFtdLFxuICAgICAgICAgICAgcmVxdWlyZW1lbnRzOiBbXSxcbiAgICAgICAgfTtcbiAgICAgICAgLy8gVGhlIGFwaSB1cmwgZm9yIHRoZSBwYWdlIGlzIHRoZSBzYW1lIGJ1dCBhIHBvc3QuXG4gICAgICAgIC8vIEZldGNoIGJpbmRpbmdzLCBwYWNrYWdlcyAmIHJlcXVpcmVtZW50c1xuICAgICAgICB0aGlzLnBhZ2VBcGkgPSBhcGlSZXF1ZXN0KFxuICAgICAgICAgICAgdGhpcy5nZXRIZWFkZXJzLmJpbmQodGhpcyksXG4gICAgICAgICAgICB0aGlzLnJlZnJlc2guYmluZCh0aGlzKSxcbiAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ocmVmXG4gICAgICAgICk7XG4gICAgICAgIC8vIEFsbCBjb21wb25lbnRzIGdldCBjb25uZWN0ZWQuXG4gICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzID0ge307XG4gICAgICAgIHRoaXMud3MgPSBudWxsO1xuXG4gICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyA9IHRoaXMudXBkYXRlQXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmNvbm5lY3QgPSB0aGlzLmNvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5kaXNjb25uZWN0ID0gdGhpcy5kaXNjb25uZWN0LmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMub25NZXNzYWdlID0gdGhpcy5vbk1lc3NhZ2UuYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICB1cGRhdGVBc3BlY3RzKGlkZW50aXR5LCBhc3BlY3RzKSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZShyZXNvbHZlID0+IHtcbiAgICAgICAgICAgIGNvbnN0IGJpbmRpbmdzID0gT2JqZWN0LmtleXMoYXNwZWN0cylcbiAgICAgICAgICAgICAgICAubWFwKGtleSA9PiB0aGlzLnN0YXRlLmJpbmRpbmdzW2Ake2lkZW50aXR5fS4ke2tleX1gXSlcbiAgICAgICAgICAgICAgICAuZmlsdGVyKGUgPT4gZSk7XG5cbiAgICAgICAgICAgIGlmICghYmluZGluZ3MpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gcmVzb2x2ZSgwKTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgYmluZGluZ3MuZm9yRWFjaChiaW5kaW5nID0+XG4gICAgICAgICAgICAgICAgdGhpcy5zZW5kQmluZGluZyhiaW5kaW5nLCBhc3BlY3RzW2JpbmRpbmcudHJpZ2dlci5hc3BlY3RdKVxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgY29ubmVjdChpZGVudGl0eSwgc2V0QXNwZWN0cywgZ2V0QXNwZWN0KSB7XG4gICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XSA9IHtcbiAgICAgICAgICAgIHNldEFzcGVjdHMsXG4gICAgICAgICAgICBnZXRBc3BlY3QsXG4gICAgICAgIH07XG4gICAgfVxuXG4gICAgZGlzY29ubmVjdChpZGVudGl0eSkge1xuICAgICAgICBkZWxldGUgdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgIH1cblxuICAgIG9uTWVzc2FnZShyZXNwb25zZSkge1xuICAgICAgICBjb25zdCBkYXRhID0gSlNPTi5wYXJzZShyZXNwb25zZS5kYXRhKTtcbiAgICAgICAgY29uc3Qge2lkZW50aXR5LCBraW5kLCBwYXlsb2FkLCBzdG9yYWdlLCByZXF1ZXN0X2lkfSA9IGRhdGE7XG4gICAgICAgIGxldCBzdG9yZTtcbiAgICAgICAgaWYgKHN0b3JhZ2UgPT09ICdzZXNzaW9uJykge1xuICAgICAgICAgICAgc3RvcmUgPSB3aW5kb3cuc2Vzc2lvblN0b3JhZ2U7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5sb2NhbFN0b3JhZ2U7XG4gICAgICAgIH1cbiAgICAgICAgc3dpdGNoIChraW5kKSB7XG4gICAgICAgICAgICBjYXNlICdzZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCBjb21wb25lbnQgPSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgICAgICAgICAgICAgaWYgKCFjb21wb25lbnQpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc3QgZXJyb3IgPSBgQ29tcG9uZW50IG5vdCBmb3VuZDogJHtpZGVudGl0eX1gO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoSlNPTi5zdHJpbmdpZnkoe2Vycm9yLCBraW5kOiAnZXJyb3InfSkpO1xuICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmVycm9yKGVycm9yKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgICAgIGNvbXBvbmVudFxuICAgICAgICAgICAgICAgICAgICAuc2V0QXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYXlsb2FkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgT2JqZWN0LmtleXMocGF5bG9hZCkuZm9yRWFjaChrID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb25zdCBrZXkgPSBgJHtpZGVudGl0eX0uJHtrfWA7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29uc3QgYmluZGluZyA9IHRoaXMuc3RhdGUuYmluZGluZ3Nba2V5XTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoYmluZGluZykge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnNlbmRCaW5kaW5nKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbXBvbmVudC5nZXRBc3BlY3QoaylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gV2hhdCBhYm91dCByZXR1cm5lZCBjb21wb25lbnRzID9cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAvLyBUaGV5IGdldCB0aGVpciBXcmFwcGVyLlxuICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnZ2V0LWFzcGVjdCc6XG4gICAgICAgICAgICAgICAgY29uc3Qge2FzcGVjdH0gPSBkYXRhO1xuICAgICAgICAgICAgICAgIGNvbnN0IHdhbnRlZCA9IHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XTtcbiAgICAgICAgICAgICAgICBpZiAoIXdhbnRlZCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBhc3BlY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcnJvcjogYEFzcGVjdCBub3QgZm91bmQgJHtpZGVudGl0eX0uJHthc3BlY3R9YCxcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgY29uc3QgdmFsdWUgPSB3YW50ZWQuZ2V0QXNwZWN0KGFzcGVjdCk7XG4gICAgICAgICAgICAgICAgdGhpcy53cy5zZW5kKFxuICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh7XG4gICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICBhc3BlY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogcHJlcGFyZVByb3AodmFsdWUpLFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnc2V0LXN0b3JhZ2UnOlxuICAgICAgICAgICAgICAgIHN0b3JlLnNldEl0ZW0oaWRlbnRpdHksIEpTT04uc3RyaW5naWZ5KHBheWxvYWQpKTtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ2dldC1zdG9yYWdlJzpcbiAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3RfaWQsXG4gICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogSlNPTi5wYXJzZShzdG9yZS5nZXRJdGVtKGlkZW50aXR5KSksXG4gICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ3BpbmcnOlxuICAgICAgICAgICAgICAgIC8vIEp1c3QgZG8gbm90aGluZy5cbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHNlbmRCaW5kaW5nKGJpbmRpbmcsIHZhbHVlKSB7XG4gICAgICAgIC8vIENvbGxlY3QgYWxsIHZhbHVlcyBhbmQgc2VuZCBhIGJpbmRpbmcgcGF5bG9hZFxuICAgICAgICBjb25zdCB0cmlnZ2VyID0ge1xuICAgICAgICAgICAgLi4uYmluZGluZy50cmlnZ2VyLFxuICAgICAgICAgICAgdmFsdWU6IHByZXBhcmVQcm9wKHZhbHVlKSxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3Qgc3RhdGVzID0gYmluZGluZy5zdGF0ZXMubWFwKHN0YXRlID0+ICh7XG4gICAgICAgICAgICAuLi5zdGF0ZSxcbiAgICAgICAgICAgIHZhbHVlOlxuICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XSAmJlxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wKFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmJvdW5kQ29tcG9uZW50c1tzdGF0ZS5pZGVudGl0eV0uZ2V0QXNwZWN0KHN0YXRlLmFzcGVjdClcbiAgICAgICAgICAgICAgICApLFxuICAgICAgICB9KSk7XG5cbiAgICAgICAgY29uc3QgcGF5bG9hZCA9IHtcbiAgICAgICAgICAgIHRyaWdnZXIsXG4gICAgICAgICAgICBzdGF0ZXMsXG4gICAgICAgICAgICBraW5kOiAnYmluZGluZycsXG4gICAgICAgICAgICBwYWdlOiB0aGlzLnN0YXRlLnBhZ2UsXG4gICAgICAgICAgICBrZXk6IGJpbmRpbmcua2V5LFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLndzLnNlbmQoSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgIH1cblxuICAgIGxvYWRSZXF1aXJlbWVudHMocmVxdWlyZW1lbnRzLCBwYWNrYWdlcykge1xuICAgICAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICAgICAgbGV0IGxvYWRpbmdzID0gW107XG4gICAgICAgICAgICAvLyBMb2FkIHBhY2thZ2VzIGZpcnN0LlxuICAgICAgICAgICAgT2JqZWN0LmtleXMocGFja2FnZXMpLmZvckVhY2gocGFja19uYW1lID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCBwYWNrID0gcGFja2FnZXNbcGFja19uYW1lXTtcbiAgICAgICAgICAgICAgICBsb2FkaW5ncyA9IGxvYWRpbmdzLmNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgcGFjay5yZXF1aXJlbWVudHMubWFwKHRoaXMubG9hZFJlcXVpcmVtZW50KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIC8vIFRoZW4gbG9hZCByZXF1aXJlbWVudHMgc28gdGhleSBjYW4gdXNlIHBhY2thZ2VzXG4gICAgICAgICAgICAvLyBhbmQgb3ZlcnJpZGUgY3NzLlxuICAgICAgICAgICAgUHJvbWlzZS5hbGwobG9hZGluZ3MpXG4gICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICBsZXQgaSA9IDA7XG4gICAgICAgICAgICAgICAgICAgIC8vIExvYWQgaW4gb3JkZXIuXG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IGhhbmRsZXIgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoaSA8IHJlcXVpcmVtZW50cy5sZW5ndGgpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudHNbaV0pLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpKys7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGhhbmRsZXIoKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZSgpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgICAgICBoYW5kbGVyKCk7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAuY2F0Y2gocmVqZWN0KTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgbG9hZFJlcXVpcmVtZW50KHJlcXVpcmVtZW50KSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgICAgICBjb25zdCB7dXJsLCBraW5kLCBtZXRhfSA9IHJlcXVpcmVtZW50O1xuICAgICAgICAgICAgbGV0IG1ldGhvZDtcbiAgICAgICAgICAgIGlmIChraW5kID09PSAnanMnKSB7XG4gICAgICAgICAgICAgICAgbWV0aG9kID0gbG9hZFNjcmlwdDtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoa2luZCA9PT0gJ2NzcycpIHtcbiAgICAgICAgICAgICAgICBtZXRob2QgPSBsb2FkQ3NzO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChraW5kID09PSAnbWFwJykge1xuICAgICAgICAgICAgICAgIHJldHVybiByZXNvbHZlKCk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHJldHVybiByZWplY3Qoe2Vycm9yOiBgSW52YWxpZCByZXF1aXJlbWVudCBraW5kOiAke2tpbmR9YH0pO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgbWV0aG9kKHVybCwgbWV0YSlcbiAgICAgICAgICAgICAgICAudGhlbihyZXNvbHZlKVxuICAgICAgICAgICAgICAgIC5jYXRjaChyZWplY3QpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBfY29ubmVjdFdTKCkge1xuICAgICAgICAvLyBTZXR1cCB3ZWJzb2NrZXQgZm9yIHVwZGF0ZXNcbiAgICAgICAgbGV0IHRyaWVzID0gMDtcbiAgICAgICAgY29uc3QgY29ubmV4aW9uID0gKCkgPT4ge1xuICAgICAgICAgICAgdGhpcy53cyA9IG5ldyBXZWJTb2NrZXQoXG4gICAgICAgICAgICAgICAgYHdzJHtcbiAgICAgICAgICAgICAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYuc3RhcnRzV2l0aCgnaHR0cHMnKSA/ICdzJyA6ICcnXG4gICAgICAgICAgICAgICAgfTovLyR7dGhpcy5wcm9wcy5iYXNlVXJsIHx8XG4gICAgICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ob3N0fS9kYXp6bGVyL3VwZGF0ZWBcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICB0aGlzLndzLmFkZEV2ZW50TGlzdGVuZXIoJ21lc3NhZ2UnLCB0aGlzLm9uTWVzc2FnZSk7XG4gICAgICAgICAgICB0aGlzLndzLm9ub3BlbiA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgIHRyaWVzID0gMDtcbiAgICAgICAgICAgIH07XG4gICAgICAgICAgICB0aGlzLndzLm9uY2xvc2UgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgcmVjb25uZWN0ID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgICAgICAgICAgdHJpZXMrKztcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbm5leGlvbigpO1xuICAgICAgICAgICAgICAgICAgICB9IGNhdGNoIChlKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAodHJpZXMgPCB0aGlzLnByb3BzLnJldHJpZXMpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBzZXRUaW1lb3V0KHJlY29ubmVjdCwgMTAwMCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIHNldFRpbWVvdXQocmVjb25uZWN0LCAxMDAwKTtcbiAgICAgICAgICAgIH07XG4gICAgICAgIH07XG4gICAgICAgIGNvbm5leGlvbigpO1xuICAgIH1cblxuICAgIC8vIFRPRE8gaW1wbGVtZW50IG9yIHJlbW92ZSBkZXBlbmRlbmNlIG9uIHRoZXNlIGZ1bmN0aW9ucy5cbiAgICBnZXRIZWFkZXJzKCkge1xuICAgICAgICByZXR1cm4ge307XG4gICAgfVxuICAgIHJlZnJlc2goKSB7fVxuXG4gICAgY29tcG9uZW50V2lsbE1vdW50KCkge1xuICAgICAgICB0aGlzLnBhZ2VBcGkoJycsIHttZXRob2Q6ICdQT1NUJ30pLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgICAgICAgcGFnZTogcmVzcG9uc2UucGFnZSxcbiAgICAgICAgICAgICAgICBsYXlvdXQ6IHJlc3BvbnNlLmxheW91dCxcbiAgICAgICAgICAgICAgICBiaW5kaW5nczogcmVzcG9uc2UuYmluZGluZ3MsXG4gICAgICAgICAgICAgICAgcGFja2FnZXM6IHJlc3BvbnNlLnBhY2thZ2VzLFxuICAgICAgICAgICAgICAgIHJlcXVpcmVtZW50czogcmVzcG9uc2UucmVxdWlyZW1lbnRzLFxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB0aGlzLmxvYWRSZXF1aXJlbWVudHMoXG4gICAgICAgICAgICAgICAgcmVzcG9uc2UucmVxdWlyZW1lbnRzLFxuICAgICAgICAgICAgICAgIHJlc3BvbnNlLnBhY2thZ2VzXG4gICAgICAgICAgICApLnRoZW4oKCkgPT4gdGhpcy5fY29ubmVjdFdTKCkpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtsYXlvdXQsIHJlYWR5fSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGlmICghcmVhZHkpIHJldHVybiA8ZGl2PkxvYWRpbmcuLi48L2Rpdj47XG4gICAgICAgIGlmICghaXNDb21wb25lbnQobGF5b3V0KSkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBMYXlvdXQgaXMgbm90IGEgY29tcG9uZW50OiAke2xheW91dH1gKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZWRcIj5cbiAgICAgICAgICAgICAgICB7aHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0Lm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIGxheW91dC5wYWNrYWdlLFxuICAgICAgICAgICAgICAgICAgICBsYXlvdXQuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgIGxheW91dC5hc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5VcGRhdGVyLmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5VcGRhdGVyLnByb3BUeXBlcyA9IHtcbiAgICBiYXNlVXJsOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgcGluZzogUHJvcFR5cGVzLmJvb2wsXG4gICAgcGluZ19pbnRlcnZhbDogUHJvcFR5cGVzLm51bWJlcixcbiAgICByZXRyaWVzOiBQcm9wVHlwZXMubnVtYmVyLFxufTtcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUHJvcFR5cGVzIGZyb20gJ3Byb3AtdHlwZXMnO1xuaW1wb3J0IHtjb25jYXQsIGpvaW59IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7Y2FtZWxUb1NwaW5hbH0gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcyc7XG5cbi8qKlxuICogV3JhcHMgY29tcG9uZW50cyBmb3IgYXNwZWN0cyB1cGRhdGluZy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgV3JhcHBlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgYXNwZWN0czogcHJvcHMuYXNwZWN0cyB8fCB7fSxcbiAgICAgICAgICAgIHJlYWR5OiBmYWxzZSxcbiAgICAgICAgICAgIGluaXRpYWw6IGZhbHNlLFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLnNldEFzcGVjdHMgPSB0aGlzLnNldEFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5nZXRBc3BlY3QgPSB0aGlzLmdldEFzcGVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMgPSB0aGlzLnVwZGF0ZUFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICB1cGRhdGVBc3BlY3RzKGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuc2V0QXNwZWN0cyhhc3BlY3RzKS50aGVuKCgpID0+XG4gICAgICAgICAgICB0aGlzLnByb3BzLnVwZGF0ZUFzcGVjdHModGhpcy5wcm9wcy5pZGVudGl0eSwgYXNwZWN0cylcbiAgICAgICAgKTtcbiAgICB9XG5cbiAgICBzZXRBc3BlY3RzKGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKHJlc29sdmUgPT4ge1xuICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgICAgICAgICB7YXNwZWN0czogey4uLnRoaXMuc3RhdGUuYXNwZWN0cywgLi4uYXNwZWN0c319LFxuICAgICAgICAgICAgICAgIHJlc29sdmVcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGdldEFzcGVjdChhc3BlY3QpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuc3RhdGUuYXNwZWN0c1thc3BlY3RdO1xuICAgIH1cblxuICAgIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgICAgICAvLyBPbmx5IHVwZGF0ZSB0aGUgY29tcG9uZW50IHdoZW4gbW91bnRlZC5cbiAgICAgICAgLy8gT3RoZXJ3aXNlIGdldHMgYSByYWNlIGNvbmRpdGlvbiB3aXRoIHdpbGxVbm1vdW50XG4gICAgICAgIHRoaXMucHJvcHMuY29ubmVjdChcbiAgICAgICAgICAgIHRoaXMucHJvcHMuaWRlbnRpdHksXG4gICAgICAgICAgICB0aGlzLnNldEFzcGVjdHMsXG4gICAgICAgICAgICB0aGlzLmdldEFzcGVjdFxuICAgICAgICApO1xuICAgICAgICBpZiAoIXRoaXMuc3RhdGUuaW5pdGlhbCkge1xuICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzKHRoaXMuc3RhdGUuYXNwZWN0cykudGhlbigoKSA9PlxuICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlYWR5OiB0cnVlLCBpbml0aWFsOiB0cnVlfSlcbiAgICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjb21wb25lbnRXaWxsVW5tb3VudCgpIHtcbiAgICAgICAgdGhpcy5wcm9wcy5kaXNjb25uZWN0KHRoaXMucHJvcHMuaWRlbnRpdHkpO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2NvbXBvbmVudCwgY29tcG9uZW50X25hbWUsIHBhY2thZ2VfbmFtZX0gPSB0aGlzLnByb3BzO1xuICAgICAgICBjb25zdCB7YXNwZWN0cywgcmVhZHl9ID0gdGhpcy5zdGF0ZTtcbiAgICAgICAgaWYgKCFyZWFkeSkgcmV0dXJuIG51bGw7XG5cbiAgICAgICAgcmV0dXJuIFJlYWN0LmNsb25lRWxlbWVudChjb21wb25lbnQsIHtcbiAgICAgICAgICAgIC4uLmFzcGVjdHMsXG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzOiB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBpZGVudGl0eTogdGhpcy5wcm9wcy5pZGVudGl0eSxcbiAgICAgICAgICAgIGNsYXNzX25hbWU6IGpvaW4oXG4gICAgICAgICAgICAgICAgJyAnLFxuICAgICAgICAgICAgICAgIGNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgW1xuICAgICAgICAgICAgICAgICAgICAgICAgYCR7cGFja2FnZV9uYW1lXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnJlcGxhY2UoJ18nLCAnLScpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnRvTG93ZXJDYXNlKCl9LSR7Y2FtZWxUb1NwaW5hbChjb21wb25lbnRfbmFtZSl9YCxcbiAgICAgICAgICAgICAgICAgICAgXSxcbiAgICAgICAgICAgICAgICAgICAgYXNwZWN0cy5jbGFzc19uYW1lID8gYXNwZWN0cy5jbGFzc19uYW1lLnNwbGl0KCcgJykgOiBbXVxuICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICksXG4gICAgICAgIH0pO1xuICAgIH1cbn1cblxuV3JhcHBlci5wcm9wVHlwZXMgPSB7XG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYy5pc1JlcXVpcmVkLFxuICAgIGNvbXBvbmVudDogUHJvcFR5cGVzLm5vZGUuaXNSZXF1aXJlZCxcbiAgICBjb25uZWN0OiBQcm9wVHlwZXMuZnVuYy5pc1JlcXVpcmVkLFxuICAgIGNvbXBvbmVudF9uYW1lOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgcGFja2FnZV9uYW1lOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgZGlzY29ubmVjdDogUHJvcFR5cGVzLmZ1bmMuaXNSZXF1aXJlZCxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgUmVuZGVyZXIgZnJvbSAnLi9jb21wb25lbnRzL1JlbmRlcmVyJztcblxuZnVuY3Rpb24gcmVuZGVyKHtiYXNlVXJsLCBwaW5nLCBwaW5nX2ludGVydmFsLCByZXRyaWVzfSwgZWxlbWVudCkge1xuICAgIFJlYWN0RE9NLnJlbmRlcihcbiAgICAgICAgPFJlbmRlcmVyXG4gICAgICAgICAgICBiYXNlVXJsPXtiYXNlVXJsfVxuICAgICAgICAgICAgcGluZz17cGluZ31cbiAgICAgICAgICAgIHBpbmdfaW50ZXJ2YWw9e3BpbmdfaW50ZXJ2YWx9XG4gICAgICAgICAgICByZXRyaWVzPXtyZXRyaWVzfVxuICAgICAgICAvPixcbiAgICAgICAgZWxlbWVudFxuICAgICk7XG59XG5cbmV4cG9ydCB7UmVuZGVyZXIsIHJlbmRlcn07XG4iLCIvKiBlc2xpbnQtZGlzYWJsZSBuby1tYWdpYy1udW1iZXJzICovXG5cbmNvbnN0IGpzb25QYXR0ZXJuID0gL2pzb24vaTtcblxuLyoqXG4gKiBAdHlwZWRlZiB7T2JqZWN0fSBYaHJPcHRpb25zXG4gKiBAcHJvcGVydHkge3N0cmluZ30gW21ldGhvZD0nR0VUJ11cbiAqIEBwcm9wZXJ0eSB7T2JqZWN0fSBbaGVhZGVycz17fV1cbiAqIEBwcm9wZXJ0eSB7c3RyaW5nfEJsb2J8QXJyYXlCdWZmZXJ8b2JqZWN0fEFycmF5fSBbcGF5bG9hZD0nJ11cbiAqL1xuXG4vKipcbiAqIEB0eXBlIHtYaHJPcHRpb25zfVxuICovXG5jb25zdCBkZWZhdWx0WGhyT3B0aW9ucyA9IHtcbiAgICBtZXRob2Q6ICdHRVQnLFxuICAgIGhlYWRlcnM6IHt9LFxuICAgIHBheWxvYWQ6ICcnLFxuICAgIGpzb246IHRydWUsXG59O1xuXG5leHBvcnQgY29uc3QgSlNPTkhFQURFUlMgPSB7XG4gICAgJ0NvbnRlbnQtVHlwZSc6ICdhcHBsaWNhdGlvbi9qc29uJyxcbn07XG5cbi8qKlxuICogWGhyIHByb21pc2Ugd3JhcC5cbiAqXG4gKiBGZXRjaCBjYW4ndCBkbyBwdXQgcmVxdWVzdCwgc28geGhyIHN0aWxsIHVzZWZ1bC5cbiAqXG4gKiBBdXRvIHBhcnNlIGpzb24gcmVzcG9uc2VzLlxuICogQ2FuY2VsbGF0aW9uOiB4aHIuYWJvcnRcbiAqIEBwYXJhbSB7c3RyaW5nfSB1cmxcbiAqIEBwYXJhbSB7WGhyT3B0aW9uc30gW29wdGlvbnNdXG4gKiBAcmV0dXJuIHtQcm9taXNlfVxuICovXG5leHBvcnQgZnVuY3Rpb24geGhyUmVxdWVzdCh1cmwsIG9wdGlvbnMgPSBkZWZhdWx0WGhyT3B0aW9ucykge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHttZXRob2QsIGhlYWRlcnMsIHBheWxvYWQsIGpzb259ID0ge1xuICAgICAgICAgICAgLi4uZGVmYXVsdFhock9wdGlvbnMsXG4gICAgICAgICAgICAuLi5vcHRpb25zLFxuICAgICAgICB9O1xuICAgICAgICBjb25zdCB4aHIgPSBuZXcgWE1MSHR0cFJlcXVlc3QoKTtcbiAgICAgICAgeGhyLm9wZW4obWV0aG9kLCB1cmwpO1xuICAgICAgICBjb25zdCBoZWFkID0ganNvbiA/IHsuLi5KU09OSEVBREVSUywgLi4uaGVhZGVyc30gOiBoZWFkZXJzO1xuICAgICAgICBPYmplY3Qua2V5cyhoZWFkKS5mb3JFYWNoKGsgPT4geGhyLnNldFJlcXVlc3RIZWFkZXIoaywgaGVhZFtrXSkpO1xuICAgICAgICB4aHIub25yZWFkeXN0YXRlY2hhbmdlID0gKCkgPT4ge1xuICAgICAgICAgICAgaWYgKHhoci5yZWFkeVN0YXRlID09PSBYTUxIdHRwUmVxdWVzdC5ET05FKSB7XG4gICAgICAgICAgICAgICAgaWYgKHhoci5zdGF0dXMgPCA0MDApIHtcbiAgICAgICAgICAgICAgICAgICAgbGV0IHJlc3BvbnNlVmFsdWUgPSB4aHIucmVzcG9uc2U7XG4gICAgICAgICAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAgICAgICAgIGpzb25QYXR0ZXJuLnRlc3QoeGhyLmdldFJlc3BvbnNlSGVhZGVyKCdDb250ZW50LVR5cGUnKSlcbiAgICAgICAgICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXNwb25zZVZhbHVlID0gSlNPTi5wYXJzZSh4aHIucmVzcG9uc2VUZXh0KTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICByZXNvbHZlKHJlc3BvbnNlVmFsdWUpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJlamVjdCh7XG4gICAgICAgICAgICAgICAgICAgICAgICBlcnJvcjogJ1JlcXVlc3RFcnJvcicsXG4gICAgICAgICAgICAgICAgICAgICAgICBtZXNzYWdlOiBgWEhSICR7dXJsfSBGQUlMRUQgLSBTVEFUVVM6ICR7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgeGhyLnN0YXR1c1xuICAgICAgICAgICAgICAgICAgICAgICAgfSBNRVNTQUdFOiAke3hoci5zdGF0dXNUZXh0fWAsXG4gICAgICAgICAgICAgICAgICAgICAgICBzdGF0dXM6IHhoci5zdGF0dXMsXG4gICAgICAgICAgICAgICAgICAgICAgICB4aHIsXG4gICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgeGhyLm9uZXJyb3IgPSBlcnIgPT4gcmVqZWN0KGVycik7XG4gICAgICAgIHhoci5zZW5kKGpzb24gPyBKU09OLnN0cmluZ2lmeShwYXlsb2FkKSA6IHBheWxvYWQpO1xuICAgIH0pO1xufVxuXG4vKipcbiAqIEF1dG8gZ2V0IGhlYWRlcnMgYW5kIHJlZnJlc2gvcmV0cnkuXG4gKlxuICogQHBhcmFtIHtmdW5jdGlvbn0gZ2V0SGVhZGVyc1xuICogQHBhcmFtIHtmdW5jdGlvbn0gcmVmcmVzaFxuICogQHBhcmFtIHtzdHJpbmd9IGJhc2VVcmxcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFwaVJlcXVlc3QoZ2V0SGVhZGVycywgcmVmcmVzaCwgYmFzZVVybCA9ICcnKSB7XG4gICAgcmV0dXJuIGZ1bmN0aW9uKCkge1xuICAgICAgICBsZXQgcmV0cmllZCA9IGZhbHNlO1xuICAgICAgICBjb25zdCB1cmwgPSBiYXNlVXJsICsgYXJndW1lbnRzWzBdO1xuICAgICAgICBjb25zdCBvcHRpb25zID0gYXJndW1lbnRzWzFdIHx8IHt9O1xuICAgICAgICBvcHRpb25zLmhlYWRlcnMgPSB7Li4uZ2V0SGVhZGVycygpLCAuLi5vcHRpb25zLmhlYWRlcnN9O1xuICAgICAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICAgICAgeGhyUmVxdWVzdCh1cmwsIG9wdGlvbnMpXG4gICAgICAgICAgICAgICAgLnRoZW4ocmVzb2x2ZSlcbiAgICAgICAgICAgICAgICAuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGVyci5zdGF0dXMgPT09IDQwMSAmJiAhcmV0cmllZCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0cmllZCA9IHRydWU7XG4gICAgICAgICAgICAgICAgICAgICAgICByZWZyZXNoKClcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAudGhlbigoKSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB4aHJSZXF1ZXN0KHVybCwge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGhlYWRlcnM6IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAuLi5vcHRpb25zLmhlYWRlcnMsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4uZ2V0SGVhZGVycygpLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSkudGhlbihyZXNvbHZlKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAuY2F0Y2gocmVqZWN0KTtcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlamVjdChlcnIpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgIH0pO1xuICAgIH07XG59XG4iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfZG9tX187Il0sInNvdXJjZVJvb3QiOiIifQ==