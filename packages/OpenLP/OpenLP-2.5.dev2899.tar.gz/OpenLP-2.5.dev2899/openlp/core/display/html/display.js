/**
 * display.js is the main Javascript file that is used to drive the display.
 */

/**
 * Background type enumeration
 */
var BackgroundType = {
  Transparent: "transparent",
  Solid: "solid",
  Gradient: "gradient",
  Video: "video",
  Image: "image"
};

/**
 * Gradient type enumeration
 */
var GradientType = {
  Horizontal: "horizontal",
  LeftTop: "leftTop",
  LeftBottom: "leftBottom",
  Vertical: "vertical",
  Circular: "circular"
};

/**
 * Horizontal alignment enumeration
 */
var HorizontalAlign = {
  Left: "left",
  Right: "right",
  Center: "center",
  Justify: "justify"
};

/**
 * Vertical alignment enumeration
 */
var VerticalAlign = {
  Top: "top",
  Middle: "middle",
  Bottom: "bottom"
};

/**
 * Audio state enumeration
 */
var AudioState = {
  Playing: "playing",
  Paused: "paused",
  Stopped: "stopped"
};

/**
 * Return an array of elements based on the selector query
 * @param {string} selector - The selector to find elements
 * @returns {array} An array of matching elements
 */
function $(selector) {
  return Array.from(document.querySelectorAll(selector));
}

/**
 * Build linear gradient CSS
 * @private
 * @param {string} startDir - Starting direction
 * @param {string} endDir - Ending direction
 * @param {string} startColor - The starting color
 * @param {string} endColor - The ending color
 * @returns {string} A string of the gradient CSS
 */
function _buildLinearGradient(startDir, endDir, startColor, endColor) {
  return "-webkit-gradient(linear, " + startDir + ", " + endDir + ", from(" + startColor + "), to(" + endColor + ")) fixed";
}

/**
 * Build radial gradient CSS
 * @private
 * @param {string} width - Width of the gradient
 * @param {string} startColor - The starting color
 * @param {string} endColor - The ending color
 * @returns {string} A string of the gradient CSS
 */
function _buildRadialGradient(width, startColor, endColor) {
  return "-webkit-gradient(radial, " + width + " 50%, 100, " + width + " 50%, " + width + ", from(" + startColor + "), to(" + endColor + ")) fixed";
}

/**
 * Get a style value from an element (computed or manual)
 * @private
 * @param {Object} element - The element whose style we want
 * @param {string} style - The name of the style we want
 * @returns {(Number|string)} The style value (type depends on the style)
 */
function _getStyle(element, style) {
  return document.defaultView.getComputedStyle(element).getPropertyValue(style);
}

/**
 * Convert newlines to <br> tags
 * @private
 * @param {string} text - The text to parse
 * @returns {string} The text now with <br> tags
 */
function _nl2br(text) {
  return text.replace("\r\n", "\n").replace("\n", "<br>");
}

/**
 * Prepare text by creating paragraphs and calling _nl2br to convert newlines to <br> tags
 * @private
 * @param {string} text - The text to parse
 * @returns {string} The text now with <p> and <br> tags
 */
function _prepareText(text) {
  return "<p>" + _nl2br(text) + "</p>";
}

/**
 * An audio player with a play list
 */
var AudioPlayer = function (audioElement) {
  this._audioElement = null;
  this._eventListeners = {};
  this._playlist = [];
  this._currentTrack = null;
  this._canRepeat = false;
  this._state = AudioState.Stopped;
  this.createAudioElement();
};

/**
 * Call all listeners associated with this event
 * @private
 * @param {object} event - The event that was emitted
 */
AudioPlayer.prototype._callListener = function (event) {
  if (this._eventListeners.hasOwnProperty(event.type)) {
    this._eventListeners[event.type].forEach(function (listener) {
      listener(event);
    });
  }
  else {
    console.warn("Received unknown event \"" + event.type + "\", doing nothing.");
  }
};

/**
 * Create the <audio> element that is used to play the audio
 */
AudioPlayer.prototype.createAudioElement = function () {
  this._audioElement = document.createElement("audio");
  this._audioElement.addEventListener("ended", this.onEnded);
  this._audioElement.addEventListener("ended", this._callListener);
  this._audioElement.addEventListener("timeupdate", this._callListener);
  this._audioElement.addEventListener("volumechange", this._callListener);
  this._audioElement.addEventListener("durationchange", this._callListener);
  this._audioElement.addEventListener("loadeddata", this._callListener);
  document.addEventListener("complete", function(event) {
    document.body.appendChild(this._audioElement);
  });
};
AudioPlayer.prototype.addEventListener = function (eventType, listener) {
  this._eventListeners[eventType] = this._eventListeners[eventType] || [];
  this._eventListeners[eventType].push(listener);
};
AudioPlayer.prototype.onEnded = function (event) {
  this.nextTrack();
};
AudioPlayer.prototype.setCanRepeat = function (canRepeat) {
  this._canRepeat = canRepeat;
};
AudioPlayer.prototype.clearTracks = function () {
  this._playlist = [];
};
AudioPlayer.prototype.addTrack = function (track) {
  this._playlist.push(track);
};
AudioPlayer.prototype.nextTrack = function () {
  if (!!this._currentTrack) {
    var trackIndex = this._playlist.indexOf(this._currentTrack);
    if ((trackIndex + 1 >= this._playlist.length) && this._canRepeat) {
      this.play(this._playlist[0]);
    }
    else if (trackIndex + 1 < this._playlist.length) {
      this.play(this._playlist[trackIndex + 1]);
    }
    else {
      this.stop();
    }
  }
  else if (this._playlist.length > 0) {
    this.play(this._playlist[0]);
  }
  else {
    console.warn("No tracks in playlist, doing nothing.");
  }
};
AudioPlayer.prototype.play = function () {
  if (arguments.length > 0) {
    this._currentTrack = arguments[0];
    this._audioElement.src = this._currentTrack;
    this._audioElement.play();
    this._state = AudioState.Playing;
  }
  else if (this._state == AudioState.Paused) {
    this._audioElement.play();
    this._state = AudioState.Playing;
  }
  else {
    console.warn("No track currently paused and no track specified, doing nothing.");
  }
};

/**
 * Pause
 */
AudioPlayer.prototype.pause = function () {
  this._audioElement.pause();
  this._state = AudioState.Paused;
};

/**
 * Stop playing
 */
AudioPlayer.prototype.stop = function () {
  this._audioElement.pause();
  this._audioElement.src = "";
  this._state = AudioState.Stopped;
};

/**
 * The Display object is what we use from OpenLP
 */
var Display = {
  _slides: {},
  _revealConfig: {
    margin: 0.0,
    minScale: 1.0,
    maxScale: 1.0,
    controls: false,
    progress: false,
    history: false,
    overview: false,
    center: false,
    help: false,
    transition: "none",
    backgroundTransition: "none",
    viewDistance: 9999,
    width: "100%",
    height: "100%"
  },
  /**
   * Start up reveal and do any other initialisation
   */
  init: function () {
    Reveal.initialize(this._revealConfig);
  },
  /**
   * Reinitialise Reveal
   */
  reinit: function () {
    Reveal.reinitialize();
  },
  /**
   * Set the transition type
   * @param {string} transitionType - Can be one of "none", "fade", "slide", "convex", "concave", "zoom"
   */
  setTransition: function (transitionType) {
    Reveal.configure({"transition": transitionType});
  },
  /**
   * Clear the current list of slides
  */
  clearSlides: function () {
    $(".slides")[0].innerHTML = "";
    this._slides = {};
  },
  /**
   * Checks if the present slide content fits within the slide
  */
  doesContentFit: function () {
    var currSlide = $(".slides")[0];
    console.debug("scrollHeight: " + currSlide.scrollHeight + ", clientHeight: " + currSlide.clientHeight);
    return currSlide.clientHeight >= currSlide.scrollHeight;
  },
  /**
   * Generate the OpenLP startup splashscreen
   * @param {string} bg_color - The background color
   * @param {string} image - Path to the splash image
   */
  setStartupSplashScreen: function(bg_color, image) {
    Display.clearSlides();
    var globalBackground = $("#global-background")[0];
    globalBackground.style.cssText = "";
    globalBackground.style.setProperty("background", bg_color);
    var slidesDiv = $(".slides")[0];
    var section = document.createElement("section");
    section.setAttribute("id", 0);
    section.setAttribute("data-background", bg_color);
    section.setAttribute("style", "height: 100%; width: 100%; position: relative;");
    var img = document.createElement('img');
    img.src = image;
    img.setAttribute("style", "position: absolute; top: 0; bottom: 0; left: 0; right: 0; margin: auto; max-height: 100%; max-width: 100%");
    section.appendChild(img);
    slidesDiv.appendChild(section);
    Display._slides['0'] = 0;
    Display.reinit();
  },
  /**
   * Set fullscreen image from path
   * @param {string} bg_color - The background color
   * @param {string} image - Path to the image
   */
  setFullscreenImage: function(bg_color, image) {
    Display.clearSlides();
    var globalBackground = $("#global-background")[0];
    globalBackground.style.cssText = "";
    globalBackground.style.setProperty("background", bg_color);
    var slidesDiv = $(".slides")[0];
    var section = document.createElement("section");
    section.setAttribute("id", 0);
    section.setAttribute("data-background", bg_color);
    section.setAttribute("style", "height: 100%; width: 100%;");
    var img = document.createElement('img');
    img.src = image;
    img.setAttribute("style", "height: 100%; width: 100%");
    section.appendChild(img);
    slidesDiv.appendChild(section);
    Display._slides['0'] = 0;
    Display.reinit();
  },
  /**
   * Set fullscreen image from base64 data
   * @param {string} bg_color - The background color
   * @param {string} image_data - base64 encoded image data
   */
  setFullscreenImageFromData: function(bg_color, image_data) {
    Display.clearSlides();
    var globalBackground = $("#global-background")[0];
    globalBackground.style.cssText = "";
    globalBackground.style.setProperty("background", bg_color);
    var slidesDiv = $(".slides")[0];
    var section = document.createElement("section");
    section.setAttribute("id", 0);
    section.setAttribute("data-background", bg_color);
    section.setAttribute("style", "height: 100%; width: 100%;");
    var img = document.createElement('img');
    img.src = 'data:image/png;base64,' + image_data;
    img.setAttribute("style", "height: 100%; width: 100%");
    section.appendChild(img);
    slidesDiv.appendChild(section);
    Display._slides['0'] = 0;
    Display.reinit();
  },
  /**
   * Display an alert
   * @param {string} text - The alert text
   * @param {int} location - The location of the text (top, middle or bottom)
  */
 alert: function (text, location) {
  console.debug(" alert text: " + text, ", location: " + location);
  /*
   * The implementation should show an alert.
   * It should be able to handle receiving a new alert before a previous one is "finished", basically queueing it.
   */
  return;
},

  /**
   * Add a slides. If the slide exists but the HTML is different, update the slide.
   * @param {string} verse - The verse number, e.g. "v1"
   * @param {string} text - The HTML for the verse, e.g. "line1<br>line2"
   * @param {string} footer_text - The HTML for the footer"
   */
  addTextSlide: function (verse, text, footerText) {
    var html = _prepareText(text);
    if (this._slides.hasOwnProperty(verse)) {
      var slide = $("#" + verse)[0];
      if (slide.innerHTML != html) {
        slide.innerHTML = html;
      }
    }
    else {
      var slidesDiv = $(".slides")[0];
      var slide = document.createElement("section");
      slide.setAttribute("id", verse);
      slide.innerHTML = html;
      slidesDiv.appendChild(slide);
      var slides = $(".slides > section");
      this._slides[verse] = slides.length - 1;
      if (footerText) {
        $(".footer")[0].innerHTML = footerText;
      }
    }
    if ((arguments.length > 3) && (arguments[3] === true)) {
      this.reinit();
    }
    else if (arguments.length == 3) {
      this.reinit();
    }
  },
  /**
   * Set text slides.
   * @param {Object[]} slides - A list of slides to add as JS objects: {"verse": "v1", "text": "line 1\nline2"}
   */
  setTextSlides: function (slides) {
    Display.clearSlides();
    slides.forEach(function (slide) {
      Display.addTextSlide(slide.verse, slide.text, slide.footer, false);
    });
    Display.reinit();
    Display.goToSlide(0);
  },
  /**
   * Set image slides
   * @param {Object[]} slides - A list of images to add as JS objects [{"path": "url/to/file"}]
   */
  setImageSlides: function (slides) {
    Display.clearSlides();
    var slidesDiv = $(".slides")[0];
    slides.forEach(function (slide, index) {
      var section = document.createElement("section");
      section.setAttribute("id", index);
      section.setAttribute("data-background", "#000");
      section.setAttribute("style", "height: 100%; width: 100%;");
      var img = document.createElement('img');
      img.src = slide["path"];
      img.setAttribute("style", "max-width: 100%; max-height: 100%; margin: 0; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);");
      section.appendChild(img);
      slidesDiv.appendChild(section);
      Display._slides[index.toString()] = index;
    });
    Display.reinit();
  },
  /**
   * Set a video
   * @param {Object} video - The video to show as a JS object: {"path": "url/to/file"}
   */
  setVideo: function (video) {
    this.clearSlides();
    var section = document.createElement("section");
    section.setAttribute("data-background", "#000");
    var videoElement = document.createElement("video");
    videoElement.src = video["path"];
    videoElement.preload = "auto";
    videoElement.setAttribute("id", "video");
    videoElement.setAttribute("style", "height: 100%; width: 100%;");
    videoElement.autoplay = false;
    // All the update methods below are Python functions, hence not camelCase
    videoElement.addEventListener("durationchange", function (event) {
      mediaWatcher.update_duration(event.target.duration);
    });
    videoElement.addEventListener("timeupdate", function (event) {
      mediaWatcher.update_progress(event.target.currentTime);
    });
    videoElement.addEventListener("volumeupdate", function (event) {
      mediaWatcher.update_volume(event.target.volume);
    });
    videoElement.addEventListener("ratechange", function (event) {
      mediaWatcher.update_playback_rate(event.target.playbackRate);
    });
    videoElement.addEventListener("ended", function (event) {
      mediaWatcher.has_ended(event.target.ended);
    });
    videoElement.addEventListener("muted", function (event) {
      mediaWatcher.has_muted(event.target.muted);
    });
    section.appendChild(videoElement);
    $(".slides")[0].appendChild(section);
    this.reinit();
  },
  /**
   * Play a video
   */
  playVideo: function () {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].play();
    }
  },
  /**
   * Pause a video
   */
  pauseVideo: function () {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].pause();
    }
  },
  /**
   * Stop a video
   */
  stopVideo: function () {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].pause();
      videoElem[0].currentTime = 0.0;
    }
  },
  /**
   * Go to a particular time in a video
   * @param seconds The position in seconds to seek to
   */
  seekVideo: function (seconds) {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].currentTime = seconds;
    }
  },
  /**
   * Set the playback rate of a video
   * @param rate A Double of the rate. 1.0 => 100% speed, 0.75 => 75% speed, 1.25 => 125% speed, etc.
   */
  setPlaybackRate: function (rate) {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].playbackRate = rate;
    }
  },
  /**
   * Set the volume
   * @param level The volume level from 0 to 100.
   */
  setVideoVolume: function (level) {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].volume = level / 100.0;
    }
  },
  /**
   * Mute the volume
   */
  toggleVideoMute: function () {
    var videoElem = $("#video");
    if (videoElem.length == 1) {
      videoElem[0].muted = !videoElem[0].muted;
    }
  },
  /**
   * Clear the background audio playlist
   */
  clearPlaylist: function () {
    var backgroundAudoElem = $("#background-audio");
    if (backgroundAudoElem.length == 1) {
      var audio = backgroundAudoElem[0];
      /* audio.playList */
    }
  },
  /**
   * Add background audio
   * @param files The list of files as objects in an array
   */
  addBackgroundAudio: function (files) {
  },
  /**
   * Go to a slide.
   * @param slide The slide number or name, e.g. "v1", 0
   */
  goToSlide: function (slide) {
    if (this._slides.hasOwnProperty(slide)) {
      Reveal.slide(this._slides[slide]);
    }
    else {
      Reveal.slide(slide);
    }
  },
  /**
   * Go to the next slide in the list
  */
  next: Reveal.next,
  /**
   * Go to the previous slide in the list
  */
  prev: Reveal.prev,
  /**
   * Blank the screen
  */
  blankToBlack: function () {
    if (!Reveal.isPaused()) {
      Reveal.togglePause();
    }
    // var slidesDiv = $(".slides")[0];
  },
  /**
   * Blank to theme
  */
  blankToTheme: function () {
    var slidesDiv = $(".slides")[0];
    slidesDiv.style.visibility = "hidden";
    var footerDiv = $(".footer")[0];
    footerDiv.style.visibility = "hidden";
    if (Reveal.isPaused()) {
      Reveal.togglePause();
    }
  },
  /**
   * Show the screen
  */
  show: function () {
    var slidesDiv = $(".slides")[0];
    slidesDiv.style.visibility = "visible";
    var footerDiv = $(".footer")[0];
    footerDiv.style.visibility = "visible";
    if (Reveal.isPaused()) {
      Reveal.togglePause();
    }
  },
  /**
   * Figure out how many lines can fit on a slide given the font size
   * @param fontSize The font size in pts
   */
  calculateLineCount: function (fontSize) {
    var p = $(".slides > section > p");
    if (p.length == 0) {
      this.addSlide("v1", "Arky arky");
      p = $(".slides > section > p");
    }
    p = p[0];
    p.style.fontSize = "" + fontSize + "pt";
    var d = $(".slides")[0];
    var lh = parseFloat(_getStyle(p, "line-height"));
    var dh = parseFloat(_getStyle(d, "height"));
    return Math.floor(dh / lh);
  },
  setTheme: function (theme) {
    this._theme = theme;
    // Set the background
    var globalBackground = $("#global-background")[0];
    var backgroundStyle = {};
    var backgroundHtml = "";
    switch (theme.background_type) {
      case BackgroundType.Transparent:
        backgroundStyle["background"] = "transparent";
        break;
      case BackgroundType.Solid:
        backgroundStyle["background"] = theme.background_color;
        break;
      case BackgroundType.Gradient:
        switch (theme.background_direction) {
          case GradientType.Horizontal:
            backgroundStyle["background"] = _buildLinearGradient("left top", "left bottom",
                                                                 theme.background_start_color,
                                                                 theme.background_end_color);
            break;
          case GradientType.Vertical:
            backgroundStyle["background"] = _buildLinearGradient("left top", "right top",
                                                                 theme.background_start_color,
                                                                 theme.background_end_color);
            break;
          case GradientType.LeftTop:
            backgroundStyle["background"] = _buildLinearGradient("left top", "right bottom",
                                                                 theme.background_start_color,
                                                                 theme.background_end_color);
            break;
          case GradientType.LeftBottom:
            backgroundStyle["background"] = _buildLinearGradient("left bottom", "right top",
                                                                 theme.background_start_color,
                                                                 theme.background_end_color);
            break;
          case GradientType.Circular:
            backgroundStyle["background"] = _buildRadialGradient(window.innerWidth / 2, theme.background_start_color,
                                                                 theme.background_end_color);
            break;
          default:
            backgroundStyle["background"] = "#000";
        }
        break;
      case BackgroundType.Image:
        backgroundStyle["background-image"] = "url('" + theme.background_filename + "')";
        console.warn(backgroundStyle["background-image"]);
        break;
      case BackgroundType.Video:
        backgroundStyle["background-color"] = theme.background_border_color;
        backgroundHtml = "<video loop autoplay muted><source src='" + theme.background_filename + "'></video>";
        console.warn(backgroundHtml);
        break;
      default:
        backgroundStyle["background"] = "#000";
    }
    globalBackground.style.cssText = "";
    for (var key in backgroundStyle) {
      if (backgroundStyle.hasOwnProperty(key)) {
        globalBackground.style.setProperty(key, backgroundStyle[key]);
      }
    }
    if (!!backgroundHtml) {
      globalBackground.innerHTML = backgroundHtml;
    }
    // set up the main area
    mainStyle = {
      "word-wrap": "break-word",
      /*"margin": "0",
      "padding": "0"*/
    };
    if (!!theme.font_main_outline) {
      mainStyle["-webkit-text-stroke"] = "" + theme.font_main_outline_size + "pt " +
                                         theme.font_main_outline_color;
      mainStyle["-webkit-text-fill-color"] = theme.font_main_color;
    }
    mainStyle["font-family"] = theme.font_main_name;
    mainStyle["font-size"] = "" + theme.font_main_size + "pt";
    mainStyle["font-style"] = !!theme.font_main_italics ? "italic" : "";
    mainStyle["font-weight"] = !!theme.font_main_bold ? "bold" : "";
    mainStyle["color"] = theme.font_main_color;
    mainStyle["line-height"] = "" + (100 + theme.font_main_line_adjustment) + "%";
    mainStyle["text-align"] = theme.display_horizontal_align;
    if (theme.display_horizontal_align != HorizontalAlign.Justify) {
      mainStyle["white-space"] = "pre-wrap";
    }
    mainStyle["vertical-align"] = theme.display_vertical_align;
    if (theme.hasOwnProperty('font_main_shadow_size')) {
      mainStyle["text-shadow"] = theme.font_main_shadow_color + " " + theme.font_main_shadow_size + "px " +
                                 theme.font_main_shadow_size + "px";
    }
    mainStyle["padding-bottom"] = theme.display_vertical_align == VerticalAlign.Bottom ? "0.5em" : "0";
    mainStyle["padding-left"] = !!theme.font_main_outline ? "" + (theme.font_main_outline_size * 2) + "pt" : "0";
    // These need to be fixed, in the Python they use a width passed in as a parameter
    mainStyle["position"] = "absolute";
    mainStyle["width"] = "" + (window.innerWidth - (theme.font_main_outline_size * 4)) + "px";
    mainStyle["height"] = "" + (window.innerHeight - (theme.font_main_outline_size * 4)) + "px";
    mainStyle["left"] = "" + theme.font_main_x + "px";
    mainStyle["top"] = "" + theme.font_main_y + "px";
    var slidesDiv = $(".slides")[0];
    slidesDiv.style.cssText = "";
    for (var key in mainStyle) {
      if (mainStyle.hasOwnProperty(key)) {
        slidesDiv.style.setProperty(key, mainStyle[key]);
      }
    }
    // Set up the footer
    footerStyle = {
      "text-align": "left"
    };
    footerStyle["position"] = "absolute";
    footerStyle["left"] = "" + theme.font_footer_x + "px";
    footerStyle["top"] = "" + theme.font_footer_y + "px";
    footerStyle["bottom"] = "" + (window.innerHeight - theme.font_footer_y - theme.font_footer_height) + "px";
    footerStyle["width"] = "" + theme.font_footer_width + "px";
    footerStyle["font-family"] = theme.font_footer_name;
    footerStyle["font-size"] = "" + theme.font_footer_size + "pt";
    footerStyle["color"] = theme.font_footer_color;
    footerStyle["white-space"] = theme.font_footer_wrap ? "normal" : "nowrap";
    var footer = $(".footer")[0];
    footer.style.cssText = "";
    for (var key in footerStyle) {
      if (footerStyle.hasOwnProperty(key)) {
        footer.style.setProperty(key, footerStyle[key]);
      }
    }
  },
  /**
   * Return the video types supported by the video tag
   */
  getVideoTypes: function () {
    var videoElement = document.createElement('video');
    var videoTypes = [];
    if (videoElement.canPlayType('video/mp4; codecs="mp4v.20.8"') == "probably" ||
        videoElement.canPlayType('video/mp4; codecs="avc1.42E01E"') == "pobably" ||
        videoElement.canPlayType('video/mp4; codecs="avc1.42E01E, mp4a.40.2"') == "probably") {
      videoTypes.push(['video/mp4', '*.mp4']);
    }
    if (videoElement.canPlayType('video/ogg; codecs="theora"') == "probably") {
      videoTypes.push(['video/ogg', '*.ogv']);
    }
    if (videoElement.canPlayType('video/webm; codecs="vp8, vorbis"') == "probably") {
      videoTypes.push(['video/webm', '*.webm']);
    }
    return videoTypes;
  },
  /**
   * Sets the scale of the page - used to make preview widgets scale 
   */
  setScale: function(scale) {
    document.body.style.zoom = scale+"%";
  }
};
new QWebChannel(qt.webChannelTransport, function (channel) {
  window.mediaWatcher = channel.objects.mediaWatcher;
});
